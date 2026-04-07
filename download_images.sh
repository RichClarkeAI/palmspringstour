#!/bin/bash

# Image download helper script for Palm Springs Architecture Tour
# Usage: ./download_images.sh <url_file> <home_id>
# Example: ./download_images.sh visitor_center_urls.txt visitor-center

URL_FILE=$1
HOME_ID=$2
OUTPUT_DIR="images"

if [ $# -lt 2 ]; then
    echo "Usage: $0 <url_file> <home_id>"
    echo "Example: $0 visitor_center_urls.txt visitor-center"
    exit 1
fi

if [ ! -f "$URL_FILE" ]; then
    echo "Error: URL file '$URL_FILE' not found"
    exit 1
fi

# Read URLs and download with proper numbering
COUNTER=1
while IFS= read -r url; do
    # Skip empty lines and comments
    [ -z "$url" ] && continue
    [[ "$url" =~ ^# ]] && continue

    OUTPUT_FILE="${OUTPUT_DIR}/${HOME_ID}-${COUNTER}.jpg"
    echo "Downloading $COUNTER: $url"
    curl -s -L "$url" -o "$OUTPUT_FILE"

    # Check if download succeeded
    if [ $? -eq 0 ] && [ -f "$OUTPUT_FILE" ]; then
        # Optimize image if ImageMagick is available
        if command -v convert &> /dev/null; then
            convert "$OUTPUT_FILE" -resize 1200x1200\> -quality 85 "$OUTPUT_FILE" 2>/dev/null
        fi
        echo "  ✓ Saved to $OUTPUT_FILE"
    else
        echo "  ✗ Failed to download"
    fi

    ((COUNTER++))

    # Stop after 10 images
    if [ $COUNTER -gt 10 ]; then
        echo "Downloaded maximum 10 images"
        break
    fi

    # Small delay between downloads
    sleep 0.5
done < "$URL_FILE"

echo "Downloaded $((COUNTER-1)) images for $HOME_ID"
