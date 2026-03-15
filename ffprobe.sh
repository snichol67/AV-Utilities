ffprobe -v error -print_format json -show_chapters "WYWH-LIVE-t05.mkv" > WYWH-LIVE-t05.json

i=2
jq -c '.chapters[]' WYWH-LIVE-t05.json | while read -r row; do
  Echo $row
  start=$(echo "$row" | jq -r '.start_time')
  end=$(echo "$row" | jq -r '.end_time')
  title=$(echo "$row" | jq -r '.tags.title // empty')
  printf -v num "%02d" "$i"
  out="LIVE-${num}-WYWH.flac"
  echo "→ Creating $out"
  ffmpeg -hide_banner -v error -i "WYWH-LIVE-t05.mkv" -ss "$start" -to "$end" \
         -map 0:a:0 -vn -c:a flac -y "$out"
  ((i++))
done

i=2
jq -c '.chapters[]' chapters.json | while read -r row; do
  Echo $row
  start=$(echo "$row" | jq -r '.start_time')
  end=$(echo "$row" | jq -r '.end_time')
  title=$(echo "$row" | jq -r '.tags.title // empty')
  printf -v num "%02d" "$i"
  out="SnakesArrows_${num}.flac"
  echo "→ Creating $out"
  ffmpeg -hide_banner -v error -i "title_t00.mkv" -ss "$start" -to "$end" \
         -map 0:a:0 -vn -c:a flac -y "$out"
  ((i++))
done

ffmpeg -hide_banner -v error -i "title_t00.mkv" -ss "start" -to "end" -map 0:a:0 -vn -c:a flac -y "outfile"