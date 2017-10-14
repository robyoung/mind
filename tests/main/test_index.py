
def test_index(test_client):
    response = test_client.get('/')

    assert response.status_code == 200
    assert 'OK' == response.get_data(as_text=True)


def test_mind_index(test_client):
    response = test_client.get('/mind')

    assert response.status_code == 301
    assert response.location.endswith('/mind/question/how-are-you-feeling')
