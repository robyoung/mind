from datetime import datetime

from .app import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    answers = db.relationship("Answer", order_by="Answer.created_at")

    def __repr__(self):
        return "<Question: {}>".format(self.title)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))

    def __repr__(self):
        return "<Answer: {}>".format(self.answer)
