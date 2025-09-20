#!/bin/bash

#Inserire il token dell'amministratore
TOKEN="eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJmbWFydHkyMzA4QGdtYWlsLmNvbSIsInVzZXJJZCI6IjE1OTU2MTEwLTZiZDYtMTFmMC05N2U1LWMxMWFiMWIzN2IxMyIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiODdkMjAwMjctYTM2My00ODNjLTk5OTMtYWUxZjM3NDk4OTA0IiwiZXhwIjoxNzU4MTMxNzgxLCJpc3MiOiJ0aGluZ3Nib2FyZC5pbyIsImlhdCI6MTc1ODEyMjc4MSwiZmlyc3ROYW1lIjoiTWFydGluYSIsImxhc3ROYW1lIjoiRmlsaWNlIiwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6IjFjMDRhZDQwLTZiZDUtMTFmMC05N2U1LWMxMWFiMWIzN2IxMyIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.dvXavzCE5431Me6QiagNiPOJEn3FpFanW0m-pYboXxbZ93fTpwXx28kEv57DC9VttIHH1yS0ud1u2OP9Gf3X7w"
THINGSBOARD_URL="http://localhost:8080"

#Recupera tutti gli ID dei dispositivi
echo "📤 Chiamata API per ottenere i dispositivi:"
response=$(curl -s -X GET "$THINGSBOARD_URL/api/tenant/devices?pageSize=1000&page=0" \
  -H "X-Authorization: Bearer $TOKEN")

echo "$response" | jq . 

device_ids=$(echo "$response" | jq -r '.data[].id.id')

#Timestamp
start_ts=$(($(date +%s)*1000))
end_ts=$((start_ts + 600000))  #+10 minuti

#Valore fittizio della media (simulazione)
media_calcolata=500

#Loop su ogni dispositivo
for device_id in $device_ids; do
  echo "📡 Controllo per dispositivo: $device_id (media: $media_calcolata)"

    if (( media_calcolata < 350 )); then
      tipo_allarme="low_average"
      severity="WARNING"
      dettaglio="Below minimum threshold"

    elif (( media_calcolata > 600 )); then
      tipo_allarme="high_average"
      severity="CRITICAL"
      dettaglio="Above maximum threshold"

    else
      tipo_allarme="average_in_range"
      severity="MINOR"
      dettaglio="Average within acceptable range"
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
    echo ✅ Alarm '$tipo_allarme' successfully created for $device_id
  else
    echo "❌ Errore HTTP $response per $device_id"
  fi
done
