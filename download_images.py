#!/usr/bin/env python3
"""Download images for Palm Springs Architecture Tour app from Wikimedia Commons and LOC."""
import os
import sys
import time
import json
import urllib.request
import urllib.parse
from PIL import Image

IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
os.makedirs(IMG_DIR, exist_ok=True)

def compress_image(path, max_size=1200, quality=80, max_bytes=500000):
    """Compress image if over max_bytes."""
    size = os.path.getsize(path)
    if size <= max_bytes:
        return
    img = Image.open(path)
    img.thumbnail((max_size, max_size))
    img.save(path, 'JPEG', quality=quality)
    print(f"  Compressed {os.path.basename(path)}: {size} -> {os.path.getsize(path)} bytes")

def download_file(url, dest):
    """Download a file, return True if valid JPEG."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PalmSpringsTourBot/1.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dest, 'wb') as f:
            f.write(data)
        # Verify it's a JPEG
        if len(data) < 5000:
            print(f"  SKIP {dest}: too small ({len(data)} bytes)")
            os.remove(dest)
            return False
        if not data[:3] == b'\xff\xd8\xff':
            print(f"  SKIP {dest}: not a JPEG")
            os.remove(dest)
            return False
        print(f"  Downloaded {dest}: {len(data)} bytes")
        return True
    except Exception as e:
        print(f"  ERROR downloading {url}: {e}")
        if os.path.exists(dest):
            os.remove(dest)
        return False

def get_wikimedia_category_files(category):
    """Get all files from a Wikimedia Commons category."""
    files = []
    url = f"https://commons.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:{urllib.parse.quote(category)}&cmtype=file&cmlimit=50&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PalmSpringsTourBot/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        for member in data.get('query', {}).get('categorymembers', []):
            files.append(member['title'])
    except Exception as e:
        print(f"  Error getting category {category}: {e}")
    return files

def get_wikimedia_image_urls(filenames, width=1280):
    """Get thumbnail URLs for Wikimedia files."""
    if not filenames:
        return {}
    titles = '|'.join(filenames)
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(titles)}&prop=imageinfo&iiprop=url&iiurlwidth={width}&format=json"
    results = {}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PalmSpringsTourBot/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        for page in data.get('query', {}).get('pages', {}).values():
            iis = page.get('imageinfo', [])
            if iis:
                ii = iis[0]
                thumb = ii.get('thumburl', ii.get('url'))
                orig = ii.get('url', '')
                title = page.get('title', '')
                # Skip TIFF files
                if orig.endswith('.tif') or orig.endswith('.tiff') or '.tif' in title.lower():
                    continue
                results[title] = thumb
    except Exception as e:
        print(f"  Error getting image URLs: {e}")
    return results

def get_wikipedia_page_images(page_title):
    """Get images used on a Wikipedia page."""
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(page_title)}&prop=images&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PalmSpringsTourBot/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        images = []
        for page in data.get('query', {}).get('pages', {}).values():
            for img in page.get('images', []):
                if img['title'].endswith(('.jpg', '.jpeg', '.png', '.JPG', '.JPEG')):
                    images.append(img['title'])
        return images
    except Exception as e:
        print(f"  Error getting page images: {e}")
        return []

def download_wikimedia_category(home_id, category, max_images=6):
    """Download images from a Wikimedia Commons category."""
    print(f"\n=== {home_id}: Searching Commons category '{category}' ===")
    files = get_wikimedia_category_files(category)
    if not files:
        print(f"  No files found in category")
        return 0
    
    # Filter out non-image files
    image_files = [f for f in files if any(f.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png'])]
    # Also filter out TIFF
    image_files = [f for f in image_files if '.tif' not in f.lower()]
    
    if not image_files:
        print(f"  No image files found")
        return 0
    
    print(f"  Found {len(image_files)} image files")
    urls = get_wikimedia_image_urls(image_files[:max_images])
    
    count = 0
    for title, url in urls.items():
        count += 1
        dest = os.path.join(IMG_DIR, f"{home_id}-{count}.jpg")
        if os.path.exists(dest):
            print(f"  SKIP {dest}: already exists")
            continue
        if download_file(url, dest):
            compress_image(dest)
        else:
            count -= 1
        time.sleep(0.5)
    
    return count

def download_wikipedia_images(home_id, page_title, max_images=3):
    """Download images from a Wikipedia page."""
    print(f"\n=== {home_id}: Searching Wikipedia page '{page_title}' ===")
    images = get_wikipedia_page_images(page_title)
    if not images:
        print(f"  No images found on page")
        return 0
    
    print(f"  Found {len(images)} images")
    urls = get_wikimedia_image_urls(images[:max_images])
    
    # Determine next number
    existing = [f for f in os.listdir(IMG_DIR) if f.startswith(home_id) and f.endswith('.jpg')]
    next_num = len(existing) + 1
    
    count = 0
    for title, url in urls.items():
        dest = os.path.join(IMG_DIR, f"{home_id}-{next_num + count}.jpg")
        if os.path.exists(dest):
            count += 1
            continue
        if download_file(url, dest):
            compress_image(dest)
            count += 1
        time.sleep(0.5)
    
    return count

def download_loc_image(home_id, item_id, resource_id, next_num):
    """Download image from Library of Congress."""
    print(f"\n=== {home_id}: Downloading LOC image {item_id} ===")
    url = f"https://www.loc.gov/item/{item_id}/?fo=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PalmSpringsTourBot/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        
        for resource in data.get('resources', []):
            for files_list in resource.get('files', []):
                for f in files_list:
                    img_url = f.get('url', '')
                    h = f.get('height', 0)
                    mime = f.get('mimetype', '')
                    if mime == 'image/jpeg' and h >= 700 and h <= 1500:
                        dest = os.path.join(IMG_DIR, f"{home_id}-{next_num}.jpg")
                        if download_file(img_url, dest):
                            compress_image(dest)
                            return 1
            # Try the image URL directly
            img_url = resource.get('image', '')
            if img_url and img_url.startswith('http'):
                # Convert gif thumbnail to jpg via IIIF
                dest = os.path.join(IMG_DIR, f"{home_id}-{next_num}.jpg")
                if download_file(img_url, dest):
                    compress_image(dest)
                    return 1
    except Exception as e:
        print(f"  Error with LOC: {e}")
    return 0

# === MAIN ===

results = {}

# 1. KAUFMANN - already have 1, need more
print("\n" + "="*60)
print("KAUFMANN DESERT HOUSE")
print("="*60)
count = download_wikimedia_category('kaufmann', 'Kaufman_Desert_House', 6)
# Also check Wikipedia page for additional images
count += download_wikipedia_images('kaufmann', 'Kaufmann_Desert_House', 3)
results['kaufmann'] = count + 1  # +1 for already downloaded

time.sleep(1)

# 2. SWISS MISS - no Wikimedia category, try different search
print("\n" + "="*60)
print("SWISS MISS")
print("="*60)
count = download_wikimedia_category('swiss-miss', 'Swiss_Miss_Houses', 6)
if count == 0:
    count = download_wikimedia_category('swiss-miss', 'Swiss_Miss_House', 6)
results['swiss-miss'] = count

time.sleep(1)

# 3. EDRIS RESIDENCE
print("\n" + "="*60)
print("EDRIS RESIDENCE")
print("="*60)
count = download_wikimedia_category('edris', 'Edris_Residence', 6)
if count == 0:
    count = download_wikimedia_category('edris', 'Edris_House', 6)
if count == 0:
    count = download_wikipedia_images('edris', 'Edris_Estate', 3)
results['edris'] = count

time.sleep(1)

# 4. ELVIS HONEYMOON - already have 2, need more
print("\n" + "="*60)
print("ELVIS HONEYMOON")
print("="*60)
count = download_wikimedia_category('elvis-honeymoon', 'House_of_Tomorrow_(Palm_Springs,_California)', 6)
if count == 0:
    count = download_wikimedia_category('elvis-honeymoon', 'Elvis_Presley_Honeymoon_House', 6)
# Already have 2 from Wikimedia and LOC
existing_elvis = len([f for f in os.listdir(IMG_DIR) if f.startswith('elvis-honeymoon') and f.endswith('.jpg')])
results['elvis-honeymoon'] = max(existing_elvis, count)

time.sleep(1)

# 5. SINATRA - already have 4
existing_sinatra = len([f for f in os.listdir(IMG_DIR) if f.startswith('sinatra') and f.endswith('.jpg')])
results['sinatra'] = existing_sinatra
print(f"\nSinatra: already have {existing_sinatra} images")

time.sleep(1)

# 6. MILLER RESIDENCE (Grace Lewis Miller / Neutra)
print("\n" + "="*60)
print("MILLER RESIDENCE")
print("="*60)
count = download_wikimedia_category('miller', 'Grace_Lewis_Miller_House', 6)
if count == 0:
    count = download_wikimedia_category('miller', 'Miller_House_(Palm_Springs)', 6)
if count == 0:
    count = download_wikipedia_images('miller', 'Grace_Lewis_Miller_House', 3)
results['miller'] = count

time.sleep(1)

# 7. ALEXANDER RESIDENCE (Walter White)
print("\n" + "="*60)
print("ALEXANDER RESIDENCE")
print("="*60)
count = download_wikimedia_category('alexander', 'Alexander_Residence_(Palm_Springs)', 6)
if count == 0:
    count = download_wikimedia_category('alexander', 'Walter_White_House', 6)
if count == 0:
    count = download_wikipedia_images('alexander', 'Alexander_Residence_(Palm_Springs,_California)', 3)
results['alexander'] = count

time.sleep(1)

# 8. DINAH SHORE RESIDENCE
print("\n" + "="*60)
print("DINAH SHORE RESIDENCE")
print("="*60)
count = download_wikimedia_category('dinah-shore', 'Dinah_Shore_House', 6)
if count == 0:
    count = download_wikimedia_category('dinah-shore', 'Dinah_Shore_Residence', 6)
if count == 0:
    count = download_wikipedia_images('dinah-shore', 'Dinah_Shore_(residence)', 3)
results['dinah-shore'] = count

time.sleep(1)

# 9. STEEL HOUSES (Wexler)
print("\n" + "="*60)
print("STEEL HOUSES (WEXLER)")
print("="*60)
count = download_wikimedia_category('steel-houses', 'Steel_Development_Houses', 6)
if count == 0:
    count = download_wikimedia_category('steel-houses', 'Wexler_Steel_Houses', 6)
if count == 0:
    count = download_wikipedia_images('steel-houses', 'Wexler_Steel_Houses', 3)
results['steel-houses'] = count

# === SUMMARY ===
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
total = 0
for home, count in sorted(results.items()):
    actual = len([f for f in os.listdir(IMG_DIR) if f.startswith(home) and f.endswith('.jpg')])
    print(f"  {home}: {actual} images")
    total += actual
print(f"\n  TOTAL: {total} images")

# List all files
print("\nAll files:")
for f in sorted(os.listdir(IMG_DIR)):
    if f.endswith('.jpg'):
        size = os.path.getsize(os.path.join(IMG_DIR, f))
        print(f"  {f}: {size:,} bytes")
