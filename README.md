# SmartHome
Progetto IoT con ThingsBoard e Docker

Progetto universitario realizzato con ThingsBoard e Docker per il monitoraggio di dispositivi IoT.

## Tecnologie utilizzate

- ThingsBoard CE (Community Edition): https://thingsboard.io
- Docker & Docker Compose: https://www.docker.com
- PostgreSQL

## Installazione e Configurazione
Per utilizzare ThingsBoard e Docker inizialmente si deve installare Docker tramite il seguente sito, se si sta utilizzando un computer Apple:
https://docs.docker.com/desktop/setup/install/mac-install/

Successivamente si deve configurare tutto e avviare i container tramite la riga su terminale:
docker-compose up -d

Una volta avviati i container si deve accedere da browser al seguente link:
http://localhost:8080
con le credenziali di deafult.

Una volta entrato in questo sito per poter procedere si deve creare un tenant e aggiungere un nuovo utente per poi poter creare dispositivi/dashboard e inviare allarmi e notifiche.

## Collaboratori
- Martina Filice
- Corinne D'Elia

## Struttura del progetto
- docker-compose.yml — Configurazione per ThingsBoard e PostgreSQL
- dashboards/ —  File JSON delle dashboard
- README.md — Documentazione del progetto
- CO2_Adeunis - Dataset contenente i dati di CO2 riguardante 10 stanze a cui è associato il Timestamp e Data e ora
- ground_plan_sensors.jpg - Piantina delle stanze
- tb_decrypt_service_users_only.py - Servizio per decifrare la telemetria cifrata dei device su ThingsBoard
- cartella SvolgimentoProgetto
- cartella Spiegazioni ed Istruzioni

## Note:
- Il progetto è sviluppato con l'utilizzo di Docker Desktop come applicazione e ci si collega tramite interfaccia web a ThingsBoard
- Per lavorare in gruppo, i file vengono condivisi su GitHub.
- Per importare dati/dispositivi tra ambienti diversi si usano le funzioni di export/import di ThingsBoard
- Nella piattaforma viene utilizzato HTML per creare un grafico con bottone per accedere ai dati e l'aggiunta di email e password per verificare l'autenticazione
- Viene utilizzato python per gli script che servono per mandare i dati cifrati ai dispositivi e poi decifrare i dati e rimandarli a ThingsBoard per visualizzarli tramite i grafici
- Come algoritmo di routing viene utilizzato AODV, con i relativi messaggi di Route Request e Reply, per mettere in comunicazione le varie stanze in base alla cartina 
