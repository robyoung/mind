from mind.app import db
from mind.models import Question, Answer


def test_list_questions(test_client):
    response = test_client.get('/mind/question')

    assert response.status_code == 200


def test_show_non_existent_question(test_client):
    response = test_client.get('/mind/question/not-there')

    assert response.status_code == 404


def test_show_question(test_client, question):
    response = test_client.get('/mind/question/test-question')

    assert response.status_code == 200
    assert 'Test question' in response.get_data(as_text=True)


def test_question_login_link_instead_of_answer_form_if_not_logged_in(
    test_client, question
):
    response = test_client.get('/mind/question/test-question')

    page_html = response.get_data(as_text=True)
    assert '<form id=answer-form' not in page_html
    assert 'login to answer' in page_html


def test_question_answer_form_shown_when_logged_in(
    test_client, question, user
):
    response = test_client.get('/mind/question/test-question')

    page_html = response.get_data(as_text=True)
    assert '<form id=answer-form' in page_html
    assert 'login to answer' not in page_html


def test_answer_question(flask_app, test_client, question, user):
    with flask_app.app_context():
        question = db.session.merge(question)
        assert len(question.answers) == 0

    response = test_client.post(
        '/mind/question/test-question/answer',
        data={'answer': '1'})

    assert response.status_code == 302
    assert response.location.endswith('/mind/question/test-question')

    with flask_app.app_context():
        question = Question.query.get(question.id)
        assert len(question.answers) == 1


def test_answer_question_requires_login(flask_app, question):
    response = flask_app.test_client().post(
        '/mind/question/test-question/answer',
        data={'answer': '1'})

    assert response.status_code == 403

    with flask_app.app_context():
        question = db.session.merge(question)
        question = Question.query.get(question.id)
        assert len(question.answers) == 0


def test_answer_adds_flash_message(test_client, question, user):
    test_client.post(
        '/mind/question/test-question/answer',
        data={'answer': '1'})
    response = test_client.get('/mind/question/test-question')

    assert response.status_code == 200
    assert 'Answer added' in response.get_data(as_text=True)


def test_answer_question_when_logged_in(
    flask_app, test_client, question, user
):
    response = test_client.post(
        '/mind/question/test-question/answer',
        data={'answer': '1'})

    assert response.status_code == 302

    with flask_app.app_context():
        assert Answer.query.all()[0].email == 'example@example.org'
