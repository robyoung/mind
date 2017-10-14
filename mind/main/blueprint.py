from flask import Blueprint, render_template, redirect, url_for, request, abort

from mind.models import Question, Answer
from mind.app import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    question_slug = 'how-are-you-feeling'
    question_url = url_for('.show_question', question=question_slug)
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


@main.route("/question/<question>", methods=["GET"])
def show_question(question):
    return render_template("show_question.html", question=question)


@main.route("/question/<question>/answer", methods=["POST"])
def add_answer(question):
    # TODO: add flash message
    answer = Answer(question_id=question.id, answer=request.form['answer'])
    db.session.add(answer)
    db.session.commit()

    return redirect(url_for(".show_question", question=question))


MODEL_URL_MAP = {
    'question': Question
}


@main.url_defaults
def add_slug_to_url(endpoint, values):
    for field in MODEL_URL_MAP.keys():
        if field in values and hasattr(values[field], 'slug'):
            values[field] = values[field].slug


@main.url_value_preprocessor
def resolve_slug(endpoint, values):
    for field, model in MODEL_URL_MAP.items():
        if field in values:
            record = model.query \
                    .filter_by(slug=values[field]) \
                    .one_or_none()
            if not record:
                abort(404)
            values[field] = record
