class bank_account:
    def __init__(self , balance , int_rate =.02):
        self.balance = balance
        self.int_rate = int_rate
        
    def deposit(self, amount):
        self.balance += amount
        print(f'{amount} deposited, you now have {self.balance}')
        return self
        
    def withdraw(self,amount):
        self.balance -= amount
        print(f'{amount} has been withdrawn , you know have {self.balance}')
        
    def display_account_info(self):
        print (f'you have  ${self.balance}')
        return self
    
    def yield_interest(self):
        interest = self.balance * self.int_rate
        self.balance += interest
        print(f'interest is {interest}, and the new balance is {self.balance}')
            
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email 
        self.account = bank_account (int_rate=0.02, balance=0)

    def make_deposit(self, amount):
        self.account.deposit(amount)
        return self
    
    def make_withdraw(self, amount):
        self.account.withdraw(amount)
        return self
    
    def display_user_balance(self):
        self.account.display_account_info()
        return self
    
user_1=User('hasan','hasan.com')
user_1.make_deposit(1000).make_deposit(1500).make_withdraw(1000)
user_2=User('mike', 'mike.com')
user_2.make_deposit(800).make_withdraw(900).make_deposit(500)