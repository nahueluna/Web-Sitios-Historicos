from src.core.database import db
from src.core.models.review.review import Review

def show_specific_review(review_id):
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
        review.rejection_reason = review_rejection_reason

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