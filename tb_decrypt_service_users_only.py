#!/usr/bin/env python3
"""
Users-only decrypt service for ThingsBoard CE.

- Consente SOLO CUSTOMER_USER (opzione: permetti TENANT_ADMIN per test via ALLOW_TENANT=true).
- Verifica che il device richiesto appartenga allo STESSO customer dell'utente.
- (Opzionale) Controllo per-utente via policy.json (utile se tutti gli utenti stanno nello stesso customer).
- Decifra l'ultimo timeseries `encrypted_value` usando le chiavi private locali.
- Invia il dato decifrato a ThingsBoard come `decrypted_value`.
"""

import base64
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any, List

from flask import Flask, request, jsonify
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from ecies import decrypt

#CONFIGURAZIONE
TB_URL = os.environ.get("TB_URL", "http://localhost:8080")
KEYS_DIR = Path(os.environ.get("KEYS_DIR", "./keys")).resolve()
POLICY_FILE = Path(os.environ.get("POLICY_FILE", "./policy.json")).resolve()
ALLOW_TENANT = os.environ.get("ALLOW_TENANT", "false").lower() == "true"
REQUEST_TIMEOUT = float(os.environ.get("REQUEST_TIMEOUT", "10"))
SEND_TO_SEPARATE_DEVICE = False 

def tb_get_user_info(jwt: str) -> Optional[Dict[str, Any]]:
    r = requests.get(f"{TB_URL}/api/auth/user",
                     headers={"X-Authorization": f"Bearer {jwt}"},
                     timeout=REQUEST_TIMEOUT)
    if r.status_code != 200:
        return None
    return r.json()

