import csv
import time

# Reads data line by line. Returns the next entry its time It is called.
# Only 1 line of data is imported to memory.
def read_data(csv_file):
    with open(csv_file, 'r') as input_file:
        reader = csv.reader(input_file, delimiter = ',')
        for entry in reader:
            yield entry

# Write results to disk.
# Results will be written in 2 seperate files.
def write_data(csv_file, entries_dict, column_names):
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames = column_names)
        writer.writeheader()
        for entry_key, r in entries_dict.items():
            writer.writerow( { column_names[0] : entry_key, column_names[1] : round(r[0], 2) } )

# Update average ratings for each movie and user. Ratings are not stored in memory.
# Average rating is updated each time as: avg_r = avg_r + (rating - avg_r) / N
def update_average_ratings(entries_dict, i, rating):
    if i in entries_dict:
        r = entries_dict[i]
        avg = r[0]
        N = r[1] + 1
        entries_dict[i] = (avg + (float(rating) - avg)/N, N)
    else:
        entries_dict[i] = (float(rating), 1)

input_file = 'Database/ratings_big.csv'
output_file_users = 'users_average_ratings.csv'
output_file_movies = 'movies_average_ratings.csv'
userId_col = 0
movieId_col = 1
rating_col = 2

usersDict = {}
moviesDict = {}

start_time = time.time()

entry_gen = read_data(input_file)
next(entry_gen)

for entry in entry_gen:
    update_average_ratings( usersDict, int( entry[userId_col] ), entry[rating_col] )
    update_average_ratings( moviesDict, int( entry[movieId_col] ), entry[rating_col] )

write_data( output_file_users, usersDict, ['userId', 'avgRating'] )
write_data( output_file_movies, moviesDict, ['movieId', 'avgRating'] )

end_time = time.time()

print( 'Users processed:', len(usersDict) )
print( 'Movies processed:', len(moviesDict) )
print('Execution time is', end_time - start_time, 'seconds.')
