def test_strong_password_checker(strong_password_checker):
    assert strong_password_checker('7230C4B18649a4Aa') == 0
    assert strong_password_checker('7230C4B18649a4Aa') == 0
    assert strong_password_checker('7230C4B18649a4Aa') == 0
    assert strong_password_checker('B2b9c9AB50c32444b46') == 1
    assert strong_password_checker('6235B79cB7637C1ABC') == 0
    assert strong_password_checker('95c0004bB318B5623a2') == 1
    assert strong_password_checker('6235B79cB7637C1ABC') == 0
    assert strong_password_checker('03CcB2a35954A1cabBB5') == 0
    assert strong_password_checker('03CcB2a35954A1cabBB5') == 0
    assert strong_password_checker('03CcB2a35954A1cabBB5') == 0
