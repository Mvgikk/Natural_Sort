from generator import *
from tape import Tape
from buffer import Buffer

runs = 1
disk_reads = 0
disk_writes = 0
sort_phases = 0




def natural_sort(file_path, buffer_size, show_tape):
    global runs, disk_reads, disk_writes, sort_phases
    runs = 1
    disk_reads = 0
    disk_writes = 0
    sort_phases = 0

    input_file_tape = Tape(file_path)
    print(f"Input file before sort : \n{input_file_tape.get_tape_content_with_modulos()}\n")

    distribution_tape1 = Tape('distribution_tape1.tape')
    distribution_tape2 = Tape('distribution_tape2.tape')

    merge_tape = Tape('merge_tape.tape')

    input_file_buffer = Buffer(buffer_size, input_file_tape)

    distribution_buffers = []
    distribution_buffer1 = Buffer(buffer_size, distribution_tape1)
    distribution_buffer2 = Buffer(buffer_size, distribution_tape2)
    distribution_buffers.append(distribution_buffer1)
    distribution_buffers.append(distribution_buffer2)

    merge_buffer = Buffer(buffer_size, merge_tape)

    input_file_buffer.clear_buffer()
    distribution_buffer1.clear_buffer()
    distribution_buffer2.clear_buffer()
    merge_buffer.clear_buffer()

    file_sorted = False

    while not file_sorted:

        distribution_phase(input_file_buffer, merge_buffer, distribution_buffers)
        file_sorted = merging_phase(merge_buffer, distribution_buffers)

        if show_tape:
            print(f"Phase number: {sort_phases}")
            print(f"Distribution tape 1 : \n{distribution_tape1.get_tape_content_with_modulos()}\n"
                  f"Distribution tape 2 : \n{distribution_tape2.get_tape_content_with_modulos()}\n"
                  f"Merge Tape: \n{merge_tape.get_tape_content_with_modulos()} \n")

        sort_phases += 1




    return [runs, disk_writes, disk_reads, sort_phases]

def distribution_phase(input_file_buffer, merge_buffer,distribution_buffers):
    global runs, disk_reads, disk_writes, sort_phases

    previous_record = None

    first_record = True


    if sort_phases == 0:

        merge_buffer = input_file_buffer

    else:

        merge_buffer = merge_buffer


    merge_buffer.tape.open_file(False)
    distribution_buffers[0].tape.open_file(True)
    distribution_buffers[1].tape.open_file(True)

    current_buffer = 0

    while not merge_buffer.end_of_tape:

        merge_buffer.get_records_from_tape()
        disk_reads += 1


        while not merge_buffer.is_empty():
            #pierwszy rekord
            if first_record:

                current_record = merge_buffer.get_record()

                wrote_to_file = distribution_buffers[current_buffer].append_record_to_buffer(current_record)

                previous_record = current_record

                first_record = False

            else:

                current_record = merge_buffer.get_record()

                if complex_modulo(current_record) >= complex_modulo(previous_record):
                        #aktualny rekord wiekszy wiec dodanie do bufora nadal ta sama seria
                    wrote_to_file = distribution_buffers[current_buffer].append_record_to_buffer(current_record)

                    previous_record = current_record

                else:
                    # kolejny rekord wiekszy
                    # zmiana bufora

                    current_buffer = (current_buffer + 1) % 2
                    #pierwsza faza zliczanie seri
                    if sort_phases == 0:
                        runs += 1

                    wrote_to_file = distribution_buffers[current_buffer].append_record_to_buffer(current_record)

                    previous_record = current_record
            if wrote_to_file:
                disk_writes += 1

    if not distribution_buffers[0].is_empty():
        distribution_buffers[0].write_records()
        disk_writes += 1

    if not distribution_buffers[1].is_empty():
        distribution_buffers[1].write_records()
        disk_writes += 1

    merge_buffer.tape.close_file()
    distribution_buffers[0].tape.close_file()
    distribution_buffers[1].tape.close_file()

    merge_buffer.reset_end_of_tape()
    distribution_buffers[0].reset_end_of_tape()
    distribution_buffers[1].reset_end_of_tape()


