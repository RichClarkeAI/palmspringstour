# Palm Springs Mid-Century Architecture Tour

Mobile-friendly self-guided tour app for Palm Springs mid-century modern architecture.

## Features

- **Mobile-first design** - Large touch targets, smooth animations
- **Progress tracking** - Remembers which homes you've visited
- **Google Maps integration** - One-tap navigation to each home
- **Audio guide** - Play narration at each stop
- **Photo slideshow** - Browse photos with captions
- **Offline-capable** - Works with local content

## Getting Started

### Local Development

1. Start a local server:
   ```bash
   cd ~/clawd/tools/palm-springs-tour
   python3 -m http.server 8000
   ```

2. Open in browser: `http://localhost:8000`

### Add Content

**Photos:** Add images to `images/` directory and update `data/homes.json`:

```json
"photos": ["images/photo1.jpg", "images/photo2.jpg"]
```

**Audio:** Add MP3 files to `audio/` directory:

```json
"audioUrl": "audio/narration.mp3"
```

## Tour Stops

The tour includes 10 iconic Palm Springs mid-century modern homes:

1. **Palm Springs Visitor Center** (Albert Frey, 1965) - Former Tramway Gas Station
2. **Kaufmann Residence** (Richard Neutra, 1946) - Most famous PS home
3. **Swiss Miss Houses** (Charles DuBois, 1960) - A-frame Instagram favorites
4. **Edris Residence** (E. Stewart Williams, 1954) - Desert modernism at its finest
5. **Elvis Honeymoon House** (Palmer & Krisel, 1960) - Where Elvis & Priscilla honeymooned
6. **Frank Sinatra Twin Palms Estate** (E. Stewart Williams, 1947) - Rat Pack headquarters
7. **Grace Lewis Miller Residence** (Richard Neutra, 1937) - Neutra's early masterpiece
8. **Dr. Franz Alexander Residence** (Walter S. White, 1956) - Experimental design
9. **Dinah Shore Residence** (Donald Wexler, 1964) - Now Leonardo DiCaprio's home
10. **Steel Houses** (Wexler & Harrison, 1960) - Prefab steel innovations

## Adding Content

### Audio Files (✓ COMPLETE)
Audio narration has been generated for all 10 homes using TTS. Files are in `audio/` directory.

### Photos (⚠️ NEEDS IMAGES)
Images are NOT yet downloaded. To add photos:

1. See `IMAGE_SOURCES.md` for where to find images for each home
2. Download 10 images per home (exterior + interiors/details)
3. Name files: `home-name-1.jpg`, `home-name-2.jpg`, etc.
4. Place in `images/` folder
5. Or use the helper script: `./download_images.sh urls.txt home-id`

The app gracefully handles missing images with placeholder icons.

## Tech Stack

- Vanilla JavaScript (no frameworks)
- CSS3 with custom properties
- HTML5 semantic markup
- LocalStorage for progress tracking
- Google Maps deep links

## Design

Color palette inspired by Palm Springs desert modernism:
- Terracotta: #C17767
- Sage: #9CAF88
- Cream: #F5F1E8

Fonts:
- Playfair Display (headings)
- Josefin Sans (body)

## Browser Support

- Mobile Safari (iOS 12+)
- Chrome Mobile (Android)
- Modern desktop browsers
