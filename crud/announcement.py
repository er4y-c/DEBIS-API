from db.database import Session, engine
from models.models import Announcement

session = Session(bind=engine)

def get_all_announcement():
    return session.query(Announcement).all()