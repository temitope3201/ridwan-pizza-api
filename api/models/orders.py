from ..utils import db
from enum import Enum
from datetime import datetime

class Sizes(Enum):

    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra_large'

class OrderStatus(Enum):

    PENDING = 'pending'
    IN_TRANSIT = 'in_transit'
    DELIVERED = 'delivered'

class Flavour(Enum):

    BARBECUE_CHICKEN = 'barbecue_chicken'
    BARBECUE_BEEF = 'barbecue_beef'
    MAGHERITTA = 'magheritta'
    PEPPERONI = 'pepperoni'
    SUYA = 'suya'
    MARGHERITTA = 'magheritta'
    



class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer(), primary_key = True)
    quantity = db.Column(db.Integer(), nullable = False)
    size = db.Column(db.Enum(Sizes), default = Sizes.MEDIUM)
    order_status = db.Column(db.Enum(OrderStatus), default = OrderStatus.PENDING)
    flavour = db.Column(db.Enum(Flavour), nullable = False)
    date_created = db.Column(db.DateTime(), default = datetime.utcnow)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f"Order {self.id}"

    def save(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):

        return cls.query.get_or_404(id)

    
    def delete_order(self):

        db.session.delete(self)
        db.session.commit()