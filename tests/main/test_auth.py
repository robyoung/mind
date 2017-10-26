from unittest.mock import patch

from flask import session


@patch('mind.blueprints.mind.google')
def test_login(mock_google, test_client):
    mock_google.authorize.return_value = 'redirect'

    test_client.get('/mind/login')

    mock_google.authorize.assert_called_with(
        callback='https://localhost/mind/oauth2-callback')


@patch('mind.blueprints.mind.google')
def test_authorisation_failure(mock_google, test_client):
    mock_google.authorized_response.return_value = None

    resp = test_client.get('/mind/oauth2-callback?' +
                           'error_reason=bad&' +
                           'error_description=badbad')

    assert resp.status_code == 401
    assert 'Access denied: reason=bad error=badbad' == \
        resp.get_data(as_text=True)
    assert 'google_token' not in session
    assert 'user_info' not in session
    assert not mock_google.get.called


@patch('mind.blueprints.mind.google')
def test_authorisation(mock_google, test_client):
    mock_google.authorized_response.return_value = dict(
        access_token='access-token')
    mock_google.get.return_value.data = dict(
        email='email@example.org',
        given_name='Example')

    resp = test_client.get('/mind/oauth2-callback')

    assert resp.status_code == 302
    assert session['google_token'] == ('access-token', '')
    assert session['user_info'] == {
        'email': 'email@example.org',
        'given_name': 'Example',
    }
    assert session.permanent


@patch('mind.blueprints.mind.google')
def test_logout(mock_google, test_client):
    with test_client.session_transaction() as sess:
        sess['google_token'] = 'irrelevant'
        sess['user_info'] = 'irrelevant'

    resp = test_client.get('/mind/logout')

    assert resp.status_code == 302
    assert resp.location == 'http://localhost/mind'
    assert 'google_token' not in session
    assert 'user_info' not in session
