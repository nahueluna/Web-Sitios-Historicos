from src.core.models.logs_actions.log_actions import LogActions
from src.core.database import db


def list_log_actions(): 
    return db.session.query(
        LogActions
    ).all()

def add_log_action(action: str):
    log_action_model = LogActions(action=action)
    db.session.add(log_action_model)
    db.session.commit()
    return log_action_model

def __generate_log_actions():
    log_actions = ["Creación", "Edición", "Eliminación", "Cambio de estado", "Cambio de tags"]
    for action in log_actions:
        action = LogActions(action=action)
        db.session.add(action)
    db.session.commit()