from datetime import datetime
from models import db

class BeforeAfterItem(db.Model):
    __tablename__ = 'before_after'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    before_image = db.Column(db.String(255), nullable=False)
    after_image = db.Column(db.String(255), nullable=False)
    service_category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BeforeAfterItem {self.title}>'
