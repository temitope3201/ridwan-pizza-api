from ..utils import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(45), nullable = False, unique = True)
    email = db.Column(db.String(60), nullable = False, unique = True)
    password_hash = db.Column(db.Text(), nullable = False)
    is_staff = db.Column(db.Boolean(), default = False)
    is_active = db.Column(db.Boolean(), default = False)
    orders = db.relationship('Order', backref = 'customer', lazy = True)

    def __repr__(self) -> str:
        return f"The Username of this User is {self.username}"

    def save(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):

        return cls.query.get_or_404(id)
