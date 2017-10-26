from datetime import datetime
import re
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from .app import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False, unique=True, index=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    answers = db.relationship("Answer", order_by="desc(Answer.created_at)")

    def __repr__(self):
        return "<Question: {}>".format(self.title)


# TODO: add tests around this
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
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    email_hash = db.Column(db.String, nullable=False, index=True, unique=True)
    twitter_handle = db.Column(db.String, nullable=True)
