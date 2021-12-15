import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

# pass -x to find only failed tests (stops after first failure)

# test fixture example which can be resued in multiple tests
@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

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

def test_bank_set_initial_amount(bank_account):
    # create a new bank account instance
    # bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40

def test_depost(bank_account):
    bank_account.deposit(10)
    assert bank_account.balance == 60

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 55

# combine multiple tests into one
def test_bank_transactions(zero_bank_account):
    zero_bank_account.deposit(100)
    zero_bank_account.withdraw(25)
    assert zero_bank_account.balance == 75

# combine parameters and fixures into tests
@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 400, 800)
])

def test_bank_transactions_with_parameters(zero_bank_account,deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(zero_bank_account):
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(200)

