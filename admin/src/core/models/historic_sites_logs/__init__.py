from typing import List
from src.core.models.historic_sites_logs.hs_logs import HistoricSitesLogs
from src.core.database import db
from sqlalchemy.orm import joinedload

# Obtiene todos los logs de un sitio histórico específico
def get_logs_per_hs(hs_id: int)-> List[HistoricSitesLogs]:
    return db.session.query(
        HistoricSitesLogs
    ).filter(
        HistoricSitesLogs.historic_site_id == hs_id
    ).order_by(
        HistoricSitesLogs.log_date.desc()
    ).all()

def add_log(hs_id: int, action_type_id: int)-> HistoricSitesLogs:
    log_model = HistoricSitesLogs(
        historic_site_id = hs_id,
        action_type_id = action_type_id
    )
    db.session.add(log_model)
    db.commit()
    return log_model