# Multihash PCY (Park Chen Yu) Algorithm

PCY algorithm is an improvement of A-Priory algorithm. We have also added the **Multihash** optimization in the implementation.
PCY finds frequent itemsets by making several passes over a dataset. 

1. In the first pass, It keeps track of the occurrences of each singleton (It counts how many each individual item appears in the dataset).
Addionally, it hashes pairs that appear in the dataset to 2 different HashTables. 

2. After the 1st pass, We filter our singetons (We keep only the frequent items of our dataset). To decide if an item is frequent, we
define a threshold (**support**) for each time. If an item appears in the dataset more than the threshold, then it's considered frequent.
We also filter HashTables by converting them to bitmaps. 

3. In the second pass, we count the candidate pairs. An pair {i, j} I is counted if the following conditions are met:

        A. Both i and j are frequent items.
        B. {i, j} is hashed in a frequent bucket in both hashtables.
        
In that way, we reduce the number of counters we have to count, so we dramatically reduce the memory used in our program.
Unfortunately, the execution time is expensive, but the memory usage is low. Supermarkets might have millions of transactions with
thousands of products. So, we need to keep the memory usage low, if we'd like to find every possible frequent itemset in the dataset.

# Hash Functions
We use 2 different hash functions to hash k-plets to 2 different hash-tables. Since our items are integer numbers, we use the following
hash functions:

1st Hash Function is: (i1 * i2 * ... * iN) % num_of_buckets
2nd Hash Function (i1 + i2 + ... + iN) % num_of_buckets

You can find more information about the algorithm here: https://medium.com/weekly-data-science/the-pcy-algorithm-and-its-friends-ecba67216190
