import random

# Класс точка на поле
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # сравнение точек
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Ship:
    def __init__(self, x, y, direction, length=1):
        # длинна коробля
        self.length = length
        # координаты носа коробля (объект класса Dot)
        self.first = Dot(x, y)
        # направление коробля (горизонтальное или вертикальное)
        self.direction = direction
        # количество жизней корабля
        self.health = length

    # возвращение списка, содержащего координаты коробля (объекты класса Dot, в свою очередь состоящие из координат x и y)
    def dots(self):
        dots = [self.first]
        # если корабль больше 1 клетки, рассчитываются все координаты
        if self.length > 1:
            # если корабль горизонтальный, список с координатами дополняется списком с изменением второго значения
            if self.direction == 1:
                i = 1
                while i < self.length:
                    dots.append(Dot(self.first.x, self.first.y + i))
                    i += 1

            # если корабль вертикальный, список с координатами дополняется списком с изменением первого значения
            else:
                i = 1
                while i < self.length:
                    dots.append(Dot(self.first.x + i, self.first.y))
                    i += 1
        return dots


class Board:
    def __init__(self, hid=False):
        # поле с содержанием информации о каждой клетке
        self.field = [['О', 'О', 'О', 'О', 'О', 'О'],
                      ['О', 'О', 'О', 'О', 'О', 'О'],
                      ['О', 'О', 'О', 'О', 'О', 'О'],
                      ['О', 'О', 'О', 'О', 'О', 'О'],
                      ['О', 'О', 'О', 'О', 'О', 'О'],
                      ['О', 'О', 'О', 'О', 'О', 'О']]
        # список кораблей на доске
        self.ships = []
        # сокрытие кораблей на доске
        self.hid = hid
        # количество живых кораблей
        self.lively_ships = 0
        # список всех точек на поле
        self.all_dots = []
        for horizon in range(6):
            for verical in range(6):
                self.all_dots.append(Dot(horizon, verical))

    # добавление кораблей
    def add_ship(self, ship):
        # проверка на возможность размещения
        # если корабль трехпалубный
        if ship.length == 3:
            try:
                if self.field[ship.dots()[0].x][ship.dots()[0].y] == 'О' \
                        and self.field[ship.dots()[1].x][ship.dots()[1].y] == 'О' \
                        and self.field[ship.dots()[2].x][ship.dots()[2].y] == 'О':
                    self.field[ship.dots()[0].x][ship.dots()[0].y] = '■'
                    self.field[ship.dots()[1].x][ship.dots()[1].y] = '■'
                    self.field[ship.dots()[2].x][ship.dots()[2].y] = '■'
                    # в случае успеха корабль сохраняется в список
                    self.ships.append(ship)
                    # корабль обводится по контуру
                    self.contour(ship)
                else:
                    self.add_ship(ship)
            except IndexError:
                self.add_ship(ship)
        # если корабль двухпалубный
        elif ship.length == 2:
            try:
                if self.field[ship.dots()[0].x][ship.dots()[0].y] == 'О' \
                        and self.field[ship.dots()[1].x][ship.dots()[1].y] == 'О':
                    self.field[ship.dots()[0].x][ship.dots()[0].y] = '■'
                    self.field[ship.dots()[1].x][ship.dots()[1].y] = '■'
                    # в случае успеха корабль сохраняется в список
                    self.ships.append(ship)
                    # корабль обводится по контуру
                    self.contour(ship)
                else:
                    self.add_ship(ship)
            except IndexError:
                self.add_ship(ship)
        # если корабль однопалубный
        elif ship.length == 1:
            try:
                if self.field[ship.dots()[0].x][ship.dots()[0].y] == 'О':
                    self.field[ship.dots()[0].x][ship.dots()[0].y] = '■'
                    # в случае успеха корабль сохраняется в список
                    self.ships.append(ship)
                    # корабль обводится по контуру
                    self.contour(ship)
                else:
                    self.add_ship(ship)
            except IndexError:
                self.add_ship(ship)

    # обвод корабля по контуру
    def contour(self, ship):
        # переменный с координатами первой точки
        horizon = ship.first.x
        vertical = ship.first.y
        # если корабль горизонтальный из первой точки вычитается 1, проставляются 3 отметки по вертикали, если эти точки существуют (включены в список всех точек поля)
        if ship.direction == 1:
            if Dot(horizon, vertical - 1) in self.all_dots:
                self.field[horizon][vertical - 1] = 'T'
            if Dot(horizon - 1, vertical - 1) in self.all_dots:
                self.field[horizon - 1][vertical - 1] = 'T'
            if Dot(horizon + 1, vertical - 1) in self.all_dots:
                self.field[horizon + 1][vertical - 1] = 'T'
            # далее для каждой точки корабля проверяется наличие соседних по вертикали,при наличии выставляются отметки
            for dot in ship.dots():
                if Dot(dot.x + 1, dot.y) in self.all_dots:
                    self.field[dot.x + 1][dot.y] = 'T'
                if Dot(dot.x - 1, dot.y) in self.all_dots:
                    self.field[dot.x - 1][dot.y] = 'T'
            # далее к первой точке добавляется длинна коробля, проставляются 3 отметки по вертикали, если эти точки существуют
            for dot in self.all_dots:
                if Dot(horizon, vertical + ship.length) in self.all_dots:
                    self.field[horizon][vertical + ship.length] = 'T'
                    for dot in self.all_dots:
                        if Dot(horizon - 1, vertical + ship.length) in self.all_dots:
                            self.field[horizon - 1][vertical + ship.length] = 'T'
                    for dot in self.all_dots:
                        if Dot(horizon + 1, vertical + ship.length) in self.all_dots:
                            self.field[horizon + 1][vertical + ship.length] = 'T'

        # если корабль вертикальный, действия аналогичны вышеописанным (использована несколько иная схема сравнения)
        else:
            for dot in self.all_dots:
                if dot == Dot(horizon - 1, vertical):
                    self.field[horizon - 1][vertical] = 'T'
                    for dot in self.all_dots:
                        if dot == Dot(horizon - 1, vertical - 1):
                            self.field[horizon - 1][vertical - 1] = 'T'
                    for dot in self.all_dots:
                        if dot == Dot(horizon - 1, vertical + 1):
                            self.field[horizon - 1][vertical + 1] = 'T'
            # далее получается список всех точек корабля, и для каждой проверяется наличие соседних по вертикали,при наличии выставляются отметки
            for dot in ship.dots():
                if Dot(dot.x, dot.y + 1) in self.all_dots:
                    self.field[dot.x][dot.y + 1] = 'T'
                if Dot(dot.x, dot.y - 1) in self.all_dots:
                    self.field[dot.x][dot.y - 1] = 'T'
            # далее к первой точке добавляется длинна коробля, проставляются отметки по вертикали, если эти точки существуют
            for dot in self.all_dots:
                if dot == Dot(horizon + ship.length, vertical):
                    self.field[horizon + ship.length][vertical] = 'T'
                for dot in self.all_dots:
                    if dot == Dot(horizon + ship.length, vertical - 1):
                        self.field[horizon + ship.length][vertical - 1] = 'T'
                for dot in self.all_dots:
                    if dot == Dot(horizon + ship.length, vertical + 1):
                        self.field[horizon + ship.length][vertical + 1] = 'T'

    # вывод доски
    def __str__(self):
        return f'    1    2    3    4    5    6 \n' \
               f'1   {self.field[0][0]}    {self.field[0][1]}    {self.field[0][2]}    {self.field[0][3]}    {self.field[0][4]}    {self.field[0][5]} \n' \
               f'2   {self.field[1][0]}    {self.field[1][1]}    {self.field[1][2]}    {self.field[1][3]}    {self.field[1][4]}    {self.field[1][5]} \n' \
               f'3   {self.field[2][0]}    {self.field[2][1]}    {self.field[2][2]}    {self.field[2][3]}    {self.field[2][4]}    {self.field[2][5]} \n' \
               f'4   {self.field[3][0]}    {self.field[3][1]}    {self.field[3][2]}    {self.field[3][3]}    {self.field[3][4]}    {self.field[3][5]} \n' \
               f'5   {self.field[4][0]}    {self.field[4][1]}    {self.field[4][2]}    {self.field[4][3]}    {self.field[4][4]}    {self.field[4][5]} \n' \
               f'6   {self.field[5][0]}    {self.field[5][1]}    {self.field[5][2]}    {self.field[5][3]}    {self.field[5][4]}    {self.field[5][5]}'

    # выстрел
    def shot(self, dot):
        # проверка на выстрел за пределы поля
        try:
            # точка уже прострелена
            if self.field[dot.x][dot.y] == 'T' or self.field[dot.x][dot.y] == 'X':
                print('Точка уже поражена')
                return True
            # попадание
            # перебор списка кораблей и поиск точки выстрала в списке точек кораблей
            for ship in self.ships:
                if dot in ship.dots():
                    print('Попадание!')
                    self.field[dot.x][dot.y] = 'X'
                    # При попадании здоровье корабля уменьшается на 1
                    ship.health -= 1
                    if ship.health == 0:
                        # При снижении здоровья коробля до 0 он обводится контуром и колчиество живых кораблей на доске снижается на 1
                        print('Корабль уничтожен')
                        self.lively_ships = self.lively_ships - 1
                        self.contour(ship)
                    #     если все корабли уничтожены, цикл прирывается
                        if self.lively_ships == 0:
                            print('Победа!')
                            break
                    return True
            # промах
            else:
                self.field[dot.x][dot.y] = 'X'
                print('промах!')
        except IndexError:
            print("Ты куда лупасишь?!?!")
            return True

