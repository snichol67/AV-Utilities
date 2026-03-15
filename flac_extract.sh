ffprobe -v error -print_format json -show_chapters "C1_t02.mkv" > Zurich.json

i=2
jq -c '.chapters[]' A1_t00.json | while read -r row; do
  Echo $row
  start=$(echo "$row" | jq -r '.start_time')
  end=$(echo "$row" | jq -r '.end_time')
  title=$(echo "$row" | jq -r '.tags.title // empty')
  printf -v num "%02d" "$i"
  out="${num}-SABB_2011.flac"
  echo "→ Creating $out"
  ffmpeg -hide_banner -v error -i "A1_t00.mkv" -ss "$start" -to "$end" -map 0:a:0 -vn -c:a flac -y "$out"
  ((i++))
done

i=1
jq -c '.chapters[]' A1_t00.json | while read -r row; do
  Echo $row
  start=$(echo "$row" | jq -r '.start_time')
  end=$(echo "$row" | jq -r '.end_time')
  title=$(echo "$row" | jq -r '.tags.title // empty')
  printf -v num "%02d" "$i"
  Echo "start: $start"
  Echo "end: $end"
  out="${num}-SABB_2011.flac"
  echo "Creating $out"

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
ffmpeg -hide_banner -v error -i "/Volumes/Archives/Movies/test/WYWH-1975-t00.mkv" -ss "0.000000" -to "814.814000" -map 0:a:0 -vn -c:a flac -y "test.flac"
