#!/bin/bash

#Inserire il token dell'amministratore
TOKEN="eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJmbWFydHkyMzA4QGdtYWlsLmNvbSIsInVzZXJJZCI6IjE1OTU2MTEwLTZiZDYtMTFmMC05N2U1LWMxMWFiMWIzN2IxMyIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiZWQ0OTkyMWEtY2NhMy00ZjZiLTg2ZGItYmU4Y2QzYzFhYzg3IiwiZXhwIjoxNzU2MzkwNDE3LCJpc3MiOiJ0aGluZ3Nib2FyZC5pbyIsImlhdCI6MTc1NjM4MTQxNywiZmlyc3ROYW1lIjoiTWFydGluYSIsImxhc3ROYW1lIjoiRmlsaWNlIiwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6IjFjMDRhZDQwLTZiZDUtMTFmMC05N2U1LWMxMWFiMWIzN2IxMyIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.DstADn7n04I0nlIaFidujU_ADwNwZpwwmCZW0rxbd2HJNO47sVjrO0j3k9zJFt9-ayGuOOvpZNMioMdJQcSv3A"

THINGSBOARD_URL="http://localhost:8080"

#Recupera tutti gli ID dei dispositivi
device_ids=$(curl -s -X GET "$THINGSBOARD_URL/api/tenant/devices?pageSize=1000&page=0" \
  -H "X-Authorization: Bearer $TOKEN" | jq -r '.data[].id.id')

#Timestamp
start_ts=$(($(date +%s)*1000))
end_ts=$((start_ts + 600000))  # +10 minuti

#Loop su ogni dispositivo
for device_id in $device_ids; do
  echo "🔔 Creazione allarme per dispositivo: $device_id"

    json=$(jq -n \
    --arg id "$device_id" \
    --argjson startTs "$start_ts" \
    --argjson endTs "$end_ts" \
    '{
      originator: {
        entityType: "DEVICE",
        id: $id
      },
      type: "media_alta",
      severity: "CRITICAL",
      status: "ACTIVE_UNACK",
      startTs: $startTs,
      endTs: $endTs,
      details: {
        media_calcolata: 450,
        intervallo: "Generato da script"
      }
    }')

  #Invio dell'allarme
  response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$THINGSBOARD_URL/api/alarm" \
    -H "Content-Type: application/json" \
    -H "X-Authorization: Bearer $TOKEN" \
    -d "$json")

  if [[ "$response" == "200" || "$response" == "201" ]]; then
    echo "✅ Allarme creato con successo"
  else
    echo "❌ Errore HTTP $response"
  fi
done