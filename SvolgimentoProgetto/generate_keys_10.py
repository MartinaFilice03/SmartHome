from ecies.utils import generate_key
from pathlib import Path

#Cartella dove salvare le chiavi
KEYS_DIR =  Path(r"C:\Users\martinafilice\Desktop\TIROCINIO")

#Lista delle stanze a cui associare una coppia di chiavi
STANZE = [
    "Meeting1", "Zone2_window1", "Zone2_window2", "Meeting2",
    "Zone3_window", "Meeting3", "Meeting4",
    "Zone3_back", "Break_room", "Zone2_back"
]

#Se non esiste crea la cartella
KEYS_DIR.mkdir(parents=True, exist_ok=True)

for stanza in STANZE:
    #Genera chiave privata e pubblica
    priv = generate_key()
    pub = priv.public_key

    #File di destinazione (privata/pubblica)
    priv_path = KEYS_DIR / f"private_key_{stanza}.pem"
    pub_path  = KEYS_DIR / f"public_key_{stanza}.pem"

    #Salva la privata come hex (segreta)
    with open(priv_path, "wb") as f:
        f.write(priv.to_hex().encode())

    #Salva la pubblica compressa come hex
    with open(pub_path, "wb") as f:
        f.write(pub.format(True).hex().encode())

    print(f"🔑 Coppia di chiavi generata per {stanza}: {priv_path.name}, {pub_path.name}")

print("✅ Fatto.")
