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
                raise FileNotFoundError(f"File '{self.file_path}' not found")

            with open(self.file_path) as csvfile:
                # read csv lines
                csv_reader = csv.reader(csvfile)

                # handle header
                end_header = '</HEADER>'
                header_row = next(csv_reader)

                while header_row[0] != end_header:
                    self.header.extend(header_row)
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
            self.body[i] = ['NA' if not item.strip() else item.strip() for item in self.body[i]]

        # # 4. remove duplicates
        self.body = [list(row) for row in {tuple(row) for row in self.body}]
 
    def split_file(self, column_number):
        pass