def merging_phase(merge_buffer,distribution_buffers):

        global runs, disk_reads, disk_writes, sort_phases



        merge_buffer.tape.open_file(True)
        distribution_buffers[0].tape.open_file(False)
        distribution_buffers[1].tape.open_file(False)

        distribution_buffers[0].reset_end_of_tape()
        distribution_buffers[1].reset_end_of_tape()

        distribution_buffers[0].get_records_from_tape()
        distribution_buffers[1].get_records_from_tape()
        disk_reads += 2

        record1 = distribution_buffers[0].get_record()
        record2 = distribution_buffers[1].get_record()


        file_sorted = True

        finish_tape1 = False
        finish_tape2 = False

        if complex_modulo(record1) > complex_modulo(record2):

            merge_buffer.append_record_to_buffer(record2)
            previous = record2
            record2 = distribution_buffers[1].get_record()
        else:

            merge_buffer.append_record_to_buffer(record1)
            previous = record1
            record1 = distribution_buffers[0].get_record()

        while True:
            #prv <= r1 i prv <= r2
            if complex_modulo(previous) <= complex_modulo(record1) and complex_modulo(previous) <= complex_modulo(record2):

                if complex_modulo(record1) < complex_modulo(record2):

                    if merge_buffer.append_record_to_buffer(record1):
                        disk_writes += 1

                    previous = record1

                    if distribution_buffers[0].is_empty():

                        distribution_buffers[0].get_records_from_tape()
                        disk_reads += 1

                        if distribution_buffers[0].is_empty():
                            finish_tape2 = True
                            break

                    record1 = distribution_buffers[0].get_record()
                # r1 > r2
                else:

                    if merge_buffer.append_record_to_buffer(record2):
                        disk_writes += 1

                    previous = record2

                    if distribution_buffers[1].is_empty():

                        distribution_buffers[1].get_records_from_tape()
                        disk_reads += 1

                        if distribution_buffers[1].is_empty():
                            finish_tape1 = True
                            break

                    record2 = distribution_buffers[1].get_record()
            #r2 < prv < r1
            elif complex_modulo(record1) >= complex_modulo(previous) > complex_modulo(record2):

                file_sorted = False
                if merge_buffer.append_record_to_buffer(record1):
                    disk_writes += 1

                previous = record1

                if distribution_buffers[0].is_empty():

                    distribution_buffers[0].get_records_from_tape()
                    disk_reads += 1

                    if distribution_buffers[0].is_empty():
                        finish_tape2 = True
                        break

                record1 = distribution_buffers[0].get_record()

            #r1<prv<r2
            elif complex_modulo(record1) < complex_modulo(previous) <= complex_modulo(record2):

                file_sorted = False
                if merge_buffer.append_record_to_buffer(record2):
                    disk_writes += 1

                previous = record2

                if distribution_buffers[1].is_empty():

                    distribution_buffers[1].get_records_from_tape()
                    disk_reads += 1

                    if distribution_buffers[1].is_empty():
                        finish_tape1 = True
                        break

                record2 = distribution_buffers[1].get_record()


            else:
                # r1<r2<prv
                if complex_modulo(record1) < complex_modulo(record2):

                    if merge_buffer.append_record_to_buffer(record1):
                        disk_writes += 1

                    previous = record1

                    if distribution_buffers[0].is_empty():

                        distribution_buffers[0].get_records_from_tape()
                        disk_reads += 1

                        if distribution_buffers[0].is_empty():
                            finish_tape2 = True
                            break

                    record1 = distribution_buffers[0].get_record()
                #r2<r1<prv
                else:

                    if merge_buffer.append_record_to_buffer(record2):
                        disk_writes += 1

                    previous = record2

                    if distribution_buffers[1].is_empty():

                        distribution_buffers[1].get_records_from_tape()
                        disk_reads += 1

                        if distribution_buffers[1].is_empty():
                            finish_tape1 = True
                            break

                    record2 = distribution_buffers[1].get_record()

        if finish_tape2:

            while True:

                if complex_modulo(previous) > complex_modulo(record2):
                    file_sorted = False

                merge_buffer.append_record_to_buffer(record2)

                if distribution_buffers[1].is_empty():
                    distribution_buffers[1].get_records_from_tape()
                    disk_reads += 1

                if distribution_buffers[1].is_empty():
                    break

                record2 = distribution_buffers[1].get_record()

        elif finish_tape1:

             while True:

                if complex_modulo(previous) > complex_modulo(record1):
                    file_sorted = False

                merge_buffer.append_record_to_buffer(record1)


                if distribution_buffers[0].is_empty():
                    distribution_buffers[0].get_records_from_tape()
                    disk_reads += 1

                if distribution_buffers[0].is_empty():
                    break

                record1 = distribution_buffers[0].get_record()

        if not merge_buffer.is_empty():
            merge_buffer.write_records()
            disk_writes += 1

        merge_buffer.tape.close_file()
        distribution_buffers[0].tape.close_file()
        distribution_buffers[1].tape.close_file()

        merge_buffer.reset_end_of_tape()
        distribution_buffers[0].reset_end_of_tape()
        distribution_buffers[1].reset_end_of_tape()

        return file_sorted
