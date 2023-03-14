import random


def generate_records_to_file(file_name,no_records):
    records = ''
    for i in range(no_records):

        record = str(complex(random.choice([i for i in range(-100,100) if i != 0]),random.choice([i for i in range(-100,100) if i != 0])))
        record += '\n'
        records += record


    with open(file_name + '_' + str(no_records) + '.txt', 'w') as file:
        file.write(records)



def complex_modulo(complex_record):
    return abs(complex_record)


