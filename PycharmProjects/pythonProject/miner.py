print('Welcome to Captain Zalupa Miner! Please, read the instructions:', '\n'
      'Ввод высоты поля, ширины поля и количества мин через Enter:', '\n'
      '5', '\n' '7' '\n' '14', '\n' 'Координаты открываемого поля вводить в строку через пробел в формате "строка столбец":', '\n'
       '3 1', '\n' 'Для установки флага ввести координаты в формате "строка столбец+", где "+" - маркер:', '\n' "1 0+", '\n'
      'Для снятия флага ввести координаты в формате "строка столбец-":', '\n' '3 2-', '\n', '\n')

import random as rnd
print('Введите высоту поля: ')
l = int(input())
print('Введите ширину поля: ')
n = int(input())
print('Введите количество мин: ')
m = int(input())
if m > l*n:
    print('ERROR M>l*n')                                            # на случай, если мин больше, чем площадь поля
    raise ValueError

def field_generator(inp_):                                              # генератор поля
    inp_ = tuple(map(int, inp_.split(' ')))
    safe = False
    while not safe:
        f = ['*' for i in range(m)] + ['.' for j in range(l * n - m)]  # список из мин в начале и точек в конце
        rnd.shuffle(f)                                                  # замешиваем
        for a in range(l):                                                  # составляем поле-матрицу
            lst = []
            lst.append(f[:n])
            f.append(*lst)
            f = f[n:]
        if f[inp_[0]][inp_[1]] != '*':                                # проверка безопасного входа
            safe = True
    return f

def mines_coordinates(field_):
    mines_coords_ = []                  # список минных координат
    for g in range(l):
        for r in range(n):
            if field_[g][r] == '*':
                mines_coords_.append((g, r))
    return mines_coords_

def field_digits_generator(field_):
    for k in range(l):                                       # подсчет мин для пустых клеток
        for p in range(n):
            q = 0                                            # счетчик мин
            if field_[k][p] == '.':                           # если точка,то генерим для нее разрешенное окружение
                coord_set = coordinates(k, p)
                for coord in coord_set:
                    if field_[coord[0]][coord[1]] == '*':     # и считаем в этом окружении мины
                        q += 1
                if q != 0:                                   # если мины обнаружены - записываем число
                    field_[k][p] = q
    return field_

def coordinates(x, y):                                       # разрешенные координаты окружения для заданной точки
    steps = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    permit_list = []
    for _ in steps:
        a = x
        b = y
        a += _[0]
        b += _[1]
        if a in range(l) and b in range(n):
            permit_list.append((a, b))
    permit_list = set(permit_list)
    return permit_list

def all_dots_open(x, y):                                                        # функция вскрытия всех близлежащих точек при открытои точки
    global new_dot_coord_set, coord_set2, checked_dots
    new_dot_coord_set = []                                                      # список обнаруженных новых точек для обработки
    checked_dots = []                                                           # список уже проверенных точек
    checked_dots.append((x,y))                                                  # добавим сразу координаты первой открытой точки
    dots_end = False
    coord_set2 = coordinates(x, y)                                        # генерим допустимые координаты окружения
    while not dots_end:
        for mayby_dot_coord in coord_set2:
            if field[mayby_dot_coord[0]][mayby_dot_coord[1]] == '.':            # проверка точка - не точка
                mask[mayby_dot_coord[0]][mayby_dot_coord[1]] = '.'              # если да - открываем ее в маске
                new_dot_coord_set.append(mayby_dot_coord)                       # добавляем ее в новый список на последующую обработку
            if str(field[mayby_dot_coord[0]][mayby_dot_coord[1]]).isdigit():    # проверка число - не число
                mask[mayby_dot_coord[0]][mayby_dot_coord[1]] = field[mayby_dot_coord[0]][mayby_dot_coord[1]] # если число - открываем его  в маске
        for dot in coord_set2:                                                  # перебираем старый набор разрешенных координат
            checked_dots.append(dot)                                            # добавляем все его элементы в список проверенных точек
        coord_set2.clear()                                                      # стираем старый набор
        for new_dot in new_dot_coord_set:                                       # перебираем список новых координат точек
            for crd in coordinates(new_dot[0], new_dot[1]):                     # для каждой обнаруженной точки генерим новую карту допустимых координат окружения
                coord_set2.add(crd)                                             # добавляем все сгенеренные новые координаты окружения в чистый старый список
        coord_set2.difference_update(set(checked_dots))                         # вычитаем из этого списка все уже обработанные координаты
        new_dot_coord_set = []                                                  # очищаем список новых обнаруженных точек
        if coord_set2 == set():                                                 # закрываем цикл, если новых координат окружения нет
            break
    return()

