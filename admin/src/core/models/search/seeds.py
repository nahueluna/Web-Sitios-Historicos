import random
from src.core.database import db
from src.core.models.search.tags import Tag
from src.core.models.historic_sites.historic_sites import HistoricSites
from src.core.models.historic_site_tags.hs_tags import HistoricSitesTags

# 1. Seed tags
TAG_NAMES = [
    "Patrimonio", "Museo", "Monumento", "Sitio arqueológico", "Edificio histórico",
    "Cultural", "Natural", "Religioso", "Militar", "Educativo"
]

def seed_tags():
    tags = []
    for name in TAG_NAMES:
        tag = Tag(
            name=name,
            slug=name.lower().replace(" ", "-")
        )
        tags.append(tag)
    db.session.add_all(tags)
    db.session.commit()
    print(f"Seed completo: {len(TAG_NAMES)} tags creados.")

# 2. Seed historic_sites_tags
def seed_historic_sites_tags():
    sites = db.session.query(HistoricSites).all()
    tags = db.session.query(Tag).all()
    relations = []
    for site in sites:
        # Assign 1-3 random tags to each site
        assigned_tags = random.sample(tags, k=random.randint(1, 3))
        for tag in assigned_tags:
            relation = HistoricSitesTags(site_id=site.id, tag_id=tag.id)
            relations.append(relation)
    db.session.add_all(relations)
    db.session.commit()
    print(f"Seed completo: {len(relations)} relaciones sitio-tag creadas.")
