{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fswiss\fcharset0 Helvetica-Bold;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
{\*\listtable{\list\listtemplateid1\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{disc\}}{\leveltext\leveltemplateid1\'01\uc0\u8226 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid1}}
{\*\listoverridetable{\listoverride\listid1\listoverridecount0\ls1}}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Simulazione invio dati a ThingsBoard\
\
Questo progetto contiene uno script Python che simula la generazione, cifratura e invio di dati a ThingsBoard, una piattaforma IoT.\
\
## Come eseguire lo script\
\
Per simulare l'invio dei dati a ThingsBoard, segui questi passaggi:\
\
## Requisiti\
\
- Python 3.10 o superiore\
- Una connessione funzionante con ThingsBoard\
- Token del dispositivo su ThingsBoard\
- Ambiente virtuale Python (opzionale ma consigliato)\
\
---\
\
## Passaggi\
\
### Su Windows:\
\
```bash\
python -m venv venv\
venv\\Scripts\\activate\
pip install -r requirements.txt\
python send_data.py\
\
### Su Linux/MacOs\
\
python3 -m venv venv\
source venv/bin/activate\
pip install -r requirements.txt\
python send_data.py\
\
## Note\
\pard\pardeftab720\partightenfactor0
\cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Se non hai un file requirements.txt, puoi installare le librerie necessarie manualmente:\
\'93pip install eciespy requests\'94\
\
\pard\pardeftab720\sa240\partightenfactor0
\cf0 \strokec2 Lo script invier\'e0 un dato cifrato a ThingsBoard utilizzando la chiave pubblica ECC.\
Si deve inserire l'access token corretto del dispositivo all'interno dello script.\
\pard\pardeftab720\sa298\partightenfactor0
\cf0 \strokec2 ## File da configurare
\f1\b \
\pard\tx220\tx720\pardeftab720\li720\fi-720\sa240\partightenfactor0
\ls1\ilvl0
\f0\b0 \cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 send_data.py\strokec2 : contiene lo script di invio\
\ls1\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 requirements.txt\strokec2 : contiene le librerie necessarie\
\pard\pardeftab720\partightenfactor0
\cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 \
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 \
}