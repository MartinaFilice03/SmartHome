# SmartHome - Progetto IoT con ThingsBoard e Docker

Progetto universitario realizzato con ThingsBoard e Docker per il monitoraggio di dispositivi IoT.

## Tecnologie utilizzate

- [ThingsBoard CE](https://thingsboard.io)
- [Docker](https://www.docker.com) & Docker Compose
- PostgreSQL
- Python
- HTML/JS per widget custom
- Algoritmo di routing AODV

## Installazione e Configurazione

### 1. Installare Docker
Se utilizzi un computer **Apple (macOS)**, segui la guida ufficiale:  
[Installazione Docker Desktop per Mac](https://docs.docker.com/desktop/setup/install/mac-install/)

Per altri sistemi operativi:  
- [Installazione su Windows](https://docs.docker.com/desktop/setup/install/windows-install/)  
- [Installazione su Linux](https://docs.docker.com/engine/install/)  

### 2. Avviare ThingsBoard con Docker Compose
Dopo aver clonato il repository ed esserti posizionato nella cartella del progetto, esegui:
docker-compose up -d

### 3. Accedere all’interfaccia web
Apri il browser e vai su: http://localhost:8080

Credenziali di default di ThingsBoard CE:
- Username: tenant@thingsboard.org
- Password: tenant

### 4. Configurazione iniziale
- Crea un nuovo tenant
- Aggiungi utenti personalizzati
- Registra i dispositivi
- Crea dashboard e widget
- Configura allarmi e notifiche automatiche

## Struttura del progetto
- docker-compose.yml — configurazione Docker per ThingsBoard e PostgreSQL
- README.md — documentazione del progetto
- CO2_Adeunis/ — dataset CO₂ con timestamp e metadati
- ground_plan_sensors.jpg — piantina delle stanze
- tb_decrypt_service_users_only.py — script di decifratura dati
- SvolgimentoProgetto/ — report dettagliato dello sviluppo
- Spiegazioni ed Istruzioni/ — guide e manuali d'uso
- dashboards/ — JSON per importazione dashboard

## Funzionalità Principali
- Monitoraggio in tempo reale dei sensori ambientali (CO₂)
- Visualizzazione su dashboard personalizzate
- Gestione utenti e tenant
- Allarmi automatici
- Script Python per cifratura/decifratura dati e invio a ThingsBoard
- Simulazione di rete tra dispositivi con AODV (Route Request & Reply)

## Sicurezza e Autenticazione
- Widget custom in HTML includono autenticazione tramite email/password
- I dati dei sensori sono cifrati in uscita e decifrati prima della visualizzazione
- Gestione separata degli utenti per tenant
  
## Algoritmo di Routing
- Utilizzato AODV (Ad hoc On-Demand Distance Vector) per simulare la comunicazione tra stanze:
- Route Request (RREQ)
- Route Reply (RREP)
- Mappatura sulla cartina ground_plan_sensors.jpg

## Uso del progetto
Dopo l’avvio:
- Visualizza dati ambientali su dashboard dinamiche
- Accedi ai grafici CO₂ per ogni stanza
- Crea utenti e gestisci permessi
- Ricevi allarmi in base a soglie di sicurezza
- Esegui import/export di configurazioni ThingsBoard

## Collaboratrici
- Martina Filice
- Corinne D'Elia

## Note:
- rogetto compatibile con Docker Desktop
- GitHub usato per la collaborazione in gruppo
- Import/export dei dispositivi e dati tramite funzionalità ThingsBoard
