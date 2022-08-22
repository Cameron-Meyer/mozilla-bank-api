import random
import re
import string

import pytest
from bank.schemas import Account


class TestAccount:
    def test_account_sets_name_without_amount(self):
        assert Account(name='I am a name').name == 'I am a name'

    def test_account_sets_amount_without_name(self):
        rand_amount = random.random()
        assert Account(amount=rand_amount).amount == rand_amount

    def test_account_sets_name_and_amount(self):
        rand_amount = random.random()
        rand_name = ''.join(random.choices(string.ascii_uppercase, k=20))
        account = Account(name=rand_name, amount=rand_amount)
        assert account.name == rand_name
        assert account.amount == rand_amount

    def test_amount_fails_if_not_float(self):
        assert Account(amount='0').amount == 0.0

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
