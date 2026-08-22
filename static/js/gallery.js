// Gallery Filtering & Lightbox Handler
document.addEventListener('DOMContentLoaded', () => {
    // Lightbox modal injection
    const lightboxHtml = `
        <div id="gallery-lightbox" class="lightbox-modal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.92); z-index:2000; align-items:center; justify-content:center; backdrop-filter:blur(10px);">
            <button id="lightbox-close" style="position:absolute; top:30px; right:30px; background:none; border:none; color:#fff; font-size:2.5rem; cursor:pointer;">&times;</button>
            <div style="max-width:90%; max-height:85vh; text-align:center;">
                <img id="lightbox-img" src="" alt="" style="max-width:100%; max-height:75vh; border-radius:8px; border:1px solid rgba(255,255,255,0.15); box-shadow:0 0 30px rgba(0,0,0,0.8);">
                <div id="lightbox-caption" style="color:#ffffff; margin-top:16px; font-family:'Outfit', sans-serif; font-size:1.2rem; font-weight:600;"></div>
                <div id="lightbox-category" style="color:#ff1e27; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px; margin-top:4px;"></div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', lightboxHtml);

    const lightbox = document.getElementById('gallery-lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');
    const lightboxCategory = document.getElementById('lightbox-category');
    const closeBtn = document.getElementById('lightbox-close');

    // Gallery item click trigger
    document.querySelectorAll('.gallery-item').forEach(item => {
        item.addEventListener('click', () => {
            const img = item.querySelector('img');
            const title = item.querySelector('.gallery-title')?.innerText || '';
            const category = item.querySelector('.gallery-category')?.innerText || '';

            if (img && lightbox) {
                lightboxImg.src = img.src;
                lightboxCaption.innerText = title;
                lightboxCategory.innerText = category;
                lightbox.style.display = 'flex';
            }
        });
    });

    if (closeBtn && lightbox) {
        closeBtn.addEventListener('click', () => lightbox.style.display = 'none');
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) lightbox.style.display = 'none';
        });
    }

    // Filter Buttons
    const filterBtns = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const category = btn.getAttribute('data-filter');

            galleryItems.forEach(item => {
                const itemCat = item.getAttribute('data-category');
                if (category === 'ALL' || itemCat === category) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
});
