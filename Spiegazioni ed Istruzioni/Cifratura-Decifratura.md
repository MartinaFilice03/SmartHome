# Cifratura e Decifratura dei dati in ThingsBoard

## Obiettivo
- I dati arrivano a ThingsBoard **cifrati**.
- Utenti diversi hanno permessi diversi:
  - **Viewer/pubblici:** vedono solo i dati cifrati.
  - **Tecnico/Admin:** possono decifrare i dati tramite script esterno.
  
## Fasi operative

### 1. Configurazione ThingsBoard
- Crea utenti e ruoli:
  - `admin`: accesso completo.
  - `viewer`: sola lettura (dati cifrati).
  - `nodo`: script Python che invia i dati.
- Imposta i permessi in `Tenant → Users`.

### 2. Invio dei dati cifrati
- Usa Python e una libreria come **cryptography**.
- Cifra i dati con Fernet (o AES/ECC).
- Invia i dati cifrati via MQTT o HTTP POST a ThingsBoard.

### 3. Dashboard in ThingsBoard
- Mostra i dati cifrati così come arrivano.
- Aggiungi un messaggio tipo: _“Dati cifrati: accesso riservato”_.

### 4. Script/App esterna per utenti autorizzati
- L’utente fa login (username + password).
- Lo script ottiene un token da ThingsBoard.
- Controlla il ruolo utente:
  - Se `tecnico` o `admin` → procede con la decifratura.
  - Se `viewer` → blocca o mostra solo cifrato.
- Recupera i dati cifrati via API
