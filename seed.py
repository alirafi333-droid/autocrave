import os
import shutil
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def create_placeholder_image(filename, title, subtitle, bg_color=(15, 17, 24), accent_color=(255, 30, 39)):
    """Creates a sleek dark-themed placeholder image using Pillow"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw dark subtle grid/gradient background
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=(25, 28, 38), width=1)
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=(25, 28, 38), width=1)

    # Accent glow top bar
    draw.rectangle([0, 0, width, 8], fill=accent_color)
    
    # Border
    draw.rectangle([10, 18, width-10, height-10], outline=(40, 45, 60), width=2)

    # Text rendering (using default font if custom font not present)
    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("arial.ttf", 20)
        font_brand = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_brand = ImageFont.load_default()

    # Draw text
    draw.text((40, 40), "AUTO Z CRAVE STUDIO", fill=accent_color, font=font_brand)
    draw.text((40, height // 2 - 30), title, fill=(255, 255, 255), font=font_large)
    draw.text((40, height // 2 + 20), subtitle, fill=(180, 185, 200), font=font_small)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename, 'PNG')

def run_seed():
    from app import create_app
    from models import db
    from models.user import User
    from models.service import Service
    from models.booking import Booking
    from models.gallery import GalleryItem
    from models.before_after import BeforeAfterItem
    from models.contact import ContactMessage

    app = create_app()

    with app.app_context():
        print("Re-creating database tables...")
        db.drop_all()
        db.create_all()

        # Copy generated images if available
        brain_dir = r"C:\Users\Lenovo\.gemini\antigravity\brain\22be9ede-0920-46df-8d27-f4a75a389aa7"
        base_dir = app.config.get('BASE_DIR') or os.path.dirname(os.path.abspath(__file__))
        static_img_dir = os.path.join(base_dir, 'static', 'images')
        uploads_dir = os.path.join(base_dir, 'static', 'uploads')
        
        os.makedirs(static_img_dir, exist_ok=True)
        os.makedirs(os.path.join(uploads_dir, 'services'), exist_ok=True)
        os.makedirs(os.path.join(uploads_dir, 'gallery'), exist_ok=True)
        os.makedirs(os.path.join(uploads_dir, 'before_after'), exist_ok=True)

        # Copy real user uploaded images if available
        user_up = os.path.join(brain_dir, '.user_uploaded') if brain_dir else ''
        
        # 1. Logo
        if user_up and os.path.exists(os.path.join(user_up, 'media_1787382743272.jpg')):
            shutil.copy(os.path.join(user_up, 'media_1787382743272.jpg'), os.path.join(static_img_dir, 'logo.jpg'))

        # 2. Studio BMW Hero
        if user_up and os.path.exists(os.path.join(user_up, 'media_1787382800582.jpg')):
            shutil.copy(os.path.join(user_up, 'media_1787382800582.jpg'), os.path.join(static_img_dir, 'studio_bmw.jpg'))
            shutil.copy(os.path.join(user_up, 'media_1787382800582.jpg'), os.path.join(static_img_dir, 'hero_car.png'))

        # 3. Ceramic Coating
        if brain_dir and os.path.exists(os.path.join(brain_dir, 'ceramic_coating_1787155680395.png')):
            shutil.copy(os.path.join(brain_dir, 'ceramic_coating_1787155680395.png'), os.path.join(uploads_dir, 'services', 'ceramic_coating.png'))

        # 4. Glass Coating
        if user_up and os.path.exists(os.path.join(user_up, 'media_1787386591307.png')):
            shutil.copy(os.path.join(user_up, 'media_1787386591307.png'), os.path.join(uploads_dir, 'services', 'glass_coating.png'))

        # 5. Graphene Coating
        if user_up and os.path.exists(os.path.join(user_up, 'media_1787386798924.png')):
            shutil.copy(os.path.join(user_up, 'media_1787386798924.png'), os.path.join(uploads_dir, 'services', 'graphene_coating.png'))

        # 6. PPF Protection
        if user_up and os.path.exists(os.path.join(user_up, 'media_1787386955131.png')):
            shutil.copy(os.path.join(user_up, 'media_1787386955131.png'), os.path.join(uploads_dir, 'services', 'ppf_protection.png'))

        # 7. Deep Detailing
        if user_up and os.path.exists(os.path.join(user_up, 'media_1787387121600.png')):
            shutil.copy(os.path.join(user_up, 'media_1787387121600.png'), os.path.join(uploads_dir, 'services', 'deep_detailing.png'))

        # 8. Before & After BMW Transformation Photos
        if user_up and os.path.exists(os.path.join(user_up, 'media_1787389934522.jpg')):
            shutil.copy(os.path.join(user_up, 'media_1787389934522.jpg'), os.path.join(static_img_dir, 'before_bmw.jpg'))
            shutil.copy(os.path.join(user_up, 'media_1787389934522.jpg'), os.path.join(uploads_dir, 'before_after', 'paint_before.png'))

        if user_up and os.path.exists(os.path.join(user_up, 'media_1787389948184.jpg')):
            shutil.copy(os.path.join(user_up, 'media_1787389948184.jpg'), os.path.join(static_img_dir, 'after_bmw.jpg'))
            shutil.copy(os.path.join(user_up, 'media_1787389948184.jpg'), os.path.join(uploads_dir, 'before_after', 'paint_after.png'))

        print("Preserved and synced all real photos for services & before/after slider.")

        # Gallery placeholders
        create_placeholder_image(os.path.join(uploads_dir, 'gallery', 'porsche_ppf.png'), "Porsche 911 GT3 - Full PPF", "Category: PPF")
        create_placeholder_image(os.path.join(uploads_dir, 'gallery', 'audi_ceramic.png'), "Audi RS6 - 9H Ceramic", "Category: Ceramic Coating")
        create_placeholder_image(os.path.join(uploads_dir, 'gallery', 'bmw_graphene.png'), "BMW M5 - 10H Graphene", "Category: Graphene Coating")
        create_placeholder_image(os.path.join(uploads_dir, 'gallery', 'mercedes_glass.png'), "Mercedes G63 - Glass Shield", "Category: Glass Coating")
        create_placeholder_image(os.path.join(uploads_dir, 'gallery', 'range_detailing.png'), "Range Rover SVR - Deep Detail", "Category: Deep Detailing")

        # Before & After placeholders
        create_placeholder_image(os.path.join(uploads_dir, 'before_after', 'paint_before.png'), "BEFORE: Heavy Swirls & Oxidation", "Paint Condition Prior to Treatment", bg_color=(25, 20, 20), accent_color=(150, 40, 40))
        create_placeholder_image(os.path.join(uploads_dir, 'before_after', 'paint_after.png'), "AFTER: Flawless 9H Ceramic Finish", "Mirror Reflection Restored", bg_color=(10, 25, 20), accent_color=(40, 220, 100))
        
        create_placeholder_image(os.path.join(uploads_dir, 'before_after', 'headlight_before.png'), "BEFORE: Yellowed & Fogged Headlight", "Dull & Scratched Lens Surface", bg_color=(25, 20, 20), accent_color=(150, 40, 40))
        create_placeholder_image(os.path.join(uploads_dir, 'before_after', 'headlight_after.png'), "AFTER: Diamond Clear Headlight", "Restored Optical Clarity", bg_color=(10, 25, 20), accent_color=(40, 220, 100))

        print("Seeding Admin User...")
        admin = User(
            name="adminjawad",
            email="adminjawad@autozcrave.com",
            role="admin"
        )
        admin.set_password("adminjawad")
        db.session.add(admin)

        print("Seeding Services...")
        s1 = Service(
            name="Ceramic Coating",
            description="Premium 9H Nano-Ceramic Coating providing deep gloss enhancement, chemical resistance, UV block, and hydrophobic paint protection against environmental contaminants. Starting from PKR 8,000 (Hatchback), PKR 12,000 (Sedan), PKR 15,000 (Crossover), PKR 20,000 (SUV).",
            price="Starting from PKR 8,000",
            duration="1 - 2 Days",
            image="uploads/services/ceramic_coating.png",
            is_active=True
        )
        s2 = Service(
            name="Glass Coating",
            description="Ultra-durable hydrophobic windshield and glass treatment ensuring crystal clear wet weather visibility, water repelling, and reduced glare. Starting from PKR 8,000 (Hatchback), PKR 12,000 (Sedan), PKR 15,000 (Crossover), PKR 20,000 (SUV).",
            price="Starting from PKR 8,000",
            duration="1 - 2 Days",
            image="uploads/services/glass_coating.png",
            is_active=True
        )
        s3 = Service(
            name="Graphene Coating",
            description="Next-generation 10H Graphene Matrix coating offering unparalleled heat dissipation, enhanced water-spotting prevention, and extreme durability up to 5 years. Starting from PKR 8,000 (Hatchback), PKR 12,000 (Sedan), PKR 15,000 (Crossover), PKR 20,000 (SUV).",
            price="Starting from PKR 8,000",
            duration="1 - 2 Days",
            image="uploads/services/graphene_coating.png",
            is_active=True
        )
        s4 = Service(
            name="Paint Protection Film (PPF)",
            description="Self-healing Thermoplastic Polyurethane (TPU) paint protection film shielding your vehicle against stone chips, deep scratches, and road debris. Starting from PKR 60,000 (Hatchback), PKR 100,000 (Sedan), PKR 130,000 (Crossover), PKR 150,000 (SUV).",
            price="Starting from PKR 60,000",
            duration="1 - 2 Days",
            image="uploads/services/ppf_protection.png",
            is_active=True
        )
        s5 = Service(
            name="Deep Detailing",
            description="Comprehensive interior and exterior restoration detailing including multi-stage paint correction, leather conditioning, engine bay detailing, and wheel protection. Starting from PKR 6,000 (Hatchback), PKR 8,000 (Sedan), PKR 10,000 (Crossover), PKR 13,000 (SUV).",
            price="Starting from PKR 6,000",
            duration="1 - 2 Days",
            image="uploads/services/deep_detailing.png",
            is_active=True
        )
        db.session.add_all([s1, s2, s3, s4, s5])
        db.session.commit()

        print("Seeding Gallery Items...")
        g1 = GalleryItem(
            title="Porsche 911 GT3 RS Full PPF Wrap",
            category="PPF",
            description="Full body self-healing TPU PPF installation completed with custom computer-cut edges at DHA Lahore studio.",
            image_path="uploads/gallery/porsche_ppf.png"
        )
        g2 = GalleryItem(
            title="Audi RS6 Avant 9H Ceramic Shield",
            category="Ceramic Coating",
            description="Dual layer 9H ceramic coating paint correction delivering candy-like deep gloss reflection.",
            image_path="uploads/gallery/audi_ceramic.png"
        )
        g3 = GalleryItem(
            title="BMW M5 Competition 10H Graphene Armor",
            category="Graphene Coating",
            description="Ultra high heat dissipation graphene coating applied onto Frozen Black exterior finish.",
            image_path="uploads/gallery/bmw_graphene.png"
        )
        g4 = GalleryItem(
            title="Mercedes G63 AMG Glass Hydro-Armor",
            category="Glass Coating",
            description="360 degree hydrophobic windshield and side glass coating protection package.",
            image_path="uploads/gallery/mercedes_glass.png"
        )
        g5 = GalleryItem(
            title="Range Rover Sport SVR Concours Detail",
            category="Deep Detailing",
            description="3-stage paint correction, interior leather feeding, and ceramic rim coating treatment.",
            image_path="uploads/gallery/range_detailing.png"
        )
        db.session.add_all([g1, g2, g3, g4, g5])

        print("Seeding Before & After Projects...")
        ba1 = BeforeAfterItem(
            title="Black Paint Swirl & Hologram Correction",
            service_category="Ceramic Coating",
            description="Heavy oxidation and car wash scratches corrected with multi-stage rotary polishing followed by 9H Ceramic Shield.",
            before_image="uploads/before_after/paint_before.png",
            after_image="uploads/before_after/paint_after.png"
        )
        ba2 = BeforeAfterItem(
            title="Headlight Clarity & UV Restoration",
            service_category="Deep Detailing",
            description="Oxidized yellowed headlight lens wet sanded, polished, and sealed with ceramic UV coat.",
            before_image="uploads/before_after/headlight_before.png",
            after_image="uploads/before_after/headlight_after.png"
        )
        db.session.add_all([ba1, ba2])

        print("Seeding Sample Bookings & Messages...")
        b1 = Booking(
            customer_name="Zayn Malik",
            customer_email="zayn@example.com",
            customer_phone="+923009876543",
            vehicle_make="Audi",
            vehicle_model="e-Tron GT",
            vehicle_year="2024",
            service_id=s1.id,
            preferred_date="2026-08-25",
            preferred_time="10:00 AM",
            additional_notes="Interested in dual coat ceramic and leather protection.",
            status="Pending"
        )
        b2 = Booking(
            customer_name="Hamza Khan",
            customer_email="hamza@example.com",
            customer_phone="+923214567890",
            vehicle_make="Porsche",
            vehicle_model="Taycan Turbo S",
            vehicle_year="2025",
            service_id=s4.id,
            preferred_date="2026-08-28",
            preferred_time="02:00 PM",
            additional_notes="Full front bumper and bonnet PPF package required.",
            status="Confirmed"
        )
        db.session.add_all([b1, b2])

        m1 = ContactMessage(
            name="Ali Hassan",
            email="ali.hassan@example.pk",
            phone="+923331122334",
            subject="PPF Package for Mercedes S-Class in DHA Lahore",
            message="Hi AutozCraveStudio team, I want to inquire about full body TPU PPF for my new Mercedes S-Class. Please share price options and booking slots."
        )
        db.session.add(m1)

        db.session.commit()
        print("Database initialized and successfully seeded!")

if __name__ == '__main__':
    run_seed()
