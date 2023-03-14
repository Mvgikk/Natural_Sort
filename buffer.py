

class Buffer:


    def __init__(self, size, tape):
        self.size = size
        self.tape = tape
        self.records = []
        self.end_of_tape = False

    def __del__(self):
        self.clear_buffer()

    def clear_buffer(self):
        self.records = []


    def reset_end_of_tape(self):
        self.end_of_tape = False

    def get_records_from_tape(self):

        self.records = [record for record in self.tape.get_n_records_from_tape(self.size)]

        if len(self.records) < self.size:
            self.end_of_tape = True

    def write_records(self):
        self.tape.write_records_on_tape(self.records)
        self.clear_buffer()

    def append_record_to_buffer(self, record):
        if not self.is_full():
            self.records.append(record)
            #if buffer not full didnt write to tape
            return False

        else:
            self.write_records()
            self.records.append(record)
            return True
            #buffer full wrote to file

    def get_record(self):
        record = self.records[0]
        self.records = self.records[1:]
        return record

    def is_full(self):
        return len(self.records) >= self.size

    def is_empty(self):
        return len(self.records) == 0
