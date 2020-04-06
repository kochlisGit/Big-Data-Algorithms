# Locality-Sensitive Hashing (LSH)
LSH is an algorithm for finding similar items (pairs) in a large dataset. I have already uploaded a dataset with movies from kaggle,
which You can download and test the algorithm.
Imagine You have a very large number of documents stored in your computer (GBs) and You want to find similar pairs of those documents.
In our case, our dataset consists of users who watched movies. Users and movies have unique ids.

            user1   user2    user3   ....  userK
            
    movie1     1       1       0     ....    1
    
    movie1     0       0       1     ....    0
    
    movie1     0       0       1     ....    1
    
    .....     ....   .....   .....   ....  .....
    
    movie2
    
    movie2
    
    .....
   
    movieN
    
    movieN

Our goal is to find pairs of similar movies. 2 Movies our considered similar, If They have been seen by the same users.
The idea is that if 2 users watch, for example, a lot of "thrillers" and they have seen the same movie, then that movie is propably a thriller too.
This isn't very accurate hypothesis, but It is a good example to test this algorithm.

Naive Approach
1. Create the dense matrix (A binary matrix that consists of 0 and 1).
2. Compute the Jaccard Similarity between all movies. This takes time O(n^2)

The problem with this approach is that it takes a lot of time and RAM to create the dense matrix and also it takes too much time to find
all pairs.

LSH
LSH consists of 3 steps:
1. Shingling
2. Min-Hashing
3. Hashing signatures to buckets.

Shingling is the process, in which we convert our documents (movies) to vectors. For example the movie1 is a list with key = 1
and values = [1, 2, 5, 10, 40, 50, 300, 500, ...], where values are the ids of all users who have seen this movie.

Min-Hashing is the process, in which we reduce the dimensionality of every vector by randomly choosing signatures that represent those
vectors. A signature, could be for example a random subset of the users who have seen the movie. For example
movie1 = [1, 5, 10, 50, 300, 500]. And this is our signature for movie1.
Because creating random permuation takes too much time, I have also implemented a hash-function, which creates random permuations
very fast.

LSH is the final step of our algorithm. First it splits signatures to sub-signatures. Such an example could be
sub_sign1 = [1,5,10] and sub_sign2 = [50, 300, 500]. Then is assigns each sub-signature a unique number, which then hashes into a bucket.
The idea is that movies with same sub-signatures, might have a high Jaccard Similarity score. And that's enough to consider those 2 movies
as candidate pairs.

In our dataset, which is 2MB, it takes about 3 minutes in a normal laptop to calculate jaccard similarities of all movies.
LSH takes about a minute to find similar pairs of movies (Including Min-Hashing). Unfortunately, It doesn't find every possible pair.
It also returns a lot of false positives.
However, If your dataset is huge, most of the times You are interesting in finding similar pairs very quickly, rather than just finding
every possible pair.

You can find more information about the algorithm in https://en.wikipedia.org/wiki/Locality-sensitive_hashing
