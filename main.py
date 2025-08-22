def user_input():
    while True:
        user_column = input('Enter column number\n')
        try:
            user_column = int(user_column)
            return user_column
        except ValueError:
            print('Please enter a valid column number')


def main():
    column_number = user_input()
    print(column_number)


if __name__ == '__main__':
    main()