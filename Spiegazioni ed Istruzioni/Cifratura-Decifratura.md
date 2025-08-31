# Cifratura e Decifratura dei dati in ThingsBoard

## Obiettivo
- I dati inizialmente vengono inviati a ThingsBoard in forma cifrata.
- L’accesso ai dati dipende dal ruolo dell’utente:
  - Viewer/pubblico: vede solo i dati cifrati.
  - Tecnico/Admin: può decifrare i dati tramite uno script esterno.
  
## Fasi operative

### 1. Configurazione ThingsBoard
- Crea gli utenti e assegna i ruoli in Tenant → Users:
  - `admin` → accesso completo (inclusa API, decifratura, modifica dashboard e tanti altri accessi).
  - `viewer` → accesso in sola lettura ai dati cifrati.
  - `nodo` → utente tecnico utilizzato dallo script Python per l'invio automatico dei dati cifrati.

### 2. Invio dei dati cifrati
- Utilizza Python con una libreria di cifratura, come cryptography.
- Cifra i dati (es. temperatura, CO₂, ecc.) con ECC.
- Invia i dati cifrati a ThingsBoard tramite HTTP POST (API telemetry)

### 3. Dashboard in ThingsBoard
- I dati vengono visualizzati decifrati dopo che vengono richiesti

### 4. Decifratura tramite Script Esterno
- Lo script permette agli utenti autorizzati (admin/tecnico) di visualizzare i dati in chiaro.
Funzionamento dello script:
- L’utente effettua il login (username e password).
- Lo script ottiene un token JWT dalle API di ThingsBoard.
- Verifica il ruolo dell’utente:
  - Se admin o tecnico → accede e decifra i dati.
  - Se viewer → accesso negato o solo visualizzazione cifrata.
- Recupera i dati cifrati via API REST.
- Decifra i dati e li mostra in output (CLI o interfaccia GUI).
