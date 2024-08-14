def correct_input():  # Просто принт
    print('Введите верное значение: ')


def arr():  # Создание пустого списка на 9 ячеек
    global num_arr
    num_arr = [['-' for j in range(0, 3)] for i in range(0, 3)]


def game_table():  # Мегаграфическое исполнение игрового поля
    print('\t\t\t\t 0 1 2\n' +
          f'\t\t\t 0 | {num_arr[0][0]} {num_arr[0][1]} {num_arr[0][2]} |\n' +
          f'\t\t\t 1 | {num_arr[1][0]} {num_arr[1][1]} {num_arr[1][2]} |\n' +
          f'\t\t\t 2 | {num_arr[2][0]} {num_arr[2][1]} {num_arr[2][2]} |\n')


def start_game_priority():  # Выбор начала игры
    while True:
        try:
            start = int(input('Начало игры, за кем будет первый ход?:\n'
                              '(Нажмите 1 если начинают Крестики)\n'
                              '(Нажмите 2 если начинают Нолики)\n'
                              '>>> '))
            if start not in [1, 2]:
                correct_input()
                continue
            return start
        except ValueError:
            correct_input()


def player_input():  # Ввод значений на игровое поле
    move_flag = True if s == 1 else False
    count_move = 1
    while True:
        try:
            print(f'Ход № {count_move} очередь Крестиков' if move_flag
                  else f'Ход № {count_move} очередь Ноликов')
            x = int(input('Введите значение по горизонтали (0,1,2): '))
            y = int(input('Введите значение по вертикали (0,1,2): '))
            print('=' * 42)
            if x not in [0, 1, 2] or y not in [0, 1, 2]:
                correct_input()
                game_table()
                continue
            if num_arr[x][y] == '-':
                num_arr[x][y] = 'X' if move_flag else 'O'
                game_table()
                count_move += 1
                if count_move >= 5:
                    vin_condition('X') if move_flag else vin_condition('O')
                if count_move == 10:
                    print('Ничья')
                    exit()
                move_flag = not move_flag
                continue
            else:
                game_table()
                print('***Ячейка занята, выберите другое значение***')
                continue
        except ValueError:
            correct_input()
            game_table()
            continue


def vin_condition(ox):  # Определение победной комбинации
    vin_col, vin_row, vin_game = '', '', False
    for i in range(len(num_arr)):  # Проверка строк
        if ''.join(num_arr[i]) == ox * 3:
            vin_game = True
        for j in range(len(num_arr[i])):  # Проверка столбцов
            vin_col += num_arr[j][i]
            if vin_col == ox * 3:
                vin_game = True
            if j == 2:
                vin_col = ''
    if num_arr[1][1] + num_arr[0][2] + num_arr[2][0] == ox * 3 or\
            num_arr[1][1] + num_arr[0][0] + num_arr[2][2] == ox * 3: # Проверка диагоналей
        vin_game = True
    if vin_game:
        print('Крестики победили' if ox == 'X' else 'Нолики победили')
        end_game()


def end_game():
    print('Игра окончена')
    exit()


num_arr = []
s = start_game_priority()
arr()
game_table()
player_input()
