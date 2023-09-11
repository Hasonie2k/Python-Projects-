class BankAccount:
    all_accounts = []

    def __init__(self, interest_rate, balance=0):
        self.interest_rate = interest_rate
        self.balance = balance
        self.__class__.all_accounts.append(self)

    def deposit(self, amount):
        self.balance += amount
        return self

    def withdraw(self, amount):
        if self.balance < amount:
            print("Insufficient funds: charging a $5 fee")
            self.balance -= 5
        else:
            self.balance -= amount
        return self

    def display_account_info(self):
        print(f"Balance: {str(self.balance)}")
        return self

    def yield_interest(self):
        self.balance += self.balance * self.interest_rate
        return self

    @classmethod
    def print_all_accounts_info(cls):
        for account in cls.all_accounts:
            account.display_account_info()

account1 = BankAccount(0.07, 1000)
account2 = BankAccount(0.04, 500)

account1.deposit(5000).deposit(1000).withdraw(800).yield_interest().display_account_info

account2.deposit(2500).deposit(500).withdraw(2000).withdraw(100).yield_interest().display_account_info

BankAccount.print_all_accounts_info()
