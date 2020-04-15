import csv
import random as rand

input_file = 'items.csv'
output_file_ids = 'transactions.csv'
output_file_baskets = 'baskets.csv'

num_of_transactions = 50000
num_of_items = 500
min_items = 5
max_items = 55

num_of_important_items = int(num_of_items / 5)
important_items_frequency = 0.8
num_of_customers = int(num_of_transactions / 50)
num_of_customers_items = num_of_important_items + min_items + max_items

# Reads items from csv file.
# Each item consists of id (key) and a name (value).
def read_items(csv_file, num_of_items):
    itemMap = {}
    pid = 0

    with open(csv_file, 'r', encoding = 'utf-8') as csvfile:
        item_reader = csv.DictReader(csvfile)
        next(item_reader)
        for row in item_reader:
            itemMap[pid] = row['Name']
            pid += 1
            if pid == num_of_items:
                break
    return itemMap

# Write transactions in file.
# A transaction is a basket (list) of items (ids).
# Each row contains a basket.
def write_transactions(csv_file, transactions):
    with open(csv_file, 'w', newline = '\n') as csvfile:
        transaction_writer = csv.writer(csvfile)
        for basket in transactions:
            transaction_writer.writerow(basket)

# Writes baskets in file.
# A basket is a list of items (names).
# Each row contains a basket.
def write_baskets(csv_file, transactions, itemMap):
    with open(csv_file, 'w', encoding = 'utf-8', newline = '\n') as csvfile:
        basket_writer = csv.writer(csvfile)
        for basket_ids in transactions:
            basket = []
            for i in basket_ids:
                basket.append( itemMap[i] )
            basket_writer.writerow(basket)

# Generate random customers with random item preferences.
# Each customer prefers random items.
# Each customer also prefers important items
def generate_customers(itemMap, num_of_items,
                        num_of_customers, num_of_customers_items,
                        num_of_important_items, important_items_frequency):
    important_items = rand.sample(itemMap.keys(), num_of_important_items)
    customers = []

    for i in range(num_of_customers):
        basket = []
        for item in important_items:
            r = rand.uniform(0.0, 1.0)
            if r <= important_items_frequency:
                basket.append(item)
        for j in range(num_of_customers_items):
            pid = rand.randint(0, num_of_items - 1)
            while pid in basket:
                pid = rand.randint(0, num_of_items - 1)
            basket.append(pid)
        customers.append(basket)
    return customers

def generate_transactions(customers, num_of_customers,
                        num_of_transactions, min_items, max_items):
    transactions = []

    for i in range(num_of_transactions):
        r = rand.randint(min_items, max_items)
        c = rand.randint(0, num_of_customers - 1)
        basket = rand.sample(customers[c], r)
        transactions.append(basket)
    return transactions

print('\nSTEP 1: Reading items from database...')

itemMap = read_items(input_file, num_of_items)

print( 'Number of items read:', len(itemMap) )
print('\nSTEP 2: Generating customers')

customers = generate_customers(itemMap, num_of_items,
                                num_of_customers, num_of_customers_items,
                                num_of_important_items, important_items_frequency)

print( 'Number of customer generated:', len(customers) )
print('\nSTEP 3: Generating random transactions...')

transactions = generate_transactions(customers, num_of_customers,
                                    num_of_transactions, min_items, max_items)

print( 'Number of transactions generated:', len(transactions) )
print('\nSTEP3: Writing transactions to files...')
print('STEP5: Writing baskets to files...')

write_transactions(output_file_ids, transactions)
write_baskets(output_file_baskets, transactions, itemMap)

print('\nDone')