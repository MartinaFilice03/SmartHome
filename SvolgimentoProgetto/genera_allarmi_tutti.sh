#!/bin/bash

#Inserire il token dell'amministratore
TOKEN="eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJmbWFydHkyMzA4QGdtYWlsLmNvbSIsInVzZXJJZCI6IjE1OTU2MTEwLTZiZDYtMTFmMC05N2U1LWMxMWFiMWIzN2IxMyIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiNmJkODk1ZTItNTRkNC00YjRjLWEzNzgtOGRhNTRiNDYyMTc0IiwiZXhwIjoxNzU2NjY5MzAxLCJpc3MiOiJ0aGluZ3Nib2FyZC5pbyIsImlhdCI6MTc1NjY2MDMwMSwiZmlyc3ROYW1lIjoiTWFydGluYSIsImxhc3ROYW1lIjoiRmlsaWNlIiwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6IjFjMDRhZDQwLTZiZDUtMTFmMC05N2U1LWMxMWFiMWIzN2IxMyIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.s5AXRrxPu6IP4v3gKJLhybpHl-_ombG83lF61Z5x474NZAwqPEdSpDDOcVc0vWhp-oSm36mGp2rIO-uGjj7I-Q"
THINGSBOARD_URL="http://localhost:8080"

#Recupera tutti gli ID dei dispositivi
echo "📤 Chiamata API per ottenere i dispositivi:"
response=$(curl -s -X GET "$THINGSBOARD_URL/api/tenant/devices?pageSize=1000&page=0" \
  -H "X-Authorization: Bearer $TOKEN")

echo "$response" | jq . 

device_ids=$(echo "$response" | jq -r '.data[].id.id')

#Timestamp
start_ts=$(($(date +%s)*1000))
end_ts=$((start_ts + 600000))  # +10 minuti

#Valore fittizio della media (simulazione)
media_calcolata=450

#Loop su ogni dispositivo
for device_id in $device_ids; do
  echo "📡 Controllo per dispositivo: $device_id (media: $media_calcolata)"

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

  response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$THINGSBOARD_URL/api/alarm" \
    -H "Content-Type: application/json" \
    -H "X-Authorization: Bearer $TOKEN" \
    -d "$json")

  if [[ "$response" == "200" || "$response" == "201" ]]; then
    echo "✅ Allarme '$tipo_allarme' creato con successo per $device_id"
  else
    echo "❌ Errore HTTP $response per $device_id"
  fi
done
