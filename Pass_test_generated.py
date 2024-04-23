def test_strong_password_checker(strong_password_checker):
    assert strong_password_checker("abcdef") == 0
    assert strong_password_checker("abcdefghi") == 0
    assert strong_password_checker("abcdefghij") == 0
    assert strong_password_checker("abcdefghijk") == 0
    assert strong_password_checker("abcdefghijkl") == 0
    assert strong_password_checker("abcdefghijklm") == 0

