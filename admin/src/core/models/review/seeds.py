import random
from datetime import datetime, timedelta, timezone
from src.core.database import db
from src.core.models.review.review import Review, ReviewStatus

NUMBER_OF_REVIEWS = 60

def seed_reviews():
    reviews = []
    now = datetime.now(timezone.utc)
    # build unique user+historic pairs and shuffle
    user_ids = [n for n in range(1, NUMBER_OF_REVIEWS + 1) if n % 3 == 0]
    historic_ids = list(range(1, NUMBER_OF_REVIEWS + 1))
    all_pairs = [(u, h) for u in user_ids for h in historic_ids]
    random.shuffle(all_pairs)

    limit = min(NUMBER_OF_REVIEWS, len(all_pairs))
    for i, (user_id, historic_site_id) in enumerate(all_pairs[:limit], start=1):
        inserted = now - timedelta(days=random.randint(0, 365), seconds=random.randint(0, 86400))
        updated = inserted + timedelta(seconds=random.randint(0, 86400 * 30))
        status = random.choice([ReviewStatus.APPROVED, ReviewStatus.PENDING, ReviewStatus.REJECTED])
        rejection = None
        if status == ReviewStatus.REJECTED:
            rejection = f"Rejection reason for review {i}"
        review = Review(
            content=f"Sample review content {i}",
            rating=random.randint(1, 5),
            status=status,
            inserted_at=inserted,
            updated_at=updated,
            historic_site_id=historic_site_id,
            user_id=user_id,
            rejection_reason=rejection,
        )
        reviews.append(review)
    db.session.add_all(reviews)
    db.session.commit()
    print(f"Seed completo: {NUMBER_OF_REVIEWS} reseñas creadas.")