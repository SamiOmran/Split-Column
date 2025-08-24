import csv
import os


class CSVHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.header = []
        self.body = []

        self.read_csv()

    def read_csv(self):
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f'File {self.file_path} not found')

            with open(self.file_path) as csvfile:
                # read csv lines
                csv_reader = csv.reader(csvfile)

                # handle header
                end_header = ['</HEADER>']
                header_row = next(csv_reader)

                while header_row != end_header:
                    self.header.append(header_row)
                    header_row = next(csv_reader)
                self.header.append(end_header)

                # handle body
                self.body = list(csv_reader)
                self._fix_body()

        except Exception as e:
            print(f'Error reading CSV file: {e}')
            raise e

    def _fix_body(self):
        # 1. remove empty rows
        self.body = [row for row in self.body if row]

        length = len(self.body)
        for i in range(length):
            # 2. expand rows  ['PROG9;5;224259;;3066398'] =>  ['PROG9', '5', '224259', '', '3066398']
            self.body[i] = self.body[i][0].split(';')

            # 3. replace empty values with 'NA'
            self.body[i] = ['NA' if not item.strip() else item.strip()
                            for item in self.body[i]]

        # # 4. remove duplicates
        self.body = [list(row) for row in {tuple(row) for row in self.body}]

    def _groupby_column_number(self, column_number):
        '''
        function takes column number, returns dictionary with keys are column number 
        and its value a list of all rows with same index value
        '''
        dictionary = dict()
        body_tags = [['</BOD>'], ['<BOD>']]

        for row in self.body:
            if row not in body_tags:
                # check if row != body_tags to avoid exception
                key = row[column_number]
                found = dictionary.get(key)

                if not found:
                    dictionary[key] = [row]
                else:
                    dictionary[key].append(row)

        return dictionary

    def _create_file(self, path, content):
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            full_file = self.header + [['<BOD>']] + content + [['</BOD>']]
            writer.writerows(full_file)

    def split_file(self, column_number):
        dictionary = self._groupby_column_number(column_number)
        os.makedirs('output', exist_ok=True)

        for key, val in dictionary.items():
            i = 1
            if len(val) < 300:
                output_file = f'output/datafile_{key}.csv'
                self._create_file(output_file, val)
            else:
                while len(val) > 0:
                    chunk = val[:300]
                    val = val[300:]
                    output_file = f'output/datafile_{key}_part_{i}.csv'
                    i += 1
                    self._create_file(output_file, chunk)
