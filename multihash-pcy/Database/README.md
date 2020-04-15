# Transactions Generator

I've made this generator, in order to create random real-world transactions, so I can test the algorithm. The generator uses a dataset with over 100.000 real world supermarket items (**items.csv**). Each item contains a unique UPC (Universal Product Code) as it would on a supermarket. A UPC code (or Barcode) is a 12-digit number, which we use to identify our items. However, storing a 12-digit number consumes too bytes on the disk. To reduce the size of the file, I assign the product a unique ID (0 - 104000) and create the transaction's file (**transactions.csv**). Each Transaction is a row of ids (items). e.g.:

        1.    5, 10, 3, 500, 4, 600
        2.    3, 2, 4, 56, 57, 900
        3.    2, 1, 500, 56, 68, 9
        4.    ....................
        ..........................
        ..........................
        
# Real-World Datasets.

We would like to generate a real-world supermarket dataset, in order to find item pairs. The algorithm that creates the transactions uses the following rules:

1. The Supermarket has standard customers.
2. Customers have a list of unique items (products) of the supermarket, which they prefer to buy. Lists for every customer are pre-defined. The items are selected randomly from the dataset.
3. Additionally, there are some necessary (Important) items in the supermarket, which customers also add to their baskets with a high probability:

        Customer1: [Random Important Items ... Other Random Items from the dataset]
        Customer2: [Random Important Items ... Other Random Items from the dataset]
        Customer3: [Random Important Items ... Other Random Items from the dataset]
        ..........................................................
        
4. In each iteration, we select a random customer, from which we select a random subset of the products he prefers.

In that way, items in baskets don't follow a simple uniform distributed probability. Because the important items have a high propability of appearing in each customer's basket, the transaction's file is more likely to have more frequent itemsets.
