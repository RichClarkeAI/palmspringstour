// Palm Springs Architecture Tour App

let homesData = [];
let currentHomeIndex = 0;
let currentPhotoIndex = 0;
let visitedHomes = new Set();
let audioElement = null;
let isPlaying = false;

// DOM Elements
const homeListEl = document.getElementById('home-list');
const modalEl = document.getElementById('modal');
const modalCloseEl = document.getElementById('modal-close');
const slideshowImage = document.getElementById('slideshow-image');
const prevPhotoBtn = document.getElementById('prev-photo');
const nextPhotoBtn = document.getElementById('next-photo');
const currentPhotoEl = document.getElementById('current-photo');
const totalPhotosEl = document.getElementById('total-photos');
const modalTitle = document.getElementById('modal-title');
const modalArchitect = document.getElementById('modal-architect');
const modalCaption = document.getElementById('modal-caption');
const playBtn = document.getElementById('play-btn');
const playIcon = document.getElementById('play-icon');
const pauseIcon = document.getElementById('pause-icon');
const progressBar = document.getElementById('progress-bar');
const progressSlider = document.getElementById('progress-slider');
const timeDisplay = document.getElementById('time-display');
const navLinkBtn = document.getElementById('nav-link');
const nextStopBtn = document.getElementById('next-stop-btn');
const visitedCountEl = document.getElementById('visited-count');
const totalCountEl = document.getElementById('total-count');

// Initialize app
async function init() {
    try {
        const response = await fetch('data/homes.json');
        const data = await response.json();
        homesData = data.homes;
        
        // Load visited state from localStorage
        loadVisitedState();
        
        // Render home cards
        renderHomeCards();
        
        // Update progress counter
        updateProgressCounter();
        
        // Setup event listeners
        setupEventListeners();
        
    } catch (error) {
        console.error('Error loading homes data:', error);
        homeListEl.innerHTML = '<p style="text-align:center;padding:40px;color:var(--charcoal-light)">Error loading tour data. Please refresh.</p>';
    }
}

