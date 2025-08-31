## Simulazione Invio Dati a ThingsBoard
- Questo progetto contiene uno script Python che simula la generazione, cifratura e invio di dati a ThingsBoard, una piattaforma IoT open-source.

## Come eseguire lo script
Requisiti
- Python 3.10 o superiore
- Un'istanza attiva di ThingsBoard (locale o cloud)
- Il Device Access Token (preso dal pannello del dispositivo su ThingsBoard)
- Un ambiente virtuale Python (consigliato)

## Passaggi per l’esecuzione
- Su Windows:
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  python send_data.py
  
- Su Linux/macOS:
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python send_data.py

## Note importanti
- Se non hai un file requirements.txt, puoi installare manualmente le librerie necessarie:
  pip install eciespy requests
- Lo script invia un dato cifrato a ThingsBoard usando una chiave pubblica ECC.
- Devi modificare lo script per inserire il tuo access token nel punto indicato.

## File principali da configurare
- send_data.py → contiene lo script principale per cifrare e inviare i dati.
- requirements.txt → elenca le librerie Python necessarie (opzionale ma utile).

## Output atteso
Una volta avviato lo script:
- I dati cifrati verranno inviati a ThingsBoard.
- Potrai vederli nella telemetria del dispositivo, in formato cifrato.
- Gli utenti autorizzati potranno richiedere la decifratura e visualizzazione dei dati. 
