from policy.utils import available_language_codes


def test_available_language_codes():
    codes = available_language_codes()
    # ensure there's actually stuff in there
    assert codes
    # check some random languages
    assert 'en' in codes
    assert 'fr' in codes
    assert 'de' in codes
    # check all the codes are 2 letters long
    assert all(len(code) == 2 for code in codes)
    # check they all have names
    assert all(codes.values())
