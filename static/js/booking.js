// Customer Booking Form Logic & Date Bounds
document.addEventListener('DOMContentLoaded', () => {
    const bookingForm = document.getElementById('service-booking-form');
    const dateInput = document.getElementById('preferred_date');

    // Set minimum booking date to today
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }

    if (bookingForm) {
        bookingForm.addEventListener('submit', (e) => {
            const phone = document.getElementById('customer_phone')?.value.trim();
            if (phone && phone.length < 7) {
                alert('Please enter a valid phone or WhatsApp number.');
                e.preventDefault();
            }
        });
    }
});