def tb_get_customer_devices(jwt: str, customer_id: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    page, page_size = 0, 100
    while True:
        r = requests.get(
            f"{TB_URL}/api/customer/{customer_id}/devices?pageSize={page_size}&page={page}",
            headers={"X-Authorization": f"Bearer {jwt}"},
            timeout=REQUEST_TIMEOUT,
        )
        if r.status_code != 200:
            return []
        data = r.json()
        out.extend(data.get("data", []))
        if data.get("hasNext"):
            page += 1
        else:
            break
    return out

def tb_find_device_id_by_name(jwt: str, customer_id: str, device_name: str) -> Optional[str]:
    devices = tb_get_customer_devices(jwt, customer_id)
    for device in devices:
        if device.get("name") == device_name:
            return device.get("id", {}).get("id")
    return None

def tb_fetch_all_encrypted(jwt: str, device_id: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Recupera fino a `limit` valori cifrati dalla telemetry."""
    r = requests.get(
        f"{TB_URL}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries",
        params={"keys": "encrypted_value", "limit": limit, "orderBy": "DESC"}, 
        headers={"X-Authorization": f"Bearer {jwt}"},
        timeout=REQUEST_TIMEOUT,
    )
    if r.status_code != 200:
        return []
    data = r.json()
    vals: List[Dict[str, Any]] = data.get("encrypted_value", [])
    return vals 


#CHIAVI
def _load_private_hex_for_room(room: str) -> Optional[str]:
    pem_path = KEYS_DIR / f"private_key_{room}.pem"
    hex_path = KEYS_DIR / f"private_key_{room}.hex"

    if hex_path.exists():
        return hex_path.read_text().strip()

    if not pem_path.exists():
        return None

    pem_data = pem_path.read_bytes()
    key = serialization.load_pem_private_key(pem_data, password=None, backend=default_backend())
    priv_int = key.private_numbers().private_value
    return f"{priv_int:064x}"

def decrypt_b64_with_priv_hex(b64_cipher: str, priv_hex: str) -> Optional[str]:
    try:
        ciphertext = base64.b64decode(b64_cipher.encode())
        plaintext = decrypt(bytes.fromhex(priv_hex), ciphertext)
        return plaintext.decode(errors="ignore")
    except Exception:
        return None

#AUTORIZZAZIONE
def _load_policy() -> Dict[str, List[str]]:
    if POLICY_FILE.exists():
        try:
            return json.loads(POLICY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def is_user_allowed_for_room(user_info: Dict[str, Any], room: str) -> bool:
    authority = user_info.get("authority")
    if authority == "CUSTOMER_USER":
        pass
    elif ALLOW_TENANT and authority in ("TENANT_ADMIN", "SYS_ADMIN"):
        return True
    else:
        return False

    customer_id = user_info.get("customerId", {}).get("id")
    if not customer_id:
        return False

    devices = tb_get_customer_devices(user_info["jwt"], customer_id)
    device_names = {d.get("name") for d in devices}
    if room not in device_names:
        return False

    pol = _load_policy()
    identities = [
        (user_info.get("email") or "").lower(),
        (user_info.get("name") or "").lower(),
        ((user_info.get("firstName") or "").lower() + "." + (user_info.get("lastName") or "").lower()).strip("."),
    ]
    for ident in identities:
        if ident and ident in pol:
            return room in set(pol[ident])
    return True

#MANDA I DATI DECIFRATI
def tb_fetch_encrypted_series(jwt: str, device_id: str,
                              start_ts: int, end_ts: int,
                              limit: int = 1000) -> List[Dict[str, Any]]:
    """Recupera una serie completa di valori cifrati da ThingsBoard."""
    r = requests.get(
        f"{TB_URL}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries",
        params={
            "keys": "encrypted_value",
            "startTs": start_ts,
            "endTs": end_ts,
            "limit": limit,
            "orderBy": "ASC"
        },
        headers={"X-Authorization": f"Bearer {jwt}"},
        timeout=REQUEST_TIMEOUT,
    )
    if r.status_code != 200:
        return []
    data = r.json()
    return data.get("encrypted_value", [])


def send_bulk_decrypted_to_tb(jwt: str, device_id: str, values: List[Dict[str, Any]]):
    """Invia tutti i valori decifrati a ThingsBoard mantenendo il timestamp."""
    url = f"{TB_URL}/api/plugins/telemetry/DEVICE/{device_id}/timeseries/values"
    headers = {
        "Content-Type": "application/json",
        "X-Authorization": f"Bearer {jwt}"
    }
    
    payload = []
    for v in values:
        payload.append({
            "ts": v["ts"],
            "values": {
                "decrypted_value": v["decrypted_value"]
            }
        })
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT)
        if r.status_code != 200:
            print(f"⚠️ Errore invio bulk telemetry: {r.status_code} -> {r.text}")
    except Exception as e:
        print(f"❌ Errore POST bulk: {e}")


@app.get("/decrypt")
def api_decrypt():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "missing_or_invalid_authorization_header"}), 401
    jwt = auth.split(" ", 1)[1].strip()

    room = request.args.get("room")
    if not room:
        return jsonify({"error": "missing_room_param"}), 400

    start_ts = int(request.args.get("startTs", "0"))
    end_ts = int(request.args.get("endTs", str(int(__import__("time").time() * 1000))))
    limit = int(request.args.get("limit", "1000"))

    user = tb_get_user_info(jwt)
    if not user:
        return jsonify({"error": "invalid_token"}), 401
    user["jwt"] = jwt

    if not is_user_allowed_for_room(user, room):
        return jsonify({"error": "forbidden"}), 403

    customer_id = user.get("customerId", {}).get("id")
    dev_id = tb_find_device_id_by_name(jwt, customer_id, room)
    if not dev_id:
        return jsonify({"error": "device_not_found"}), 404

    enc_list = tb_fetch_encrypted_series(jwt, dev_id, start_ts, end_ts, limit)
    if not enc_list:
        return jsonify({"error": "no_encrypted_values"}), 404

    priv_hex = _load_private_hex_for_room(room)
    if not priv_hex:
        return jsonify({"error": "missing_private_key"}), 500

    decrypted_list = []
    for item in enc_list:
        plain = decrypt_b64_with_priv_hex(item["value"], priv_hex)
        try:
            val = float(plain)  # forza a numero
        except ValueError:
            val = None

        decrypted_list.append({
            "ts": item["ts"],
            "encrypted_value": item["value"],
            "decrypted_value": val
        })

    send_bulk_decrypted_to_tb(jwt, dev_id, decrypted_list)

    return jsonify({
        "room": room,
        "count": len(decrypted_list),
        "values": decrypted_list
    })

def cli_decrypt(jwt: str, room: str) -> None:
    class DummyReq:
        headers = {"Authorization": f"Bearer {jwt}"}
        args = {"room": room}
    with app.test_request_context(headers=DummyReq.headers, query_string=DummyReq.args):
        resp = api_decrypt()
        if isinstance(resp, tuple):
            body, status = resp
            print(status, body.get_json())
        else:
            print(resp.get_json())

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Users-only TB decrypt service (API + CLI)")
    parser.add_argument("--serve", action="store_true", help="Run Flask server on 0.0.0.0:5050")
    parser.add_argument("--jwt", help="TB JWT for quick CLI test")
    parser.add_argument("--room", help="Device name (room)")
    args = parser.parse_args()

    if args.serve:
        app.run(host="0.0.0.0", port=5050, debug=True)
    elif args.jwt and args.room:
        cli_decrypt(args.jwt, args.room)
    else:
        print("Use --serve to start the server, or --jwt <JWT> --room <Room> for CLI mode.")