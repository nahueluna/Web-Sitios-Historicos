from src.core.models.historic_sites_logs.hs_logs import HistoricSitesLogs
from src.core.database import db

# Obtiene todos los logs de un sitio histórico específico
def get_logs_per_hs(hs_id: int):
    return db.session.query(
        HistoricSitesLogs
    ).filter(
        HistoricSitesLogs.historic_site_id == hs_id
    ).order_by(
        HistoricSitesLogs.log_date.desc()
    ).all()

def add_log(hs_id: int, action_type: str)-> HistoricSitesLogs:
    log_model = HistoricSitesLogs(
        historic_site_id = hs_id,
        action_type = action_type
    )
    db.session.add(log_model)
    db.session.commit()
    return log_model