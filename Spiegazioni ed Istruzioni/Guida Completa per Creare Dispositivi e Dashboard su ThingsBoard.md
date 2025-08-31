# Guida alla Configurazione di ThingsBoard e Invio Dati da Python
## 1. Preparazione dell’Ambiente ThingsBoard
- Assicurati che ThingsBoard sia installato e in esecuzione (es. tramite Docker).
- Accedi all’interfaccia web:
  - http://localhost:8080/
  - Default login:
    - Email: sysadmin@thingsboard.org
    - Password: sysadmin

## 2. Creazione di un Tenant
- Vai su Tenants dal menu principale.
- Clicca su Add New Tenant.
- Inserisci nome e dettagli, poi salva.

## 3. Creazione di un Utente Tenant (facoltativa)
- All’interno del Tenant creato, vai su Users.
- Clicca su Add New User.
- Inserisci:
  - Email
  - Nome
  - Ruolo (es. Tenant Administrator)
- L’utente riceverà un’email per impostare la password.

## 4. Creazione di un Device
- Vai su Devices.
- Clicca su Add New Device.
- Inserisci un nome e scegli un Device Profile.
- Salva il dispositivo.
- Dopo la creazione, apri la scheda Credentials del device.
- Copia il Device Access Token, ti servirà per l’invio dei dati.

## 5. Creazione della Dashboard
- Vai su Dashboards dal menu.
- Clicca su Add New Dashboard.
- Inserisci nome e descrizione, salva.
- Apri la dashboard → clicca su Add Widget.
- Scegli il tipo di widget:
  - Es. Timeseries Chart, Gauge, Latest Value. 
- Configura il widget:
  - Seleziona il device.
  - Scegli le chiavi dei dati (es. temperature, humidity, co2).
  - Salva e posiziona i widget.

## 6. Invio dei Dati via Python
Esempio di script Python:
  import requests
  
  # Inserisci il tuo token del device
  ACCESS_TOKEN = "<DEVICE_ACCESS_TOKEN>"
  THINGSBOARD_URL = f"http://localhost:8080/api/v1/{ACCESS_TOKEN}/telemetry"
  
  # Dati da inviare
  payload = {
      "temperature": 25,
      "humidity": 40,
      "co2": 700
  }
  
  # Invio HTTP POST
  response = requests.post(THINGSBOARD_URL, json=payload)
  
  print("Status:", response.status_code)

## 7. Visualizzazione dei Dati
- I dati compariranno in tempo reale nei widget configurati.
- Puoi personalizzare:
  - Grafici storici
  - Indicatori di valore attuale
  - Allarmi e soglie
  - Colori, etichette e unità di misura
