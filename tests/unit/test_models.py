def test_new_account_with_fixture(new_account):
    """
    Given an Account db.Model
    When a new Account is created
    Then check the username, email, password_hash, and stock fields are defined correctly
    """
    assert new_account.username == 'matt'
    assert new_account.email == 'mgriffes@example.com'
    assert new_account.password_hash == '123'
    assert new_account.stocks == 'aapl'