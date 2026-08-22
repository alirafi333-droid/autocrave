// 3D Interactive Car Movement & Hotspot Viewer Handler
document.addEventListener('DOMContentLoaded', () => {
    // 1. Hero 3D Interactive Moving Studio BMW Car
    const heroSection = document.querySelector('.hero-section');
    const heroCarContainer = document.querySelector('.hero-bg-container');
    const heroCarImg = document.querySelector('.hero-bg-image');

    if (heroSection && heroCarImg) {
        let isDragging = false;
        let startX = 0, startY = 0;
        let currentRotateX = 0, currentRotateY = 0;
        let targetRotateX = 0, targetRotateY = 0;
        let targetTranslateZ = 0;

        // Smooth 60fps RAF lerp loop
        function animate3DCar() {
            // Smoothly interpolate towards target rotation
            currentRotateX += (targetRotateX - currentRotateX) * 0.08;
            currentRotateY += (targetRotateY - currentRotateY) * 0.08;

            const scrollOffset = window.scrollY * 0.15;
            const scrollScale = 1 + (window.scrollY * 0.0003);

            heroCarImg.style.transform = `
                perspective(1000px)
                rotateX(${currentRotateX}deg)
                rotateY(${currentRotateY}deg)
                translateZ(${targetTranslateZ}px)
                translateY(${scrollOffset}px)
                scale(${scrollScale})
            `;

            requestAnimationFrame(animate3DCar);
        }

        animate3DCar();

        // Mouse move 3D perspective tilt
        window.addEventListener('mousemove', (e) => {
            if (isDragging) return;
            const windowWidth = window.innerWidth;
            const windowHeight = window.innerHeight;

            const mouseX = (e.clientX / windowWidth) - 0.5; // -0.5 to 0.5
            const mouseY = (e.clientY / windowHeight) - 0.5; // -0.5 to 0.5

            targetRotateY = mouseX * 24; // Tilt Y up to 24 deg
            targetRotateX = -mouseY * 18; // Tilt X up to 18 deg
            targetTranslateZ = Math.abs(mouseX * 40);
        });

        // Touch & Mouse Drag to Rotate / Tilt 3D Car
        if (heroCarContainer) {
            heroCarContainer.addEventListener('mousedown', (e) => {
                isDragging = true;
                startX = e.clientX;
                startY = e.clientY;
            });

            window.addEventListener('mouseup', () => {
                isDragging = false;
            });

            window.addEventListener('mousemove', (e) => {
                if (!isDragging) return;
                const deltaX = e.clientX - startX;
                const deltaY = e.clientY - startY;

                targetRotateY += deltaX * 0.2;
                targetRotateX -= deltaY * 0.2;

                startX = e.clientX;
                startY = e.clientY;
            });

            // Touch events for mobile/tablet 3D rotation
            heroCarContainer.addEventListener('touchstart', (e) => {
                if (e.touches.length === 1) {
                    isDragging = true;
                    startX = e.touches[0].clientX;
                    startY = e.touches[0].clientY;
                }
            }, { passive: true });

            window.addEventListener('touchend', () => {
                isDragging = false;
            });

            window.addEventListener('touchmove', (e) => {
                if (!isDragging || !e.touches[0]) return;
                const deltaX = e.touches[0].clientX - startX;
                const deltaY = e.touches[0].clientY - startY;

                targetRotateY += deltaX * 0.25;
                targetRotateX -= deltaY * 0.25;

                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
            }, { passive: true });
        }
    }

    // 2. 360° Interactive Vehicle Viewer with Hotspots
    const hotspots = document.querySelectorAll('.hotspot');
    const infoCard = document.getElementById('hotspot-info-card');

    if (hotspots.length > 0 && infoCard) {
        hotspots.forEach(spot => {
            spot.addEventListener('click', () => {
                const title = spot.getAttribute('data-title');
                const text = spot.getAttribute('data-text');
                const badge = spot.getAttribute('data-badge');

                hotspots.forEach(s => s.classList.remove('active'));
                spot.classList.add('active');

                infoCard.innerHTML = `
                    <div style="font-size:0.75rem; color:var(--red-z); font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">${badge}</div>
                    <h4 style="font-size:1.3rem; color:#fff; margin-bottom:8px;">${title}</h4>
                    <p style="color:var(--text-muted); font-size:0.95rem; margin-bottom:16px;">${text}</p>
                    <a href="https://wa.me/923001234567?text=Hi%20AutozCraveStudio!%20I'm%20inquiring%20about%20${encodeURIComponent(title)}." target="_blank" class="btn-primary" style="padding:8px 18px; font-size:0.8rem;">
                        <i class="fa-brands fa-whatsapp"></i> Inquire About This Treatment
                    </a>
                `;
                infoCard.style.display = 'block';
            });
        });
    }

    // 3. 3D Canvas Animated LED Tunnel Light Grid Background
    const canvas = document.getElementById('3d-canvas-bg');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        let scrollY = 0;
        window.addEventListener('scroll', () => {
            scrollY = window.scrollY;
        });

        function renderLEDTunnel() {
            ctx.clearRect(0, 0, width, height);

            const scrollOffset = (scrollY * 0.2) % 60;
            ctx.strokeStyle = 'rgba(255, 30, 39, 0.08)';
            ctx.lineWidth = 1.5;

            // Draw glowing LED tunnel perspective arches matching studio photo
            for (let i = 0; i < 8; i++) {
                const z = (i * 80 + scrollOffset) % 600;
                const scale = 1 - (z / 800);
                if (scale <= 0) continue;

                const archW = width * 0.7 * scale;
                const archH = height * 0.6 * scale;
                const archX = (width - archW) / 2;
                const archY = (height - archH) / 2;

                ctx.beginPath();
                ctx.rect(archX, archY, archW, archH);
                ctx.stroke();
            }

            requestAnimationFrame(renderLEDTunnel);
        }

        renderLEDTunnel();
    }
});
