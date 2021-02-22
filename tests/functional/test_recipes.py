def test_home_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Financial Application!" in response.data
    assert b"Existing Users: Log In" in response.data
    assert b"New Users: Sign Up" in response.data


def test_home_page_post_with_fixture(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post('/')
    assert response.status_code == 405
    assert b"Welcome to the Financial Application!" not in response.data