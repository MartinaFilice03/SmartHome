# SmartHome
Progetto IoT con ThingsBoard e Docker

Progetto universitario realizzato con [ThingsBoard](https://thingsboard.io/) e Docker per il monitoraggio di dispositivi IoT.

## Tecnologie utilizzate

- ThingsBoard CE (Community Edition)
- Docker & Docker Compose
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

## Note:
- Il progetto è sviluppato con l'utilizzo di Docker Desktop come applicazione e ci si collega tramite interfaccia web a ThingsBoard
- Per lavorare in gruppo, i file vengono condivisi su GitHub.
- Per importare dati/dispositivi tra ambienti diversi si usano le funzioni di export/import di ThingsBoard
