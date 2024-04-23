def test_number_to_words(number_to_words):
    assert number_to_words(123456789000) == "One Hundred Twenty Three Billion Four Hundred Fifty Six Million Seven Hundred Eighty Nine Thousand"
    assert number_to_words(123456789000000) == "One Hundred Twenty Three Trillion Four Hundred Fifty Six Billion Seven Hundred Eighty Nine Million"
    assert number_to_words(900) == "Nine Hundred"
    assert number_to_words(1000) == "One Thousand"
    assert number_to_words(40000) == "Forty Thousand"
