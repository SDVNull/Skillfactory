import random
import time


class Coord:

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f'({self.x}, {self.y})'


class Ship:

    def __init__(self):
        self.length = (3, 2, 2, 1, 1, 1, 1) # Количество и размерность кораблей
        self.aura = ((0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)) # Список соседних клеток

    # Проверка возможности разместить корабль
    def aura_ships(self, ships_field, dot, len_ship, direction):
        x, y = dot.x + 1, dot.y + 1
        count = 0
        for i in range(len_ship):
            for _x, _y in self.aura:
                if ships_field[x + _x][y + _y] == '■':
                    count = 1
            if direction == -1:
                x += 1  # Направление вниз
            else:
                y += 1  # Направление вправо
        if count == 0:
            return True


class Game:
    def __init__(self):
        self.ship = Ship()
        self.board = Board()

    def start(self):
        self.tutorial()
        brd, comp, user = Board(), Comp(), User()
        comp.board = brd.finally_create()
        user.board = brd.finally_create()
        while True:
            brd.draw(comp.board, comp.name)
            brd.draw(user.board, user.name)
            user.shot(comp.board)
            comp.shot(user.board)

    @staticmethod  # PyCharm захотел статический метод:-)
    def tutorial():
        print("-" * 27)
        print(" " * 8 + "МОРСКОЙ БОЙ")
        print("-" * 27)


class Player:
    def __init__(self):
        self.name = None
        self.board = None


class Comp(Player):
    def __init__(self):
        super().__init__()
        self.name = 'Компьютер'
        self.crd = Coord(0, 0)

    healthpoints = 11

    def shot(self, board):
        while True:
            self.crd.x, self.crd.y = random.randint(1, 6), random.randint(1, 6)
            if board[self.crd.x][self.crd.y] in ['*', 'X']:
                continue
            break
        if board[self.crd.x][self.crd.y] == '■':
            board[self.crd.x][self.crd.y] = 'X'
            print('Искусственный интеллект поразил цель')
            User.healthpoints -= 1
            if User.healthpoints == 0:
                print('ИИ победил!')
                exit()
        elif board[self.crd.x][self.crd.y] == 0:
            board[self.crd.x][self.crd.y] = '*'
            print('Искусственный интеллект ошибся')
        time.sleep(1)


class User(Player):
    def __init__(self):
        super().__init__()
        self.name = 'Игрок'
        self.crd = Coord(0, 0)

    healthpoints = 11

    def shot(self, board):
        while True:
            shot = input('Введите координаты цели (x,y) через пробел ')
            try:
                self.crd.x, self.crd.y = int(shot.split()[0]), int(shot.split()[1])
                if self.crd.x and self.crd.y in range(0, 7):
                    if board[self.crd.x][self.crd.y] in ['*', 'X']:
                        print('Вы уже сюда стреляли, повторите ввод')
                        continue
                    break
            except IndexError:
                print('Введите корректные значения')
                continue
            except ValueError:
                print('Введите корректные значения')
                continue
        if board[self.crd.x][self.crd.y] == '■':
            board[self.crd.x][self.crd.y] = 'X'
            print('Результат хода игрока - Попадание')
            Comp.healthpoints -= 1
            if Comp.healthpoints == 0:
                print('Игрок победил!')
                exit()
        elif board[self.crd.x][self.crd.y] == 0:
            board[self.crd.x][self.crd.y] = '*'
            print('Результат хода игрока - Промах')
        time.sleep(0.5)


class Board:
    def __init__(self, size=8):
        self.ships_field = None
        self.size = size
        self.ship = Ship()

    # После нескольких неудачных попыток перезапуска генерации игрового поля
    # воспользовался сторонним решением (4 строчки кода и проблема решена):
    def finally_create(self):
        brd = None
        while brd is None:
            brd = self.board_try_to_create(self.ship)
        return brd

    def board_try_to_create(self, ship):
        # Создание списка 8*8 заполненного нулями
        # self.ships_field = [[0 for j in range(self.size)] for i in range(self.size)]
        # Но так лаконичнее:
        self.ships_field = [[0] * 8 for _ in range(8)]
        trying = 0
        for len_ship in ship.length:
            while True:
                count = 0
                # Генерация случайного направления для установки корабля (по оси Х или У)
                direction = random.choice([-1, 1])
                # Получение случайных координат
                dot = Coord(random.randint(0, 5), random.randint(0, 5))
                # Проверяем, хватит ли размера доски при направлении корабля по оси Y
                if direction == -1 and (dot.x + len_ship <= self.size - 2):
                    if ship.aura_ships(self.ships_field, dot, len_ship, direction):
                        count += 2
                # Проверяем, хватит ли размера доски при направлении корабля по оси Х
                if direction == 1 and (dot.y + len_ship <= self.size - 2):
                    if ship.aura_ships(self.ships_field, dot, len_ship, direction):
                        count += 2
                # Проверяем, чтобы стартовая ячейка для отрисовки корабля была пустая
                if self.ships_field[dot.x + 1][dot.y + 1] == 0:
                    count += 1
                # При выполнении трех условий, выход из цикла
                if count == 3:
                    break
                # Опытным путем установленно, что поле 6*6 со всеми элементами создается в среднем до 100 попыток
                # Если попыток больше, запускаем цикл заново, экономим производительность
                trying += 1
                if trying > 99:
                    return None

            for i in range(len_ship):
                self.ships_field[dot.x + 1][dot.y + 1] = '■'
                if direction == -1:
                    dot.x += 1  # Направление вниз
                else:
                    dot.y += 1  # Направление вправо

        return self.ships_field

    # Вывод игровых полей, поле компьютера маскируется
    def draw(self, board, name):
        print(f'  Игровое поле {name}а')
        print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i in range(self.size - 2):
            print(i + 1, '', end='|')
            for j in range(self.size - 2):
                if name == 'Компьютер':
                    print('', board[i + 1][j + 1] if board[i + 1][j + 1] in ['X', '*'] else '○', '', end='|')
                else:
                    print('', board[i + 1][j + 1], '', end='|')
            print()
        print()


s = Game()
s.start()
