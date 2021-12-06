import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount

# provide list of tuples to test the function with
@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])

# naming of function matters for auto-discovery by pytest; as does filenaming
# testing with parameters above
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1 , num2) == expected

def test_subtract():
    print("testing subtract function")
    assert subtract(3,2) == 1

def test_multiply():
    print("testing multiply function")
    assert multiply(2,3) == 6

def test_divide():
    print("testing divide function")
    assert divide(6,3) == 2


###############################################################################

def test_bank_set_initial_amount():
    # create a new bank account instance
    bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount():
    bank_account = BankAccount()
    assert bank_account.balance == 0

def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.withdraw(10)
    assert bank_account.balance == 40

def test_depost():
    bank_account = BankAccount(50)
    bank_account.deposit(10)
    assert bank_account.balance == 60

def test_collect_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 55

