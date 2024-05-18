

from myproject import db

class Puppy(db.Model):

    __tablename__ = 'puppies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    owner = db.relationship('Owner', backref='puppy', uselist=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f"Puppy name: {self.name} and Owner: {self.owner.name}"
        else:
            return f"Puppy name: {self.name} and no owner yet!"



class Owner(db.Model):

    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, name , puppy_id):
        self.name = name
        self.puppy_id = puppy_id

    def __repr__(self):
        if self.puppy_id:
            return f"Owner name: {self.name} and Puppy id: {self.puppy_id}"
        else:
            return f"Owner name: {self.name} and no puppy assigned yet!"
