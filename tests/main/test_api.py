import json
from unittest.mock import patch, ANY
from datetime import datetime, timedelta


from mind.app import db
from mind.models import Answer


def test_index(test_client):
    response = test_client.get('/api')

    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == {
        'send_reminders': 'http://localhost/api/send-reminders'}


def test_send_no_reminders_when_no_users(test_client):
    response = test_client.post('/api/send-reminders')

    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == {
        'message': 'Sent 0 reminders'}


def test_send_no_reminders_when_no_twitter_handle(test_client, user):
    response = test_client.post('/api/send-reminders')

    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == {
        'message': 'Sent 0 reminders'}


def test_send_no_reminders_when_up_to_date(
    flask_app, test_client, user_with_twitter, question
):
    with flask_app.app_context():
        question = db.session.merge(question)
        user = db.session.merge(user_with_twitter)
        answer = Answer(
            question=question,
            user=user,
            answer='5'
        )
        db.session.add(answer)
        db.session.commit()

    response = test_client.post('/api/send-reminders')

    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == {
        'message': 'Sent 0 reminders'}


@patch('mind.blueprints.api.twitter_client')
def test_send_reminder_when_no_latest_answer(
    mock_twitter_client, test_client, user_with_twitter
):
    response = test_client.post('/api/send-reminders')

    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == {
        'message': 'Sent 1 reminders'}
    mock_twitter_client.PostDirectMessage.assert_called_once_with(
        ANY, screen_name='example')


@patch('mind.blueprints.api.twitter_client')
def test_send_reminder_when_old_latest_answer(
    mock_twitter_client, flask_app, test_client, question, user_with_twitter
):
    with flask_app.app_context():
        question = db.session.merge(question)
        user = db.session.merge(user_with_twitter)
        answer = Answer(
            question=question,
            user=user,
            created_at=datetime.utcnow() - timedelta(days=2),
            answer='5'
        )
        db.session.add(answer)
        db.session.commit()

    response = test_client.post('/api/send-reminders')

    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == {
        'message': 'Sent 1 reminders'}
    mock_twitter_client.PostDirectMessage.assert_called_once_with(
        ANY, screen_name='example')
