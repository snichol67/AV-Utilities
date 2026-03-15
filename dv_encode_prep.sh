#!/bin/bash

# ============================================================
# Dolby Vision → HDR10 prep script (v3.2 - stable UHD version)
# Requires: ffmpeg, dovi_tool, mkvmerge
# Produces: HandBrake-ready HDR10 MKV
# ============================================================

set -e

INPUT="$1"

if [[ -z "$INPUT" ]]; then
  echo "Usage: ./dv_encode_prep_v3.2.sh input.mkv"
  exit 1
fi

if [[ ! -f "$INPUT" ]]; then
  echo "ERROR: File not found: $INPUT"
  exit 1
fi

echo "=== Dolby Vision HDR10 Prep v3.2 ==="
echo "Input: $INPUT"
echo

# ------------------------------------------------------------
# Check dependencies
# ------------------------------------------------------------
for tool in ffmpeg ffprobe dovi_tool mkvmerge; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "ERROR: $tool not installed"
    exit 1
  fi
done

# ------------------------------------------------------------
# Safe filenames
# ------------------------------------------------------------
FILENAME="$(basename "$INPUT")"
BASENAME="${FILENAME%.*}"
SAFE_BASENAME=$(printf '%s' "$BASENAME" | sed 's/[^A-Za-z0-9._-]/_/g')

VIDEO_RAW="${SAFE_BASENAME}_video.hevc"
VIDEO_BL="${SAFE_BASENAME}_BL.hevc"
AUDIO_TMP="${SAFE_BASENAME}_audio.mkv"
SUBS_TMP="${SAFE_BASENAME}_subs.mkv"
FINAL_OUT="${SAFE_BASENAME}_HDR10_READY.mkv"

# ------------------------------------------------------------
# Detect Dolby Vision
# ------------------------------------------------------------
echo "=== Checking for Dolby Vision metadata ==="

DV_CHECK=$(ffprobe -v error -select_streams v:0 \
  -show_entries stream_side_data \
  -of default=noprint_wrappers=1 "$INPUT" 2>/dev/null || true)

if echo "$DV_CHECK" | grep -q "dv_profile"; then
  echo "Dolby Vision detected."
else
  echo "No Dolby Vision metadata found."
  echo "You can feed this file directly into HandBrake."
  exit 0
fi

# ------------------------------------------------------------
# Extract streams
# ------------------------------------------------------------
echo
echo "=== Extracting streams ==="

ffmpeg -y -fflags +genpts -i "$INPUT" \
  -map 0:v:0 -c:v copy -bsf:v hevc_mp4toannexb "$VIDEO_RAW" \
  -map 0:a? -c:a copy "$AUDIO_TMP" \
  -map 0:s? -c:s copy "$SUBS_TMP"

# ------------------------------------------------------------
# Remove DV metadata
# ------------------------------------------------------------
echo
echo "=== Removing Dolby Vision enhancement layer ==="

dovi_tool remove -i "$VIDEO_RAW" -o "$VIDEO_BL"

# ------------------------------------------------------------
# Detect frame rate
# ------------------------------------------------------------
echo
echo "=== Determining frame rate ==="

FPS=$(ffprobe -v error -select_streams v:0 \
  -show_entries stream=r_frame_rate \
  -of csv=p=0 "$INPUT" | awk -F/ '{printf "%.3f", $1/$2}')

echo "Detected FPS: $FPS"

# ------------------------------------------------------------
# Final remux using mkvmerge (correct for raw HEVC)
# ------------------------------------------------------------
echo
echo "=== Remuxing HDR10 MKV with mkvmerge ==="

mkvmerge -o "$FINAL_OUT" \
  --default-duration 0:${FPS}fps "$VIDEO_BL" \
  "$AUDIO_TMP" \
  "$SUBS_TMP"

# ------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------
echo
echo "=== Cleaning up temp files ==="

rm -f "$VIDEO_RAW" "$VIDEO_BL" "$AUDIO_TMP" "$SUBS_TMP"

echo
echo "=== DONE ==="
echo "HDR10 file ready for HandBrake:"
echo "$FINAL_OUT"
echo