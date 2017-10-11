from flask import Blueprint, render_template, redirect, url_for, request

from mind.models import Question, Answer
from mind.app import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/question", methods=["GET"])
def list_questions():
    questions = Question.query.all()

    return render_template(
        "list_questions.html",
        questions=questions)


@main.route("/question", methods=["POST"])
def add_question():
    db.session.add(Question(title=request.form['question_title']))
    db.session.commit()

    return redirect(url_for(".list_questions"))


@main.route("/question/<int:question_id>", methods=["GET"])
def show_question(question_id):
    question = Question.query.get(question_id)

    return render_template(
        "show_question.html",
        question=question)


@main.route("/question/<int:question_id>/answer", methods=["POST"])
def add_answer(question_id):
    db.session.add(Answer(question_id=question_id, answer=request.form['answer']))
    db.session.commit()

    return redirect(url_for(".show_question", question_id=question_id))
