/* ==========================================================================
   AUTOZCRAVESTUDIO - CUSTOM CURSOR, PAGE TRANSITIONS & SCROLL ANIMATIONS
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Custom Automotive Cursor
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    const cursorFollower = document.createElement('div');
    cursorFollower.className = 'custom-cursor-follower';
    
    document.body.appendChild(cursor);
    document.body.appendChild(cursorFollower);

    let mouseX = -100, mouseY = -100;
    let followerX = -100, followerY = -100;

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        cursor.style.transform = `translate3d(${mouseX}px, ${mouseY}px, 0)`;
    });

    function animateFollower() {
        followerX += (mouseX - followerX) * 0.15;
        followerY += (mouseY - followerY) * 0.15;
        cursorFollower.style.transform = `translate3d(${followerX}px, ${followerY}px, 0)`;
        requestAnimationFrame(animateFollower);
    }
    animateFollower();

    // Hover interactive elements
    const hoverTargets = document.querySelectorAll('a, button, .interactive-card, .filter-btn, .ba-container, .hotspot');
    hoverTargets.forEach(target => {
        target.addEventListener('mouseenter', () => {
            cursor.classList.add('cursor-active');
            cursorFollower.classList.add('follower-active');
        });
        target.addEventListener('mouseleave', () => {
            cursor.classList.remove('cursor-active');
            cursorFollower.classList.remove('follower-active');
        });
    });

    // 2. Cinematic Page Transitions
    const overlay = document.createElement('div');
    overlay.className = 'page-transition-overlay';
    document.body.appendChild(overlay);

    document.querySelectorAll('a[href]:not([target="_blank"]):not([href^="#"]):not([href^="javascript:"])').forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href && !href.startsWith('#')) {
                e.preventDefault();
                overlay.classList.add('active');
                setTimeout(() => {
                    window.location.href = href;
                }, 350);
            }
        });
    });

    // 3. Scroll-Triggered Typography & Gloss Beam
    const scrollTexts = document.querySelectorAll('.scroll-reveal-text');
    const glossBeams = document.querySelectorAll('.gloss-beam-card');

    function checkScrollAnimations() {
        const triggerBottom = window.innerHeight * 0.85;

        scrollTexts.forEach(el => {
            const top = el.getBoundingClientRect().top;
            if (top < triggerBottom) {
                el.classList.add('revealed');
            }
        });

        glossBeams.forEach(card => {
            const top = card.getBoundingClientRect().top;
            if (top < triggerBottom) {
                card.classList.add('gloss-active');
            }
        });
    }

    window.addEventListener('scroll', checkScrollAnimations);
    checkScrollAnimations();
});
