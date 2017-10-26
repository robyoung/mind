from mind.models import User


def test_update_settings(flask_app, test_client, logged_in_user):
    response = test_client.post(
        '/mind/settings',
        data={'twitter_handle': 'example'})

    assert response.status_code == 302

    with flask_app.app_context():
        user = User.query.all()[0]
        assert user.twitter_handle == 'example'
