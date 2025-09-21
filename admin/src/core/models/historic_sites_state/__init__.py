from src.core.database import db
from src.core.models.historic_sites_state.hs_states import HistoricSitesStates  

def list_historic_sites_states(): return db.session.query(HistoricSitesStates).all()

def generate_states():
    states = ["Bueno", "Regular", "Malo"]
    for state in states:
        hs_state = HistoricSitesStates(state=state)
        db.session.add(hs_state)
    db.session.commit()