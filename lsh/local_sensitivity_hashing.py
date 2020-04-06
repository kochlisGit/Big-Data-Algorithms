# Implementation of LSH with Min-Hashing in a movies Dataset.

import csv
import numpy as np
import random as rand
import time

ratings_filepath = 'D:\\ratings.csv'
user_id_column = 0
movie_id_column = 1

# Reads data line by line. Doesn't import data to memory.
def read_next_entry(filepath):
    with open(filepath) as datafile:
        entry_file = csv.reader(datafile, delimiter = ',')
        for entry in entry_file:
            yield entry

# Reads data from ratings file and adds them to list
# movieMap: Stores an index in the dense matrix for each movie.
# MovieList: Stores users that have seen that movie.
def read_data(filepath):
    movieMap = {}
    movieList = {}
    users = set()
    index = 0

    iter_entries = read_next_entry(filepath)
    next(iter_entries)
    for entry in iter_entries:
        userId = int( entry[user_id_column] )
        movieId = int( entry[movie_id_column] )
        if movieId in movieMap:
            movieList[movieId].append(userId)
        else:
            movieMap[movieId] = index
            movieList[movieId] = [userId]
            index += 1
        users.add(userId)

    return movieMap, movieList, len(users)

# Finds Jaccard similarity between 2 sets.
def jaccard_similarity(movie1, movie2):
    s1 = set(movie1)
    s2 = set(movie2)
    return len( s1.intersection(s2) ) / len( s1.union(s2) )

# Creates universal functions based on a very large prime number and number of documents.
def create_universal_function(p = 2**33-355, m = 2**32-1):
    a = rand.randint(1, p-1)
    b = rand.randint(0, p-1)
    return lambda x: 1 + ( ( (a * x + b) % p ) % m )

def create_random_permutation(hashFunc, size):
    permutations = {}

    for i in range(size+1):
        permutations[i] = hashFunc(i)
    return permutations

# Implementation of min-hashing algorithm for our movieList.
# For every movie, It creates a signature.
def min_hashing(movieMap, movieList, num_of_docs, n):
    num_of_movies = len(movieMap)
    signature_matrix = np.full( (n, num_of_movies), num_of_docs )

    for p in range(n):
        hashFunc = create_universal_function(m = num_of_docs)
        permutations = create_random_permutation(hashFunc, num_of_docs)
        for movieId, movieUsers in movieList.items():
            for userId in movieUsers:
                signature = permutations[userId]
                movieIndex = movieMap[movieId]
                if signature < signature_matrix[p][movieIndex]:
                    signature_matrix[p][movieIndex] = signature
    return signature_matrix

# Computes the similarity between 2 signatures.
def signature_similarity(signature_matrix, movieMap, movieId1, movieId2, n_rows):
    sign1_col = signature_matrix[ :, movieMap[movieId1] ]
    sign2_col = signature_matrix[ :, movieMap[movieId2] ]
    sign1 = sign1_col[0 : n_rows]
    sign2 = sign2_col[0 : n_rows]
    return jaccard_similarity(sign1, sign2)

# Convert vector of each band to unique numbers
def get_unique_number(sign_vector):
    return int( ''.join( map(str,sign_vector) ) )

# Returns candidate pairs for buckets.
# Candidate pairs our considered 2 documents whose one of sub-signatures are hashed at least in one same bucket.
def get_candidate_pairs(band_buckets):
    candidate_pairs = set()

    for bucket_list in band_buckets.values():
        bucket_size = len(bucket_list)
        for i in range(bucket_size):
            for j in range(i+1, bucket_size):
                candidate_pairs.add( ( bucket_list[i], bucket_list[j] ) )
    return candidate_pairs

