from mind.app import db
from mind.models import Question


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


def test_answer_question(flask_app, question):
    with flask_app.app_context():
        question = db.session.merge(question)
        assert len(question.answers) == 0

    response = flask_app.test_client().post(
        '/mind/question/test-question/answer',
        data={'answer': '1'})

    assert response.status_code == 302
    assert response.location.endswith('/mind/question/test-question')

    with flask_app.app_context():
        question = Question.query.get(question.id)
        assert len(question.answers) == 1


def test_answer_adds_flash_message(test_client, question):
    test_client.post(
        '/mind/question/test-question/answer',
        data={'answer': '1'})
    response = test_client.get('/mind/question/test-question')

    assert response.status_code == 200
    assert 'Answer added' in response.get_data(as_text=True)
