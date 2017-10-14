
def test_list_questions(test_client):
    response = test_client.get('/question')

    assert response.status_code == 200


def test_show_non_existent_question(test_client):
    response = test_client.get('/question/not-there')

    assert response.status_code == 404


def test_show_question(test_client, question):
    response = test_client.get('/question/test-question')

    assert response.status_code == 200
    assert 'Test question' in response.get_data(as_text=True)


def test_answer_question(test_client, question):
    # import ipdb; ipdb.set_trace()
    assert len(question.answers) == 0

    response = test_client.post(
        '/question/test-question/answer',
        data={'answer': '1'})

    assert response.status_code == 302
    assert response.location.endswith('/question/test-question')
    assert len(question.answers) == 1
