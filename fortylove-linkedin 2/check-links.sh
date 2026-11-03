#!/usr/bin/env bash
# Проверяет все ссылки из plan.json: код ответа и Content-Type.
# Запуск: bash check-links.sh
set -u
urls=$(python3 -c "
import json
p=json.load(open('plan.json'))
for post in p['posts']:
    for a in post['assets']:
        print(a['image']['url'])
")
total=0; ok=0
while read -r u; do
  [ -z "$u" ] && continue
  total=$((total+1))
  line=$(curl -sI -m 20 "$u" | tr -d '\r')
  code=$(printf '%s\n' "$line" | awk 'NR==1{print $2}')
  ctype=$(printf '%s\n' "$line" | awk -F': ' 'tolower($1)=="content-type"{print $2}')
  if [ "$code" = "200" ]; then
    ok=$((ok+1))
  else
    echo "FAIL $code  $u"
  fi
done <<< "$urls"
echo "-----"
echo "200 OK: $ok из $total"
[ "$ok" = "$total" ] && echo "можно заливать в Buffer" || echo "сначала почини ссылки"
