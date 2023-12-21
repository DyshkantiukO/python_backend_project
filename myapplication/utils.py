from myapplication import db


def add(data):
    db.session.add(data)
    db.session.commit()


def update():
    db.session.commit()


def delete(model_class, item_id):
    try:
        item = db.session.query(model_class).filter(model_class.id == item_id).first()
        if item:
            deleted_item = {"id": item.id, **item.to_dict()}
            db.session.delete(item)
            db.session.commit()
            return deleted_item
        else:
            return None
    except AttributeError:
        return None
