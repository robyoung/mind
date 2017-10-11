from flask import Blueprint, render_template

from mind.models import Question

main = Blueprint("main", __name__)


@main.route("/")
def list_questions():
    questions = Question.query.all()

    return render_template("list_questions.html",
                           questions=questions)
