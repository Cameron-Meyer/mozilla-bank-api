import random
import string

import pytest

from bank.schemas import Account


class TestAccount:
    def test_account_sets_name_without_balance(self):
        assert Account(name='I am a name').name == 'I am a name'

    def test_account_sets_name_and_balance(self):
        rand_balance = random.random()
        rand_name = ''.join(random.choices(string.ascii_uppercase, k=20))
        account = Account(name=rand_name, balance=rand_balance)
        assert account.name == rand_name
        assert account.balance == rand_balance

    def test_balance_fails_if_not_float(self):
        assert Account(name='inconsequential', balance='0').balance == 0.0

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
