from application import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=64), unique=True, nullable=False)
    email = db.Column(db.String(length=64), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=64), nullable=False)
    history = db.Column(db.String(length=2048), nullable=True)
    note = db.Column(db.String(length=512), nullable=True)

    def __repr__(self):
        return f"Username: {self.username}, Email: {self.email}, Password: {self.password_hash}"


