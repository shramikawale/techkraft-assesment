#!/bin/bash

LOG_FILE="$1"

if [[ -z "$LOG_FILE" ]]; then
  echo "Usage: $0 <nginx_log_file>"
  exit 1
fi

if [[ ! -f "$LOG_FILE" ]]; then
  echo "Error: Log file not found"
  exit 1
fi

TOTAL_REQUESTS=$(wc -l < "$LOG_FILE")
UNIQUE_IPS=$(awk '{print $1}' "$LOG_FILE" 2>/dev/null | sort | uniq | wc -l)

TOTAL_4XX=$(awk '$9 ~ /^4[0-9][0-9]$/' "$LOG_FILE" 2>/dev/null | wc -l)
TOTAL_5XX=$(awk '$9 ~ /^5[0-9][0-9]$/' "$LOG_FILE" 2>/dev/null | wc -l)

PCT_4XX=$(awk -v e=$TOTAL_4XX -v t=$TOTAL_REQUESTS 'BEGIN { if (t==0) print 0; else printf "%.2f", (e/t)*100 }')
PCT_5XX=$(awk -v e=$TOTAL_5XX -v t=$TOTAL_REQUESTS 'BEGIN { if (t==0) print 0; else printf "%.2f", (e/t)*100 }')

TOP_IPS=$(awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -10)

TOP_ENDPOINTS=$(awk -F\" '{print $2}' "$LOG_FILE" \
  | awk '{print $2}' \
  | sort | uniq -c | sort -nr | head -10)

echo "=== Nginx Log Analysis Report ==="
echo "Total Requests: $TOTAL_REQUESTS"
echo "Unique IPs: $UNIQUE_IPS"
echo "4xx Errors: $TOTAL_4XX ($PCT_4XX%)"
echo "5xx Errors: $TOTAL_5XX ($PCT_5XX%)"

echo ""
echo "Top 10 IPs:"
echo "$TOP_IPS" | awk '{printf "%d. %s %s requests\n", NR, $2, $1}'

echo ""
echo "Top 10 Endpoints:"
echo "$TOP_ENDPOINTS" | awk '{printf "%d. %s %s requests\n", NR, $2, $1}'
