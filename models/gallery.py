from datetime import datetime
from models import db

class GalleryItem(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Ceramic Coating, Glass Coating, Graphene Coating, PPF, Deep Detailing, General
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<GalleryItem {self.title} ({self.category})>'
