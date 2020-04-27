# Bloom Filter
I have implemented a simple bloom filter used to filter registered emails from different email providers.
I used 5 different hash functions for that purpose.

# Description
Bloom Filter is one of the most simpliest and most effective ways of filtering items through a stream. Suppose that You have an email provider company (e.g. gmail). One of the most important tasks You have to do is filter Unverified (Spam) emails for your clients. There are **billions of Verified emails and billions of Unverified emails coming through a stream every second.** Also, new emails are created every day, by thousands of users, from different email providers.

# Naive Approach
The naive approach to solving this problem would be to simply construct a HashTable (Dictionary) and hash all verified email addresses (Probably billions of emails). Also, because HashTables are extendable objects, You could update it every day, by hashing more verified emails to the HashTable everyday. So, before sending an email to a user, You need to filter it's sender's address and make sure It's verified. If it is verified then It should be sent at receiver's inbox. If not, It should be sent at the receiver's spam folder.

The problem with this approach is that:

1. You need 4 bytes to store a key (hashcode), which is an integer from 1 to N, where N is the size of the HashTable.
2. You need at least (minimum) 24 bytes to store an email address.

The earth is populated by approx. 10 billion people. Suppose each of them has a personal email address, which is verified.
You would need (24+4) * 10^10 Bytes = 280GB of memory. Also, there are people who use more than 1 email addresses. So, You will definetely need a lot of RAM.

# Bloom Filters
Instead of using 10 billion of emails, we will use a bitmap (An array of bits with value 0/1) of size 100 billion. We only need 1 byte per bit cell, so we will use only 100GB of memory. We will generate a bucket (Integer) for every verified email address and set the value of that bucket in the bitmap to 1. We will use 5 different hash functions to generate 5 different buckets for that email. 

For every new email that is coming through the stream, generate a 5 hashcodes with the same hash functions used during the training phase. If bitmap[hashcode] = 1 for every hashcode generated, then the email is verified with very high probability.

# Hash Functions
I have created 5 different hash functions, which generate a hashcode for strings. These hash functions have been said to have the least collisions.
1. CRC32
2. Murmur32
3. fnv1a
4. djb2
5. sha256

The implementation for all the above hash functions are in the file "hashfunclib.py"

# Experiment
I have generated 10000 verified email addresses and i have created a 800000 size stream (textfile), which contains all the 10000 verified emails and the rest are randomly generated email addresses. The goal of bloom filter is to read every email address from the stream and accept only those 10000. By using the above 5 Hash Functions and a bitmap of 1000000 size. It accepted 10001..!
