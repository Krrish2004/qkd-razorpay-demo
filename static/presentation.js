// QKD-Razorpay Presentation JavaScript

// Core variables
let currentSlide = 1;
const totalSlides = 10;
let isAnimating = false;

// DOM Elements
const slidesContainer = document.getElementById('slidesContainer');
const slides = document.querySelectorAll('.slide');
const prevBtn = document.getElementById('prevSlide');
const nextBtn = document.getElementById('nextSlide');
const slideIndicator = document.getElementById('slideIndicator');

// Initialize the presentation
document.addEventListener('DOMContentLoaded', () => {
    // Set up the first slide
    setupSlides();
    
    // Add event listeners
    prevBtn.addEventListener('click', prevSlide);
    nextBtn.addEventListener('click', nextSlide);
    
    // Add keyboard navigation
    document.addEventListener('keydown', handleKeyNavigation);
    
    // Add touch/swipe navigation
    setupTouchNavigation();
    
    // Add background starfield effect
    createStarfield();
});

// Set up the initial slide state
function setupSlides() {
    // Hide all slides
    slides.forEach(slide => {
        slide.classList.remove('active');
    });
    
    // Show the first slide
    showSlide(currentSlide);
    
    // Update indicator
    updateSlideIndicator();
}

// Show a specific slide
function showSlide(slideNumber) {
    if (isAnimating) return;
    
    // Mark as animating
    isAnimating = true;
    
    // Hide all slides
    slides.forEach(slide => {
        slide.classList.remove('active');
    });
    
    // Show requested slide
    const targetSlide = document.getElementById(`slide${slideNumber}`);
    if (targetSlide) {
        targetSlide.classList.add('active');
    }
    
    // Update current slide number
    currentSlide = slideNumber;
    
    // Update indicator
    updateSlideIndicator();
    
    // Allow next animation after transition completes
    setTimeout(() => {
        isAnimating = false;
    }, 800);
}

// Update the slide indicator
function updateSlideIndicator() {
    slideIndicator.textContent = `${currentSlide} / ${totalSlides}`;
}

// Navigate to previous slide
function prevSlide() {
    if (currentSlide > 1) {
        showSlide(currentSlide - 1);
    }
}

// Navigate to next slide
function nextSlide() {
    if (currentSlide < totalSlides) {
        showSlide(currentSlide + 1);
    }
}

// Handle keyboard navigation
function handleKeyNavigation(e) {
    switch (e.key) {
        case 'ArrowLeft':
        case 'ArrowUp':
            prevSlide();
            break;
        case 'ArrowRight':
        case 'ArrowDown':
        case ' ': // Spacebar
            nextSlide();
            break;
        case 'Home':
            showSlide(1);
            break;
        case 'End':
            showSlide(totalSlides);
            break;
        case 'Escape':
            window.location.href = '/';
            break;
    }
}

// Set up touch/swipe navigation
function setupTouchNavigation() {
    let touchstartX = 0;
    let touchendX = 0;
    
    const handleSwipe = () => {
        const threshold = 100; // Min px traveled to count as swipe
        if (touchendX < touchstartX - threshold) {
            // Swipe left, go to next slide
            nextSlide();
        }
        if (touchendX > touchstartX + threshold) {
            // Swipe right, go to previous slide
            prevSlide();
        }
    };
    
    document.addEventListener('touchstart', e => {
        touchstartX = e.changedTouches[0].screenX;
    });
    
    document.addEventListener('touchend', e => {
        touchendX = e.changedTouches[0].screenX;
        handleSwipe();
    });
}

// Create starfield background effect
function createStarfield() {
    const wrapper = document.querySelector('.presentation-wrapper');
    
    // Create starfield container
    const starfield = document.createElement('div');
    starfield.classList.add('starfield');
    wrapper.appendChild(starfield);
    
    // Add stars
    const starsCount = Math.floor(window.innerWidth / 4);
    
    for (let i = 0; i < starsCount; i++) {
        createStar(starfield);
    }
    
    // Add CSS for starfield
    const style = document.createElement('style');
    style.textContent = `
        .starfield {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            overflow: hidden;
        }
        
        .star {
            position: absolute;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 50%;
            opacity: 0;
            animation-name: twinkle;
            animation-iteration-count: infinite;
            animation-direction: alternate;
        }
        
        @keyframes twinkle {
            0% {
                opacity: 0;
                transform: scale(0.5);
            }
            100% {
                opacity: 1;
                transform: scale(1);
            }
        }
    `;
    document.head.appendChild(style);
}

// Create an individual star for the starfield
function createStar(starfield) {
    const star = document.createElement('div');
    star.classList.add('star');
    
    // Random position
    const x = Math.random() * 100;
    const y = Math.random() * 100;
    
    // Random size (0.5px to 2.5px)
    const size = 0.5 + Math.random() * 2;
    
    // Random animation duration (1s to 5s)
    const duration = 1 + Math.random() * 4;
    
    // Random animation delay
    const delay = Math.random() * 5;
    
    // Apply styles
    star.style.left = `${x}%`;
    star.style.top = `${y}%`;
    star.style.width = `${size}px`;
    star.style.height = `${size}px`;
    star.style.animationDuration = `${duration}s`;
    star.style.animationDelay = `${delay}s`;
    
    // Add blue tint to some stars
    if (Math.random() > 0.7) {
        star.style.backgroundColor = 'rgba(0, 113, 227, 0.8)';
    }
    
    starfield.appendChild(star);
}

// Progress bar animation when a slide becomes active
function animateProgressBars() {
    const activeSlide = document.querySelector('.slide.active');
    if (!activeSlide) return;
    
    const progressBars = activeSlide.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const target = bar.getAttribute('data-progress') || '100';
        bar.style.width = `${target}%`;
    });
}

// Observe slide changes to trigger animations
const slideObserver = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
        if (mutation.attributeName === 'class') {
            const targetElement = mutation.target;
            if (targetElement.classList.contains('active') && targetElement.classList.contains('slide')) {
                // Trigger animations when a slide becomes active
                animateProgressBars();
            }
        }
    });
});

// Start observing slides
slides.forEach(slide => {
    slideObserver.observe(slide, { attributes: true });
}); 