from src.core.database import db
from src.core.models.review.review import Review
from src.core.models.auth import Usuario
from datetime import datetime

def list_reviews_with_filters(site='', status='', rating='', date_from='', date_to='', user_email='', order_by='inserted_at', order_dir='desc', page=1, per_page=25):
    query = db.session.query(
        Review
    )

    if site:
        query = query.filter(
            Review.historic_site_id == site
        )

    if status:
        query = query.filter(Review.status == status)

    if rating:
        query = query.filter(Review.rating == rating)

    if date_from:
        try:
            date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Review.inserted_at >= date_from_parsed)
        except ValueError:
            pass

    if date_to:
        try:
            date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(Review.inserted_at <= date_to_parsed)
        except ValueError:
            pass

    if user_email:
        query = query.join(Usuario, Review.user_id == Usuario.id).filter(Usuario.email.ilike(f"%{user_email}%"))

    if order_by in ['inserted_at', 'rating']:
        order_column = getattr(Review, order_by)
        if order_dir == 'desc':
            order_column = order_column.desc()
        else:
            order_column = order_column.asc()
        query = query.order_by(order_column)

    total = query.count()

    if not page is None:
        reviews = query.offset((int(page) - 1) * int(per_page)).limit(int(per_page)).all()
    else:
        reviews = query.all()

    return reviews, total

def get_specific_review(review_id):
    review_obj = db.session.query(Review).filter(Review.id == review_id).first()
    return review_obj

def create_review(**kwargs):
    review_obj = Review(**kwargs)
    db.session.add(review_obj)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return review_obj

def update_review_status(review_id, new_status, review_rejection_reason=None):
    review_obj = db.session.query(Review).filter(Review.id == review_id).first()
    if review_obj:
        review_obj.status = new_status
        review_obj.rejection_reason = review_rejection_reason

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    return review_obj

def remove_review(review_id):
    review_obj = db.session.query(Review).filter(Review.id == review_id).first()

    if review_obj:
        db.session.delete(review_obj)
        db.session.commit()
        return True

    return False