# класс игрока
class Player:
    def __init__(self):
        self.my_board = None
        self.its_board = None

    # определение координат для выстрела
    def ask(self):
        pass

    # ход в игре
    def move(self):
        pass

class AI(Player):
    def __init__(self):
        self.my_board = 'Game.random_board()'

    # определение координат для выстрела
    def move(self, board):
        if board.shot(Dot(random.randint(0, 5), random.randint(0, 5))) == True:
            self.move(board)

class User(Player):
    # определение координат для выстрела
    def ask(self):
        xshot = int(input("Введите строку для выстрела ")) - 1
        yshot = int(input("Введите столбец для выстрела ")) - 1
        return Dot(xshot, yshot)

    # ход в игре
    def move(self, board):
        try:
            if board.shot(self.ask()) == True:
                print(board)
                self.move(board)
        except ValueError:
            print('Неверный формат координат, давай еще раз.')
            self.move(board)
class Game:
    def __init__(self):
        self.user = User()
        self.user_board = Board()
        self.ai = AI()
        self.ai_board = Board(True)

    # генерация доски
    def random_board(self, board, i=7):
        i -= 1
        if i > 0:
            self.random_board(board, i)

        # создается объект класса корабль
        def create_ship():
            # в зависимости от шага определяется длинна коробля
            if i == 0:
                l = 3
            elif 0 < i < 3:
                l = 2
            else:
                l = 1

            # генерация направления коробля
            if i < 3:
                directiona = random.randint(1, 2)
            else:
                directiona = 1

            # генерируется первая точка коробля
            xa, ya = random.randint(1, 6), random.randint(1, 6)

            # генерируется корабль
            return Ship(xa - 1, ya - 1, directiona, l)

        def instal_ship(a):
            # проверка на возможность размещения
            # если корабль трехпалубный
            if a.length == 3:
                try:
                    if board.field[a.dots()[0].x][a.dots()[0].y] == 'О' \
                            and board.field[a.dots()[1].x][a.dots()[1].y] == 'О' \
                            and board.field[a.dots()[2].x][a.dots()[2].y] == 'О':
                        board.field[a.dots()[0].x][a.dots()[0].y] = '■'
                        board.field[a.dots()[1].x][a.dots()[1].y] = '■'
                        board.field[a.dots()[2].x][a.dots()[2].y] = '■'
                        # в случае успеха корабль сохраняется в список
                        board.ships.append(a)
                        # корабль обводится по контуру
                        board.contour(a)
                        # количество живых кораблей увеличивается на 1
                        board.lively_ships = board.lively_ships + 1
                    else:
                        instal_ship(create_ship())
                except IndexError:
                    instal_ship(create_ship())
            # если корабль двухпалубный
            elif a.length == 2:
                try:
                    if board.field[a.dots()[0].x][a.dots()[0].y] == 'О' \
                            and board.field[a.dots()[1].x][a.dots()[1].y] == 'О':
                        board.field[a.dots()[0].x][a.dots()[0].y] = '■'
                        board.field[a.dots()[1].x][a.dots()[1].y] = '■'
                        # в случае успеха корабль сохраняется в список
                        board.ships.append(a)
                        # корабль обводится по контуру
                        board.contour(a)
                        # количество живых кораблей увеличивается на 1
                        board.lively_ships = board.lively_ships + 1
                    else:
                        instal_ship(create_ship())
                except IndexError:
                    instal_ship(create_ship())
            # если корабль однопалубный
            elif a.length == 1:
                try:
                    if board.field[a.dots()[0].x][a.dots()[0].y] == 'О':
                        board.field[a.dots()[0].x][a.dots()[0].y] = '■'
                        # в случае успеха корабль сохраняется в список
                        board.ships.append(a)
                        # корабль обводится по контуру
                        board.contour(a)
                        # количество живых кораблей увеличивается на 1
                        board.lively_ships = board.lively_ships + 1
                    else:
                        instal_ship(create_ship())
                except IndexError:
                    instal_ship(create_ship())
        try:
            instal_ship(create_ship())
        except RecursionError:
            # обнуление доски и перезапуск генерации
            board.field = [['О', 'О', 'О', 'О', 'О', 'О'],
                      ['О', 'О', 'О', 'О', 'О', 'О'],
                      ['О', 'О', 'О', 'О', 'О', 'О'],
                      ['О', 'О', 'О', 'О', 'О', 'О'],
                      ['О', 'О', 'О', 'О', 'О', 'О'],
                      ['О', 'О', 'О', 'О', 'О', 'О']]
            board.ships = []
            board.lively_ships = 0
            self.random_board(board)

    def greet(self):
        print('\nПриветствую тебя, морской пират!\nСейчас начнётся морское крушилово!\n'
              'В бою тебе будет необходимо следовать инструкциям, вводя соответствующие цифры\n'
              'Да начнётся истребление!\n'
              'МОЧИ!!!\n')

    def loop(self):
        step = 1
        while self.ai_board.lively_ships != 0 and self.user_board.lively_ships != 0:
            if step % 2 != 0:
                print('\nВаша доска')
                print(self.user_board)
                print('\nДоска соперника')
                print(self.ai_board)
                print('\nВаш ход')
                self.user.move(self.ai_board)
                step = step + 1
            else:
                print('\nход ПК')
                self.ai.move(self.user_board)
                step = step + 1

    def start(self):
        # генерация доски AI
        self.random_board(self.ai_board)
        # генерация доски игрока
        self.random_board(self.user_board)
        # Скрытие кораблей на доске AI
        self.ai_board.field = [['О', 'О', 'О', 'О', 'О', 'О'],
                           ['О', 'О', 'О', 'О', 'О', 'О'],
                           ['О', 'О', 'О', 'О', 'О', 'О'],
                           ['О', 'О', 'О', 'О', 'О', 'О'],
                           ['О', 'О', 'О', 'О', 'О', 'О'],
                           ['О', 'О', 'О', 'О', 'О', 'О']]
        # обнуление контуров на доске игрока
        for x in range(6):
            for y in range(6):
                if (self.user_board.field[x][y]) == 'T':
                    self.user_board.field[x][y] = 'О'
        # приветствие
        self.greet()
        # игровой цикл
        self.loop()

# Запуск
Game().start()