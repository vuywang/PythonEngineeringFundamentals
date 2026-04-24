class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f'{self.name}正在汪汪叫')

dog = Dog('加辉', 2)
dog.bark()

class Phone:
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price

    def show_info(self):
        print(f'brand: {self.brand}, price: {self.price}')

phone = Phone("苹果", 9999)
phone.show_info()

class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def read(self):
        print(f'正在阅读 {self.title}')

book = Book("小王子", "不认识", "100")
book.read()

class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        print(f'正在存款 {amount}')
        if amount <= 0:
            print('存款金额必须大于0')
            return
        self.balance += amount
        print(f'存款成功，当前余额为 {self.balance}')

    def withdraw(self, amount):
        if amount <= 0:
            print("取款金额必须大于0")
            return
        if self.balance < amount:
            print("余额不足")
            return
        self.balance -= amount
        print(f'取款成功，当前余额为 {self.balance}')

account = Account("vuy", 100000000)
account.deposit(10000)
account.withdraw(5000)
account.withdraw(10000000000)

class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Dog(Animal):
    def __init__(self,name, age):
        super().__init__(name, age)

    def bark(self):
        print(f"{self.name} 正在狗叫")

dog = Dog("加辉", 18)
dog.bark()

