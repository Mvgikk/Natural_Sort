import generator
class Tape:

    def __init__(self,file_name):
        self.file_name = file_name
        self.file = None
        self.pos = 0

        try:
            self.file = open(file_name,'r+')
            self.file.close()
        except:
            self.file = open(file_name,'x')
            self.file.close()


    def __del__(self):
        self.file.close()
        self.file = None
        self.pos = 0


    def open_file(self,overwrite):
        if overwrite:
            self.file = open(self.file_name, 'w+')
        else:
            self.file = open(self.file_name, 'r+')


    def close_file(self):
        self.file.close()


    def get_tape_content_with_modulos(self):
        content = ''

        with open(self.file_name, "r") as file:
            while True:
                record = file.readline()
                if record == '':
                    break
                record = record.strip()
                complex_record = complex(record)
                content += record + ' ' + str(generator.complex_modulo(complex_record)) + '\n'
                if not record:
                    break

        return content



    def write_records_on_tape(self,records):
        s_rec = ''

        for record in records:
            s_rec += str(record) + '\n'

        self.file.write(s_rec)
        self.pos = self.file.tell()

    def get_n_records_from_tape(self,n):
        n_records = []

        for _ in range(n):
            record = self.file.readline()
            if record != "":
                record = record.strip()
                record = complex(record)
                n_records.append(record)

        return n_records

