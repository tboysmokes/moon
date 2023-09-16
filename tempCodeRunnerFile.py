from faker import Faker
import random
import datetime

fake = Faker()

def generate_transaction():
    date = fake.date_between(start_date='-1y', end_date='today')
    description = fake.sentence()
    amount = round(random.uniform(1, 1000), 2)
    account = fake.credit_card_number(card_type='mastercard')
    return {
        'date': date,
        'description': description,
        'amount': amount,
        'account': account
    }

transactions = [generate_transaction() for _ in range(100)]  # Generate 100 random transactions

for transaction in transactions:
    print(transaction)
