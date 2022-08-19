import re

import pytest
from bank.schemas import Account


class TestAccount:
    def test_raise_value_error_if_name_is_missing(self):
        # Can't override the default None check
        with pytest.raises(ValueError, match=re.escape('field required (type=value_error.missing)')):
            Account()

    def test_raise_value_error_if_name_is_empty(self):
        with pytest.raises(ValueError, match="field required, but is either empty or pure whitespace"):
            Account(name='')

    def test_raise_value_error_if_name_is_all_whitespace(self):
        with pytest.raises(ValueError, match="field required, but is either empty or pure whitespace"):
            Account(name='             ')

    def test_raise_value_error_if_name_contains_special_characters_or_digits(self):
        with pytest.raises(ValueError, match="field contains non-alpha and non-whitespace characters"):
            # Non-exhaustive, just a sanity check. Would have to dynamically generate a test for every special char
            Account(name='I, John FireFox, D0th Declare, !@#$%^&*()_+-=[]{}\\|,.<>?/')
