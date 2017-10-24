
def test_index(test_client):
    response = test_client.get('/')

    assert response.status_code == 200
    assert 'OK' == response.get_data(as_text=True)


def test_mind_index(test_client):
    response = test_client.get('/mind')

    assert response.status_code == 302
    assert response.location.endswith('/mind/question/how-are-you-today')


def test_mind_static(test_client):
    response = test_client.get('/mind/static/js/init.js')

    assert response.status_code == 200


def test_mind_proxy_fix(test_client):
    response = test_client.get('/mind', headers={'X-Forwarded-Proto': 'https'})

    assert response.location.startswith('https://')