def game_over(field_):
    print('GAME OVER! CAPTAIN ZALUPA HAS LEFT THE VESSEL!♠♠♠')
    for c in field_:
        print(*c)
    return ()

print('\n')

mask = [['o' for i in range(n)] for j in range(l)]        # создаем маску из символов, закрывающих поле
xs_coords = []                                            # список координат флагов
xs = 0                                                    # счетчик флагов
game = True
easy_start = True
while game:
    for _ in range(n):
        print(str(_).rjust(4), end='')                          # выводим горизонтальную шкалу координат
    print('     Mines left: ', m - xs, end='')                    # выводим счетчик оставшихся мин
    print('\n'*2)
    for h in range(len(mask)):
        for _ in mask[h]:                                         # выводим маску
            print(str(_).rjust(4), end='')
        print(str(h).rjust(6), '\n')                              # выводим вертикальную шкалу координат

    print('Введите координаты:')
    inp = input()
    if inp[0].isdigit() == False or int(inp[0]) not in range(0,l) or int(inp[2]) not in range(0,n):
        print('ОШИБКА ВВОДА')
        continue
    if easy_start:                                                # безопасный вход
        field = field_generator(inp)                              # генерим поле
        field = field_digits_generator(field)                     # генерим числа
        mines_coords = mines_coordinates(field)                   # записываем координаты мин
        easy_start = False

    if inp.endswith('+'):                                                                                   # запрос на отметку мины(флага) с маркером
        point = tuple(map(int, inp[:-1].split(' ')))                                                      # считываем координаты без маркера
        if mask[point[0]][point[1]] == 'o':          # запрещаем ставить X на числе или точке
            mask[point[0]][point[1]] = 'X'                      # ставим флаг на маске
            xs_coords.append((point[0], point[1]))              # добавляем эти координаты в список координат флагов
            xs += 1                                             # счетчик флага +1
            if xs == m and sorted(xs_coords) == mines_coords:   # если количество флагов и их координаты совпадают с количеством мин и их координатами, то победа
                print('Mines left:  0', '\n' 'YOU WIN!!! CONGRATULATIONS FROM CAPTAIN ZALUPA!!!♥♥♥')
                break
    elif inp.endswith('-'):                                 # запрос на отмену флага
        point = tuple(map(int, inp[:-1].split(' ')))         # считываем координаты без маркера
        mask[point[0]][point[1]] = 'o'                      # убираем флаг с маски
        xs_coords.remove((point[0], point[1]))              # убираем координаты флага
        xs -= 1                                             # счетчик флага -1
    else:
        point = tuple(map(int, inp.split(' ')))             # если маркера нет - просто считываем координаты
        if str(mask[point[0]][point[1]]).isdigit():         # запрос на открытие всех клеток вокруг числа
            coord_set3 = coordinates(point[0], point[1])    # создаем доступное окружение
            Xs_ = 0                                              # счетчик Х-ов
            Xs_coords_ = []                                     # список координат Х-ов
            for coord in coord_set3:                            # считаем количество X-ов в окружении числа
                if mask[coord[0]][coord[1]] == 'X':
                    Xs_coords_.append((coord[0], coord[1]))     # записываем их координаты
                    Xs_ += 1
            if Xs_ == mask[point[0]][point[1]]:                # если количество Х-ов в окружении совпадает с открытым числом
                coord_set3.difference_update(set(Xs_coords_))  # то вскрываем все точки, кроме иксов
                for coord in coord_set3:
                    mask[coord[0]][coord[1]] = field[coord[0]][coord[1]]
                    if mask[coord[0]][coord[1]] == '.':         # если точка, то запускаем функцию по вскрытию всех точек в окружении
                        all_dots_open(coord[0], coord[1])
                    elif not set(Xs_coords_).issubset(mines_coords):         # но если Х не попадает на мину, то всё.
                        game_over(field)
                        game = False
                        break
        mask[point[0]][point[1]] = field[point[0]][point[1]]    # открываем значение координат
        if mask[point[0]][point[1]] == '*':                 # если мина - конец игры, выводим поле
            game_over(field)
            break
        if mask[point[0]][point[1]] == '.':                 # если точка, то запускаем функцию по вскрытию всех точек в окружении
            all_dots_open(point[0], point[1])























