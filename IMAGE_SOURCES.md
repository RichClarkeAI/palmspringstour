# Image Sources for Palm Springs Architecture Tour

This document lists where to find images for each home in the tour.

## Image Sources (Fair Use for Educational Purposes)

### 1. Palm Springs Visitor Center (Albert Frey, 1965)
**Search Terms:** "Palm Springs Visitor Center", "Tramway Gas Station Albert Frey"

Good sources:
- Wikipedia: https://en.wikipedia.org/wiki/Tramway_Gas_Station
- Palm Springs Official Site: https://www.visitpalmsprings.com
- Wikimedia Commons (public domain)
- Architectural photography sites

**Recommended Images:**
- Exterior with hyperbolic paraboloid roof (1-3)
- Interior visitor center (4-7)
- Historical photos as gas station (8-9)
- Night shots (10)

### 2. Kaufmann Residence (Richard Neutra, 1946)
**Search Terms:** "Kaufmann Desert House Neutra", "Kaufmann Residence Palm Springs"

Good sources:
- Wikimedia Commons
- Architectural Digest archives
- Slim Aarons "Poolside Gossip" photo
- Neutra Foundation

**Recommended Images:**
- Famous exterior view (1)
- Pool and patio (2-3)
- Living room (4-5)
- Kitchen/dining (6-7)
- Bedroom (8)
- Historical photos (9-10)

### 3. Swiss Miss Houses (Charles DuBois, 1960)
**Search Terms:** "Swiss Miss Palm Springs", "Charles DuBois Palm Springs"

Good sources:
- Palm Springs Modern Committee
- Real estate listings (Zillow, Redfin)
- Instagram #palmspringsmidcentury
- Architecture blogs

**Recommended Images:**
- A-frame entryway (1-3)
- Street view showing multiple homes (4)
- Interior with peaked ceiling (5-7)
- Kitchen/living area (8-9)
- Patio/pool (10)

### 4. Edris Residence (E. Stewart Williams, 1954)
**Search Terms:** "Edris Residence Palm Springs", "E. Stewart Williams"

Good sources:
- Palm Springs Art Museum archives
- Architectural photography collections
- Historical society

### 5. Elvis Honeymoon House (Palmer & Krisel, 1960)
**Search Terms:** "Elvis Honeymoon House Palm Springs", "House of Tomorrow Palm Springs"

Good sources:
- House is a vacation rental with extensive online photos
- TripAdvisor
- Elvis Presley Enterprises
- Fan sites

### 6. Frank Sinatra Twin Palms Estate (E. Stewart Williams, 1947)
**Search Terms:** "Sinatra Twin Palms Estate", "Frank Sinatra Palm Springs house"

Good sources:
- Estate website and real estate listings
- Historical celebrity photo archives
- Life Magazine archives

### 7. Grace Lewis Miller Residence (Richard Neutra, 1937)
**Search Terms:** "Miller Residence Neutra Palm Springs"

Good sources:
- Neutra archives
- USC Architecture Library
- Historical preservation sites

### 8. Dr. Franz Alexander Residence (Walter S. White, 1956)
**Search Terms:** "Alexander Residence Walter White Palm Springs"

Good sources:
- Walter S. White archives
- Architecture school collections
- Modernism Week materials

### 9. Dinah Shore Residence (Donald Wexler, 1964)
**Search Terms:** "Dinah Shore house Palm Springs", "Leonardo DiCaprio Palm Springs"

Good sources:
- Architectural Digest
- Celebrity home features
- Wexler archives

### 10. Steel Houses (Donald Wexler & Richard Harrison, 1960)
**Search Terms:** "Wexler Steel Houses Palm Springs", "Alexander Steel Houses"

Good sources:
- Palm Springs Modern Committee
- Architecture documentaries
- Modernism Week tours
- Real estate listings

## How to Download Images

### Manual Method (Recommended)
1. Search for each home using the terms above
2. Download high-quality images (aim for 1200px width minimum)
3. Rename files with consistent naming: `home-name-1.jpg`, `home-name-2.jpg`, etc.
4. Place in `/images/` folder
5. Update `data/homes.json` if filenames differ

### Automated Method (if permitted)
```bash
# Using wget to download from a list of URLs
wget -i image_urls.txt -P images/

# Or using curl
xargs -n 1 curl -O < image_urls.txt
```

## Image Guidelines

- **File size:** Keep under 500KB each (compress if needed)
- **Format:** JPG for photos, PNG for graphics with transparency
- **Naming:** Use lowercase, hyphens, numbered 1-10
- **Content:** 
  - First image should be best exterior shot
  - Include interior, details, historical photos
  - Avoid watermarked images
  - Prefer high-resolution, well-lit photos

## Bulk Image Optimization

If images are too large, use ImageMagick:

```bash
# Resize and compress all images in folder
cd images
for img in *.jpg; do
  convert "$img" -resize 1200x1200\> -quality 85 "$img"
done
```

## Fair Use Note

Images used for educational purposes in a non-commercial tour app generally fall under fair use. Always:
- Use publicly available images
- Credit photographers when known
- Don't use watermarked or clearly copyrighted professional photos without permission
- Prefer historical/archival photos (often public domain)
