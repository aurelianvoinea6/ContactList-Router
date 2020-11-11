from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __init__(self, _id, email, password, is_active):
        self.id=_id
        self.email=email
        self.password=password
        self.is_active=is_active

    @classmethod
    def get_user_by_username(cls, username):
        user_results = cls.query.filter_by(username=username).first()
        return user_results

    @classmethod
    def get_user_by_id(cls, id):
        user_results = cls.query.filter_by(id=id).first()
        return user_results

    def save_to_data(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self):
        db.session.delete(self)
        db.session.commit()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), unique=False, nullable=False)
    done = db.Column(db.Boolean(), unique=False, nullable=False)
    username = db.Column(db.String(25), unique=False, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.label

    def __init__(self, label, done, username):
        self.label=label
        self.done=done
        self.username=username

    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "done": self.done,
            "username": self.username
            # do not serialize the password, its a security breach
        }

    @classmethod
    def get_task_by_username(cls, username):
        task_results = cls.query.filter_by(username=username)
        serialized_tasks = list(map(lambda x: x.serialize(), task_results))
        return serialized_tasks

    @classmethod
    def get_task_by_id(cls, id):
        task_results = cls.query.filter_by(id=id).first()
        return task_results

    def save_to_data(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self):
        db.session.delete(self)
        db.session.commit()