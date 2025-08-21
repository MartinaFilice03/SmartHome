# SmartHome
Progetto IoT con ThingsBoard e Docker

Progetto universitario realizzato con ThingsBoard e Docker per il monitoraggio di dispositivi IoT.

## Tecnologie utilizzate

- ThingsBoard CE (Community Edition): https://thingsboard.io
- Docker & Docker Compose: https://www.docker.com
- PostgreSQL

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
- Aggiungi un nuovo utente
- Crea dispositivi e dashboard
- Configura allarmi e notifiche

## Collaboratori
- Martina Filice
- Corinne D'Elia

## Struttura del progetto
- docker-compose.yml — Configurazione per ThingsBoard e PostgreSQL
- README.md — Documentazione del progetto
- CO2_Adeunis - Dataset contenente i dati di CO2 riguardante 10 stanze a cui è associato il Timestamp e Data e ora
- ground_plan_sensors.jpg - Piantina delle stanze
- tb_decrypt_service_users_only.py - Servizio per decifrare la telemetria cifrata dei device su ThingsBoard
- SvolgimentoProgetto/ — report passo-passo del progetto
- Spiegazioni ed Istruzioni/ — guide e manuali d’uso
- dashboards/ — JSON pronti all’importazione

## Uso del progetto
Una volta avviato tutto si può:
- Monitorare i sensori
- Vedere i grafici CO2 per ogni stanza
- Gestire utenti e tenant
- Inviare allarmi e notifiche
- Creazione di diverse dashboard con all'interno uno o più widget

## Note:
- Il progetto è sviluppato con l'utilizzo di Docker Desktop come applicazione e ci si collega tramite interfaccia web a ThingsBoard
- Per lavorare in gruppo, i file vengono condivisi su GitHub.
- Per importare dati/dispositivi tra ambienti diversi si usano le funzioni di export/import di ThingsBoard
- Nella piattaforma viene utilizzato HTML per creare un grafico con bottone per accedere ai dati e l'aggiunta di email e password per verificare l'autenticazione
- Viene utilizzato python per gli script che servono per mandare i dati cifrati ai dispositivi e poi decifrare i dati e rimandarli a ThingsBoard per visualizzarli tramite i grafici
- Come algoritmo di routing viene utilizzato AODV, con i relativi messaggi di Route Request e Reply, per mettere in comunicazione le varie stanze in base alla cartina 
