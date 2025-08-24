import shutil
import sys

from src.csv_handler import CSVHandler


def user_input():
    '''
    user_input handles user input from command line to get the column number
    returns: column number as int
    '''
    while True:
        user_column = input('Enter column number between 1 and 5:\n')
        try:
            user_column = int(user_column)
            if 1 <= user_column <= 5:
                return user_column - 1 # for list index
            else:
                print('Column number must be between 1 and 5.')
        except ValueError:
            print('Please enter a valid number.')


def handle(column_number):
    try:
        file_path = sys.argv[1]
        csv_file = CSVHandler(file_path)

        csv_file.split_file(column_number)

    except IndexError as e:
        print('Make sure you pass file path!')
        raise (e)


def main():
    column_number = user_input()
    handle(column_number)

    clear_data = input('Delete output files Y/N ?')
    if clear_data.upper() == 'Y':
        shutil.rmtree('output/')


if __name__ == '__main__':
    main()