# Implementation of Locality-Sensitive Hashing on our Signature Matrix.
# It returns a list of candidate pairs of similar movies.
def locality_sensitive_hashing(signature_matrix, bands, rows):
    candidate_pairs = set()

    hashFunc = create_universal_function()
    for b in range(bands):
        band_bucket = {}
        for col in range( len(signature_matrix) ):
            signature = signature_matrix[:, col]
            sub_sign = signature[b*rows : b*rows + rows]
            unique_number = get_unique_number(sub_sign)
            hash_value = hashFunc(unique_number)
            if hash_value in band_bucket:
                band_bucket[hash_value].append(col)
            else:
                band_bucket[hash_value] = [col]
        bucket_pairs = get_candidate_pairs(band_bucket)
        candidate_pairs = candidate_pairs.union(bucket_pairs)
        
    return candidate_pairs

# Compute TP, FP, FN, TN, Precision, Recall, F1.
def compute_metrics(similar_pairs, pairs_suggested, similar_pairs_found, size):
    true_positives = similar_pairs_found
    false_positives = pairs_suggested - true_positives
    false_negatives = similar_pairs - true_positives
    true_negatives = int( ( size*(size - 1) )/2 - true_positives - false_positives - false_negatives)

    if true_positives == 0:
        precision = 0
        recall = 0
        f1 = 0
    else:
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)
        f1 = 2*recall*precision/( recall + precision )

    return true_positives, false_positives, false_negatives, true_negatives, precision, recall, f1

# Print metrics.
def print_metrics(tp, fp, fn, tn, prec, rec, f1):
    print('\nTrue Positives:', tp, '\nFalse Positives:', fp)
    print('False Negatives:', fn, '\nTrue Negatives:', tn)
    print('Precision:', prec)
    print('Recal:', rec)
    print('F1 Score:', f1)

def main():
    print('Extracting data...')

    start_time = time.time()
    movieMap, movieList, num_of_users = read_data(ratings_filepath)
    end_time = time.time()

    print( '\nTotal movies extracted:', len(movieMap) )
    print( 'Total users extracted:', num_of_users)
    print('Time for extracting data:', round(end_time - start_time, 2), 'seconds')

    threshold = 0.5
    movieIds = list( movieMap.keys() )
    num_of_keys = len(movieIds)
    similar_pairs = set()

    print('\nComputing Jaccard similarities of movies with at least', threshold, 'similarity...')

    start_time = time.time()
    for i in range(num_of_keys):
        for j in range(i+1, num_of_keys):
            movieId1 = movieIds[i]
            movieId2 = movieIds[j]
            if jaccard_similarity( movieList[movieId1], movieList[movieId2] ) >= threshold:
                similar_pairs.add( ( movieMap[movieId1], movieMap[movieId2] ) )
    end_time = time.time()
    num_of_similar_pairs = len(similar_pairs)

    print( '\nNumber of similar movies using jaccard similarity =', num_of_similar_pairs)
    print('Execution time for computing similarities of all movies is', round(end_time - start_time, 2), 'seconds')

    print('\nConstructing signature matrix...')

    n = 100
    start_time = time.time()
    signature_matrix = min_hashing(movieMap, movieList, num_of_users, n)
    end_time = time.time()

    print(signature_matrix)
    print('Signature Matrix shape:', signature_matrix.shape)
    print('Time for constructing signature matrix:', round(end_time - start_time, 2), 'seconds')

    print('\nHashing signatures to buckets...')

    bands_n_rows = {25: 4, 20:5, 14:7, 10:10}
    for b, r in bands_n_rows.items():
        print( '\nTrying for bands =', b, 'and rows =', r, 'with s =', (1/b)**(1/r) )

        start_time = time.time()
        candidate_pairs = locality_sensitive_hashing(signature_matrix, b, r)
        end_time = time.time()

        print('Execution time:', round(end_time - start_time, 2), 'seconds')

        num_of_candidates_suggested = len(candidate_pairs)
        num_of_similar_pairs_found = len( similar_pairs.intersection(candidate_pairs) )
        tp, fp, fn, tn, prec, rec, f1 = compute_metrics( num_of_similar_pairs,
                                                            num_of_candidates_suggested,
                                                            num_of_similar_pairs_found,
                                                            len(movieMap) )
        print_metrics(tp, fp, fn, tn, prec, rec, f1)


if __name__ == '__main__':
    main()
