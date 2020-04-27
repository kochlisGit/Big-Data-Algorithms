import hashfunclib as hashfl
import array
import sys

input_file_keys = 'Database/emails_reg_db.txt'
input_file_stream = 'Database/emails_stream.txt'
output_file = 'unregisted_emails.txt'

bitmap_size = 800000

hash_functions = [  lambda email: hashfl.crc32(email) % bitmap_size,
                    lambda email: hashfl.murmur3_32(email) % bitmap_size,
                    lambda email: hashfl.fnv_1a(email) % bitmap_size,
                    lambda email: hashfl.djb2(email) % bitmap_size,
                    lambda email: hashfl.sha256(email) % bitmap_size    ]

def read_file(input_file):
    with open(input_file) as txtfile:
        for line in txtfile:
            yield line.rstrip('\n')

def register_emails(email_file, bitmap_size):
    bitmap = array.array('b', [0]*bitmap_size)
    registered_emails = 0

    for email in read_file(email_file):
        registered_emails += 1
        for h in hash_functions:
            bucket = h(email)
            bitmap[bucket] = 1
    return bitmap, registered_emails

def count_bitmap_usage(bitmap):
    count = 0
    for value in bitmap:
        if value == 1:
            count += 1
    return (count / bitmap_size) * 100

def verify_email(bitmap, hash_functions, email):
    for h in hash_functions:
        bucket = h(email)
        if bitmap[bucket] == 0:
            return False
    return True

def filter_email_steam(stream_file, bitmap, hash_functions):
    verified_emails = 0
    unverified_emails = 0

    for email in read_file(stream_file):
        if verify_email(bitmap, hash_functions, email):
            verified_emails += 1
        else:
            unverified_emails += 1
    return verified_emails, unverified_emails

print('Registering keys to memory...')
bitmap, registered_emails = register_emails(input_file_keys, bitmap_size)

print('Number of emails registered in memory =', registered_emails)
print('Bitmap usage =', round(count_bitmap_usage(bitmap),3), '%')
print('Memory usage of bitmap =', round(sys.getsizeof(bitmap) / 2**20, 3), 'MB')

print('\nReading stream...')
verified_emails, unverified_emails = filter_email_steam(input_file_stream, bitmap, hash_functions)

print('Number of verified emails found =', verified_emails)
print('Number of unverified emails found =', unverified_emails)