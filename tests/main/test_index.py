
def test_index(test_client):
    response = test_client.get('/')

    assert response.status_code == 301
    assert response.location.endswith('/question/how-are-you-feeling')
