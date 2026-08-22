// Interactive Before & After Comparison Slider
document.addEventListener('DOMContentLoaded', () => {
    const sliders = document.querySelectorAll('.ba-container');

    sliders.forEach(container => {
        const beforeImg = container.querySelector('.ba-image-before');
        const handle = container.querySelector('.ba-slider-handle');

        if (!beforeImg || !handle) return;

        let isDragging = false;

        function setPosition(x) {
            const rect = container.getBoundingClientRect();
            let position = x - rect.left;
            
            // Clamp within container boundaries
            if (position < 0) position = 0;
            if (position > rect.width) position = rect.width;

            const percentage = (position / rect.width) * 100;
            beforeImg.style.width = `${percentage}%`;
            handle.style.left = `${percentage}%`;
        }

        // Mouse Events
        container.addEventListener('mousedown', (e) => {
            isDragging = true;
            setPosition(e.clientX);
        });

        window.addEventListener('mouseup', () => {
            isDragging = false;
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            setPosition(e.clientX);
        });

        // Touch Events for Mobile / Tablet
        container.addEventListener('touchstart', (e) => {
            isDragging = true;
            if (e.touches[0]) setPosition(e.touches[0].clientX);
        }, { passive: true });

        window.addEventListener('touchend', () => {
            isDragging = false;
        });

        window.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            if (e.touches[0]) setPosition(e.touches[0].clientX);
        }, { passive: true });
    });
});