function renderHomeCards() {
    homeListEl.innerHTML = homesData.map((home, index) => `
        <div class="home-card ${visitedHomes.has(home.id) ? 'visited' : ''}" data-index="${index}">
            <div class="card-thumbnail">
                ${home.photos[0] ? 
                    `<img src="${home.photos[0]}" alt="${home.name}" style="width:100%;height:100%;object-fit:cover" onerror="this.style.display='none'">` : 
                    '🏠'}
            </div>
            <div class="card-content">
                <h2>${home.name}</h2>
                <div class="card-meta">
                    <span>
                        <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16">
                            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                        </svg>
                        ${home.address}
                    </span>
                    <span>
                        <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16">
                            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z"/>
                        </svg>
                        ${home.architect}, ${home.year}
                    </span>
                </div>
                <div class="card-actions">
                    <button class="btn btn-navigate" onclick="navigateToHome(${index}, event)">
                        <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
                            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                        </svg>
                        Navigate
                    </button>
                    <button class="btn btn-arrived" onclick="openModal(${index}, event)">
                        Arrived
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

function setupEventListeners() {
    // Modal close
    modalCloseEl.addEventListener('click', closeModal);
    modalEl.addEventListener('click', (e) => {
        if (e.target === modalEl) closeModal();
    });
    
    // Photo navigation
    prevPhotoBtn.addEventListener('click', () => changePhoto(-1));
    nextPhotoBtn.addEventListener('click', () => changePhoto(1));
    
    // Audio controls
    playBtn.addEventListener('click', toggleAudio);
    progressSlider.addEventListener('input', seekAudio);
    
    // Next stop button
    nextStopBtn.addEventListener('click', goToNextStop);
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (!modalEl.classList.contains('active')) return;
        
        if (e.key === 'Escape') closeModal();
        if (e.key === 'ArrowLeft') changePhoto(-1);
        if (e.key === 'ArrowRight') changePhoto(1);
    });
}

function navigateToHome(index, event) {
    event.stopPropagation();
    const home = homesData[index];
    const encodedAddress = encodeURIComponent(home.address);
    const mapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${encodedAddress}`;
    window.open(mapsUrl, '_blank');
}

function openModal(index, event) {
    if (event) event.stopPropagation();
    
    currentHomeIndex = index;
    currentPhotoIndex = 0;
    const home = homesData[index];
    
    // Update modal content
    modalTitle.textContent = home.name;
    modalArchitect.textContent = `${home.architect}, ${home.year}`;
    modalCaption.textContent = home.caption;
    
    // Update navigation link
    const encodedAddress = encodeURIComponent(home.address);
    navLinkBtn.href = `https://www.google.com/maps/dir/?api=1&destination=${encodedAddress}`;
    
    // Setup photos
    totalPhotosEl.textContent = home.photos.length;
    updatePhotoDisplay();
    
    // Setup audio
    setupAudio(home.audioUrl);
    
    // Update next stop button
    if (index >= homesData.length - 1) {
        nextStopBtn.disabled = true;
        nextStopBtn.textContent = 'Tour Complete!';
    } else {
        nextStopBtn.disabled = false;
        nextStopBtn.innerHTML = `Next Stop <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"/></svg>`;
    }
    
    // Mark as visited
    markAsVisited(home.id);
    
    // Show modal
    modalEl.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    modalEl.classList.remove('active');
    document.body.style.overflow = '';
    
    // Stop audio
    if (audioElement) {
        audioElement.pause();
        isPlaying = false;
        updatePlayButton();
    }
}

function updatePhotoDisplay() {
    const home = homesData[currentHomeIndex];
    const photoPath = home.photos[currentPhotoIndex];
    
    slideshowImage.src = photoPath;
    slideshowImage.alt = `${home.name} photo ${currentPhotoIndex + 1}`;
    currentPhotoEl.textContent = currentPhotoIndex + 1;
    
    // Handle image load errors
    slideshowImage.onerror = function() {
        this.style.background = 'linear-gradient(135deg, var(--sage) 0%, var(--sage-dark) 100%)';
        this.style.height = '300px';
        this.src = 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="50" x="50" text-anchor="middle" font-size="40">🏠</text></svg>');
    };
}

function changePhoto(direction) {
    const home = homesData[currentHomeIndex];
    currentPhotoIndex += direction;
    
    if (currentPhotoIndex < 0) currentPhotoIndex = home.photos.length - 1;
    if (currentPhotoIndex >= home.photos.length) currentPhotoIndex = 0;
    
    updatePhotoDisplay();
}

function setupAudio(audioUrl) {
    // Clean up previous audio
    if (audioElement) {
        audioElement.pause();
        audioElement = null;
    }

    // Create new audio element
    audioElement = new Audio(audioUrl);
    isPlaying = false;
    updatePlayButton();

    // Reset play button state from any previous error
    playBtn.disabled = false;
    playBtn.style.opacity = '1';

    // Reset progress
    progressBar.style.width = '0%';
    progressSlider.value = 0;
    timeDisplay.textContent = '0:00';

    // Audio event listeners
    audioElement.addEventListener('loadedmetadata', () => {
        timeDisplay.textContent = formatTime(audioElement.duration);
    });

    audioElement.addEventListener('timeupdate', () => {
        const progress = (audioElement.currentTime / audioElement.duration) * 100;
        progressBar.style.width = progress + '%';
        progressSlider.value = progress;
        timeDisplay.textContent = formatTime(audioElement.currentTime);
    });

    audioElement.addEventListener('ended', () => {
        isPlaying = false;
        updatePlayButton();
    });

    audioElement.addEventListener('error', () => {
        console.log('Audio not available for this stop');
        timeDisplay.textContent = 'No audio';
        playBtn.style.opacity = '0.5';
        playBtn.disabled = true;
    });
}

function toggleAudio() {
    if (!audioElement) return;

    if (isPlaying) {
        audioElement.pause();
        isPlaying = false;
        updatePlayButton();
    } else {
        audioElement.play().then(() => {
            isPlaying = true;
            updatePlayButton();
        }).catch(e => {
            console.log('Audio playback failed:', e);
            isPlaying = false;
            updatePlayButton();
        });
    }
}

function updatePlayButton() {
    playIcon.style.display = isPlaying ? 'none' : 'block';
    pauseIcon.style.display = isPlaying ? 'block' : 'none';
}

function seekAudio(e) {
    if (!audioElement || !audioElement.duration) return;
    
    const seekTime = (e.target.value / 100) * audioElement.duration;
    audioElement.currentTime = seekTime;
}

function formatTime(seconds) {
    if (!seconds || isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function markAsVisited(homeId) {
    visitedHomes.add(homeId);
    saveVisitedState();
    updateProgressCounter();
    
    // Update card styling
    const cards = document.querySelectorAll('.home-card');
    cards.forEach(card => {
        const index = parseInt(card.dataset.index);
        if (homesData[index].id === homeId) {
            card.classList.add('visited');
        }
    });
}

function goToNextStop() {
    if (currentHomeIndex < homesData.length - 1) {
        openModal(currentHomeIndex + 1);
    }
}

function loadVisitedState() {
    const saved = localStorage.getItem('ps-tour-visited');
    if (saved) {
        visitedHomes = new Set(JSON.parse(saved));
    }
}

function saveVisitedState() {
    localStorage.setItem('ps-tour-visited', JSON.stringify([...visitedHomes]));
}

function updateProgressCounter() {
    visitedCountEl.textContent = visitedHomes.size;
    totalCountEl.textContent = homesData.length;
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', init);
