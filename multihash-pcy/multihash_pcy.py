import csv
import array
import itertools
import sys

input_file = 'Database/transactions.csv'
num_of_buckets = 100000
support = 750

# Returns memory usage of this process in bytes.
def memory_footprint(*stored_varlist):
    total_bytes = 0
    for var in stored_varlist:
        total_bytes += sys.getsizeof(var)
    return total_bytes

# Read transactions from data.
def read_transactions(input_file):
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for transaction in reader:
            yield transaction

# The first Hash Function used to Map itemsets (id1, id2, ... idN) to buckets.
# bucketid = (id1 * id2 * ... * idN) % num_of_buckets.
def hashFunc1(itemset, num_of_buckets):
    product = 1
    for itemId in itemset:
        product *= itemId
    return product % num_of_buckets

# The second Hash Function used to Map itemsets (id1, id2, ... idN) to buckets.
# bucketid = (id1 + id2 + ... + idN) % num_of_buckets.
def hashFunc2(itemset, num_of_buckets):
    return sum(itemset) % num_of_buckets

# Returns a binary array (0-1) from a Hashtable.
# 0 --> A bucket is not frequent.
# 1 --> A bucket is frequent.
def generateBitmap(hashTable, support, num_of_buckets):
    for i in range(num_of_buckets):
        if hashTable[i] < support:
            hashTable[i] = 0
        else:
            hashTable[i] = 1
    return array.array('B', hashTable)

# Returns a set of all frequent items.
def filter_items(itemList, support):
    frequent_items = set()
    for item, count in itemList.items():
        if count >= support:
            frequent_items.add(item)
    return frequent_items

# First pass of multihash pcy. During the first pass:
# 1. It counts frequency of each item in the dataset.
# 2. It hashes every pair that appears in the dataset to 2 hashtables.
def first_pass(transactions, num_of_buckets):
    itemList = dict()
    hashTable1 = [ 0 for i in range(num_of_buckets) ]
    hashTable2 = [ 0 for i in range(num_of_buckets) ]

    for basket in transactions:
        size = len(basket)
        for i in range(size):
            item1 = int( basket[i] )
            if item1 in itemList:
                itemList[item1] += 1
            else:
                itemList[item1] = 1
            
            for j in range(i+1, size):
                item2 = int( basket[j] )
                hashId1 = hashFunc1( [item1, item2], num_of_buckets )
                hashTable1[hashId1] += 1
                hashId2 = hashFunc2( [item1, item2], num_of_buckets )
                hashTable2[hashId2] += 1
    return itemList, hashTable1, hashTable2

# Maps every k-plet in the dataset in 2 different hashtables.
def map_k_itemsets(transactions, k, num_of_buckets):
    hashTable1 = [ 0 for i in range(num_of_buckets) ]
    hashTable2 = [ 0 for i in range(num_of_buckets) ]

    for basket in transactions:
        items = sorted( list( map(int, basket) ) )
        for itemset in itertools.combinations(items, k):
            hashId1 = hashFunc1(itemset, num_of_buckets)
            hashTable1[hashId1] += 1
            hashId2 = hashFunc2(itemset, num_of_buckets)
            hashTable2[hashId2] += 1
    return hashTable1, hashTable2

# Counts every k-itemset in the database.
# An itemset I={I1, I2, ..., IN} is counted if:
# 1. I1, I2, ..., IN are frequent items.
# 2. I is hashed in frequent buckets in both hashtables.
def count_k_itemsets(transactions, k, frequent_items, bitmap1, bitmap2, num_of_buckets):
    candidate_itemsets = dict()
    for basket in transactions:
        items = sorted( list( map(int, basket) ) )
        for itemset in itertools.combinations(items, k):
            items_are_frequent = True
            for item in itemset:
                if not item in frequent_items:
                    items_are_frequent = False
                    break
            if items_are_frequent:
                hashId1 = hashFunc1(itemset, num_of_buckets)
                if bitmap1[hashId1] == 1:
                    hashId2 = hashFunc2(itemset, num_of_buckets)
                    if bitmap2[hashId2] == 1:
                        if itemset in candidate_itemsets:
                            candidate_itemsets[itemset] += 1
                        else:
                            candidate_itemsets[itemset] = 1
    return candidate_itemsets

# Implementation of multihash pcy algorithm.
# Finds all frequnt k-itemsets in the database.
# It requires 2 passes for each k = 2, 3, ..., N, N
# Iterations stop if the number of frequent k-itemsets is less than k + 1.
def multihash_pcy(input_file, support, num_of_buckets):
    print('Running 1st pass - Counting frequent items...')

    itemList, hashTable1, hashTable2 = first_pass(read_transactions(input_file), num_of_buckets)

    print( 'Memory usage in Bytes:', memory_footprint(itemList, hashTable1, hashTable2) )
    print('Filtering data...')

    frequent_items = filter_items(itemList, support)
    del itemList
    bitmap1 = generateBitmap(hashTable1, support, num_of_buckets)
    del hashTable1
    bitmap2 = generateBitmap(hashTable2, support, num_of_buckets)
    del hashTable2

    print( '\nMemory usage in Bytes after filtering:', memory_footprint(frequent_items, bitmap1, bitmap2) )
    print( 'Number of frequent items in the dataset =', len(frequent_items) )

    k = 2
    frequent_sets = set()
    while True:
        print('Counting itemsets for k =', k)

        candidate_itemsets = count_k_itemsets(read_transactions(input_file), k, frequent_items, bitmap1, bitmap2, num_of_buckets)
        frequent_itemsets = filter_items(candidate_itemsets, support)

        print( 'Number of frequent itemsets found in pass', k, '=', len(frequent_itemsets) )

        if len(frequent_itemsets) < k + 1:
            for itemset in frequent_itemsets:
                frequent_sets.add(itemset)
            break
        else:
            frequent_sets = frequent_sets.union(frequent_itemsets)
            k += 1
            del candidate_itemsets
            del frequent_itemsets

            print('\nMapping itemsets for k =', k)

            hashTable1, hashTable2 = map_k_itemsets(read_transactions(input_file), k, num_of_buckets)
            bitmap1 = generateBitmap(hashTable1, support, num_of_buckets)
            del hashTable1
            bitmap2 = generateBitmap(hashTable2, support, num_of_buckets)
            del hashTable2
    return frequent_items.union(frequent_sets)

frequent_itemsets = multihash_pcy(input_file, support, num_of_buckets)

print( 'Number of frequent itemsets =', len(frequent_itemsets) )
print(frequent_itemsets)