import base64
import requests
import pandas as pd
from pathlib import Path
from ecies import encrypt
from aodv import AODV

#CONFIGURAZIONE
THINGSBOARD_URL = "http://localhost:8080"
EXCEL_FILE = r"/Users/martinafilice/Desktop/TIROCINIO/DataSets IAQ/Repository-Processed/Grenoble/CO2_Adeunis.xlsx"
KEYS_DIR   = Path("/Users/martinafilice/Desktop/TIROCINIO/keys")
BATCH_SIZE = 500 #Dimensione batch telemetry
ROUTE_TTL_SECONDS = 300   #TTL rotte AODV
LOG_EVERY_BATCH = 1  #Stampa gli hop ad ogni batch

#Device reali ThingsBoard (10 stanze del dataset)
STANZE_TOKEN = {
    "Meeting1":       "OOYgBrVjfHG062yttNlK",
    "Meeting2":       "JxjGRTNCH61DXfoWU2g8",
    "Meeting3":       "UyOWyz45PwyZTOHZbDM9",
    "Meeting4":       "tCxelX0hD6fhIWOEwjaB",
    "Zone2_window1":  "KocJcwx36aEsIsbzoKea",
    "Zone2_window2":  "rjn5WlGBdmlxOnUOwI0Q",
    "Zone2_back":     "ae9bE7YV6Qp6wBXXjl0g",
    "Zone3_window":   "w6AgksKf08IgXyDOynIW",
    "Zone3_back":     "BDoypTUxx6Lk7mqYW4gq",
    "Break_room":     "ScCkA81CmWttfPw8gMIw"
}

#Nome “sink” per i log (nodo finale)
THINGSBOARD_SINK_NAME = "ThingsBoard"

#Grafo dei vicini (multi-hop logico verso Break_room → ThingsBoard)
NEIGHBORS = {
    #Zona 2 (due sensori vicini alle finestre) convergono sul back della zona 2
    "Zone2_window1": ["Zone2_back"],
    "Zone2_window2": ["Zone2_back"],

    #Dalla zona 2 si passa verso l'ala ovest (Meeting3) e poi al corridoio nord (Meeting2 → Meeting1)
    "Zone2_back":    ["Meeting3"],
    "Meeting3":      ["Meeting2"],
    "Meeting2":      ["Meeting1"],

    #Dall'ala nord si entra in zona 3 e poi si torna verso il centro
    "Meeting1":      ["Zone3_window"],
    "Zone3_window":  ["Zone3_back"],
    "Zone3_back":    ["Break_room"],

    #Il piano superiore (Meeting4) scende vicino alla break room (scala accanto)
    "Meeting4":      ["Break_room"],

    #Convergenza finale
    "Break_room":    [THINGSBOARD_SINK_NAME],
    THINGSBOARD_SINK_NAME: []
}
# FINE CONFIGURAZIONE

#Assicura che esista una colonna timestamp (ms); converte se serve
def _ensure_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    if "timestamp" in df.columns and pd.api.types.is_numeric_dtype(df["timestamp"]):
        return df
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["timestamp"] = (df["timestamp"].astype("int64") // 10**6)
        return df
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["timestamp"] = (df["Date"].astype("int64") // 10**6)
        return df
    raise ValueError("Manca una colonna timestamp o Date nel dataset.")

#Legge la chiave pubblica (hex) salvata per una stanza
def _public_hex(keys_dir: Path, stanza: str) -> str | None:
    p = keys_dir / f"public_key_{stanza}.pem"
    return p.read_text().strip() if p.exists() else None

#Invia un batch di punti a ThingsBoard e stampa esito
def _post_batch(session: requests.Session, url: str, payload: list[dict], stanza: str) -> None:
    resp = session.post(url, json=payload, timeout=30)
    if resp.status_code == 200:
        print(f"✅ Inviati {len(payload)} punti ({stanza})")
    else:
        print(f"❌ Errore batch ({stanza}): {resp.status_code} - {resp.text}")

#Carica dataset e prepara timestamp
def main():
    df = pd.read_excel(EXCEL_FILE, engine="openpyxl")
    df = _ensure_timestamp(df)

    #Inizializza il protocollo AODV con topologia e TTL rotte
    aodv = AODV(NEIGHBORS, ttl_seconds=ROUTE_TTL_SECONDS)

    with requests.Session() as session:
        session.headers.update({"Content-Type": "application/json"})

        #Ciclo su tutte le stanze del dataset (10 device su TB)
        for stanza, token in STANZE_TOKEN.items():
            pub_hex = _public_hex(KEYS_DIR, stanza)
            if not pub_hex:
                print(f"❌ Mancano le chiavi pubbliche per {stanza}")
                continue

            #Cerca/calcola un percorso stanza → sink (solo per log)
            path = aodv.get_path(stanza, THINGSBOARD_SINK_NAME) or aodv.discover(stanza, THINGSBOARD_SINK_NAME)
            if not path:
                print(f"⚠️ Nessun percorso {stanza} → {THINGSBOARD_SINK_NAME}")
                continue
            print(f"\n📡 AODV {stanza} → {THINGSBOARD_SINK_NAME} : " + " → ".join(path))

            #Endpoint ThingsBoard per il device della stanza
            url = f"{THINGSBOARD_URL}/api/v1/{token}/telemetry"

            batch_payload: list[dict] = []
            sent_batches = 0

            #Scorre tutte le righe del dataset
            for _, row in df.iterrows():
                if stanza not in row or pd.isna(row[stanza]):
                    continue

                valore = float(row[stanza]) #Valore sensore
                ts = int(row["timestamp"]) #Timestamp ms

                #Cifra il valore e codifica base64
                plaintext = f"{round(valore, 2)}".encode()
                encoded = base64.b64encode(encrypt(bytes.fromhex(pub_hex), plaintext)).decode()

                values = {"encrypted_value": encoded}

                batch_payload.append({"ts": ts, "values": values})

                #Invia batch quando raggiunge BATCH_SIZE
                if len(batch_payload) >= BATCH_SIZE:
                    sent_batches += 1
                    if LOG_EVERY_BATCH and (sent_batches % LOG_EVERY_BATCH == 0):
                        #Log degli hop attraversati
                        for i in range(len(path)-1):
                            print(f"   hop {i+1}/{len(path)-1}: {path[i]} ➜ {path[i+1]}")
                    _post_batch(session, url, batch_payload, stanza)
                    batch_payload.clear()
                    
            #Invia l’ultimo batch residuo
            if batch_payload:
                sent_batches += 1
                if LOG_EVERY_BATCH and (sent_batches % LOG_EVERY_BATCH == 0):
                    for i in range(len(path)-1):
                        print(f"   hop {i+1}/{len(path)-1}: {path[i]} ➜ {path[i+1]}")
                _post_batch(session, url, batch_payload, stanza)

    print("\n Fine invii AODV (per-device, 10 stanze).")

if __name__ == "__main__":
    main()
