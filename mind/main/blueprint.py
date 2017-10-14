from flask import Blueprint, render_template, redirect, url_for, request

from mind.models import Question, Answer
from mind.app import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    question_slug = 'how-are-you-feeling'
    question_url = url_for(
        '.show_question', question_slug=question_slug)
    return redirect(question_url), 301


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


@main.route("/question/<question_slug>", methods=["GET"])
def show_question(question_slug):
    question = Question.query.filter_by(slug=question_slug).one_or_none()
    if not question:
        # TODO: proper 404
        return "", 404

    return render_template(
        "show_question.html",
        question=question)


@main.route("/question/<question_slug>/answer", methods=["POST"])
def add_answer(question_slug):
    # TODO: add flash message
    # TODO: move to route filter
    question = Question.query.filter_by(slug=question_slug).one_or_none()
    if not question:
        # TODO: proper 404
        return "", 404
    answer = Answer(question_id=question.id, answer=request.form['answer'])
    db.session.add(answer)
    db.session.commit()

    return redirect(url_for(".show_question", question_slug=question_slug))
