#!/bin/bash
# usage: get.sh outname url [extra curl args...]
D=/private/tmp/claude-501/-Users-soodoku-Documents-GitHub-quota-representation/e4e84a77-95f7-4cd7-9092-72d59b858bd6/scratchpad/national
name=$1; out=$D/raw/$1; url=$2; shift 2
sleep 2
code=$(curl -sS -L --max-time 60 --socks5-hostname localhost:1080 -A "Mozilla/5.0 (Macintosh) research-survey" -c $D/cookies.txt -b $D/cookies.txt -o "$out" -w "%{http_code} %{content_type} %{size_download}" "$@" "$url")
sha=$(shasum -a 256 "$out" 2>/dev/null | cut -d' ' -f1)
echo -e "$(date -u +%FT%TZ)\t$url\t$*\t$code\t$sha\t$name" >> $D/log.tsv
echo "$code -> $out"
