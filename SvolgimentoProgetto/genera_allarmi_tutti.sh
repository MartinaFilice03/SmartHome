#!/bin/bash

#Token dell'amministratore
TOKEN="eyJhbGciOiJIUzUxMiJ9..."
THINGSBOARD_URL="http://localhost:8080"

#Recupera tutti gli ID dei dispositivi
echo "📤 Chiamata API per ottenere i dispositivi:"
response=$(curl -s -X GET "$THINGSBOARD_URL/api/tenant/devices?pageSize=1000&page=0" \
  -H "X-Authorization: Bearer $TOKEN")

echo "$response" | jq . #Stampa JSON formattato (debug)
device_ids=$(echo "$response" | jq -r '.data[].id.id')

#Finestra temporale allarme
start_ts=$(($(date +%s)*1000))
end_ts=$((start_ts + 600000)) 

#Valore medio simulato per la logica di allarme
media_calcolata=200

#Ciclo su ogni device
for device_id in $device_ids; do
  echo "📡 Controllo per dispositivo: $device_id (media: $media_calcolata)"

  #Selezione tipo/severità in base alla media
  if (( media_calcolata < 350 )); then
    tipo_allarme="media_bassa"
    severity="WARNING"
    dettaglio="Sotto la soglia minima"

  elif (( media_calcolata > 800 )); then
    tipo_allarme="media_alta"
    severity="CRITICAL"
    dettaglio="Oltre la soglia massima"

  else
    tipo_allarme="media_fuori_range"
    severity="MAJOR"
    dettaglio="Media fuori range accettabile"
  fi

  #Costruzione payload allarme 
  json=$(jq -n \
    --arg id "$device_id" \
    --arg type "$tipo_allarme" \
    --arg severity "$severity" \
    --arg detail "$dettaglio" \
    --argjson startTs "$start_ts" \
    --argjson endTs "$end_ts" \
    --argjson media "$media_calcolata" \
    '{
      originator: {
        entityType: "DEVICE",
        id: $id
      },
      type: $type,
      severity: $severity,
      status: "ACTIVE_UNACK",
      startTs: $startTs,
      endTs: $endTs,
      details: {
        media_calcolata: $media,
        intervallo: $detail
      }
    }')

  #Invio allarme
  response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$THINGSBOARD_URL/api/alarm" \
    -H "Content-Type: application/json" \
    -H "X-Authorization: Bearer $TOKEN" \
    -d "$json")

  #Esito
  if [[ "$response" == "200" || "$response" == "201" ]]; then
    echo "✅ Allarme '$tipo_allarme' creato con successo per $device_id"
  else
    echo "❌ Errore HTTP $response per $device_id"
  fi
done
