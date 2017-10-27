from datetime import datetime
import re
import uuid

from sqlalchemy.dialects.postgresql import UUID

from .database import db
from .utils import hash_email


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False, unique=True, index=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    answers = db.relationship("Answer",
                              order_by="desc(Answer.created_at)",
                              backref="question")

    def __repr__(self):
        return "<Question: {}>".format(self.title)


RE_SLUG_REPLACE = re.compile(r'[^\w\-]+')


@db.event.listens_for(Question, "before_insert")
def default_slug(mapper, connection, target):
    if not target.slug:
        target.slug = RE_SLUG_REPLACE.sub('-', target.title.lower())


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    user_uuid = db.Column(
        UUID(as_uuid=True), db.ForeignKey('user.uuid'), nullable=False)

    def __repr__(self):
        return "<Answer: {}>".format(self.answer)


class User(db.Model):
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    latest_answer_created_at = db.Column(
        db.DateTime, nullable=True)

    email_hash = db.Column(db.String, nullable=False, index=True, unique=True)
    twitter_handle = db.Column(db.String, nullable=True)

    answers = db.relationship("Answer", backref="user")

    def __repr__(self):
        return f"<User: {self.uuid}>"

    @staticmethod
    def get_or_create(email):
        email_hash = hash_email(email)
        user = User.query.filter(User.email_hash == email_hash).first()
        if user is None:
            user = User(email_hash=hash_email(email))
            db.session.add(user)
            db.session.commit()
        return user


@db.event.listens_for(Answer, "after_insert")
def update_user_latest_answer_created_at(mapper, connection, target):
    print("Ever in here")
    user_table = User.__table__
    connection.execute(
        user_table.update().
        where(user_table.c.uuid == target.user.uuid).
        values(latest_answer_created_at=datetime.utcnow())
    )
