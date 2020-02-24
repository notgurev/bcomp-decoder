# готово к 3 лабе по ОПД


def hex_to_binary(hex):
    # Костыль. Я устал.
    d = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111',
    }
    hex_list = list(hex)
    for i in range(0, len(hex_list)):
        hex_list[i] = d.get(hex_list[i])
    binary = ''.join(hex_list)
    return binary


def binary_to_signed_16(x):
    # говнокод
    if x[0] == '0':
        return hex(int(x, 2)).lstrip('0x').capitalize()
    else:
        x = list(x)
        for i in range(0, len(x)):
            if x[i] == '1':
                x[i] = '0'
            else:
                x[i] = '1'
        x = ''.join(x)
        x = hex(int(x, 2)+1).lstrip('0x').capitalize()
        return '-'+x


def adr_com(x):
    a_kop = {
        '2': ('AND %s', 'Логическое умножение'),
        '3': ('OR %s', 'Логическое или'),
        '4': ('ADD %s', 'Сложение'),
        '5': ('ADC %s', 'Сложение с переносом'),
        '6': ('SUB %s', 'Вычитание'),
        '7': ('CMP %s', 'Сравнение'),
        '8': ('LOOP %s', 'Декремент и пропуск'),
        '9': ('', 'Резерв'),
        'A': ('LD %s', 'Загрузка'),
        'B': ('SWAM %s', 'Обмен'),
        'C': ('JUMP %s', 'Переход'),
        'D': ('CALL %s', 'Вызов подпрограммы'),
        'E': ('ST %s', 'Сохранение'),
    }
    x_bin = hex_to_binary(x)
    # Анализ адресации
    m = 'error'
    info = ''
    if x_bin[4] == '0':
        # Прямая абсолютная адресация
        # В мнемонику записываем адрес
        info = '(Прямая абсолютная адресация)'
        m = '0x' + x[1:4].lstrip('0')
    if x_bin[4] == '1':
        if x[1] == 'F':
            # Прямая загрузка операнда (записываем в info)
            info = '(Прямая загрузка операнда)'
            # В мнемонику записываем операнд
            m = '#0x' + x[2:4]
        else:
            mode = x_bin[5:8]
            offset = binary_to_signed_16(x_bin[8:16])
            if mode == '110':
                # Прямая относительная адресация (записываем в info)
                info = '(Прямая относительная адресация)'
                # В мнемонику записываем смещение
                if offset[0] != '-': #этот ужас надо как-то убрать
                    m = 'IP+%s' % offset
                else:
                    m = 'IP%s' % offset
            elif mode == '000':
                # Косвенная относительная адресация (записываем в info)
                info = '(Косвенная относительная адресация)'
                if offset[0] != '-':
                    m = '(IP+%s)' % offset
                else:
                    m = '(IP%s)' % offset
            elif mode == '010':
                # Косвенная относительная автоинкрементная адресация (записываем в info)
                info = '(Косвенная относительная автоинкрементная адресация)'
                if offset[0] != '-':
                    m = '(IP+%s)+' % offset
                else:
                    m = '(IP%s)+' % offset
            elif mode == '011':
                # Косвенная относительная автодекрементная адресация (записываем в info)
                info = '(Косвенная относительная автодекрементная адресация)'
                if offset[0] != '-':
                    m = '(IP+%s)-' % offset
                else:
                    m = '(IP%s)-' % offset

    temp = a_kop.get(x[0])
    return (temp[0] % m, temp[1], info)


def bez_adr_com(x):
    b = {
        '0000': ('NOP ', 'Нет операции'),
        '0100': ('HLT ', 'Остановка'),
        '0200': ('CLA ', 'Очистка аккумулятора'),
        '0280': ('NOT ', 'Инверсия аккумулятора'),
        '0300': ('CLC ', 'Очистка рег. переноса'),
        '0380': ('CMC ', 'Инверсия рег. переноса'),
        '0400': ('ROL ', 'Циклический сдвиг влево'),
        '0480': ('ROR ', 'Циклический сдвиг вправо'),
        '0500': ('ASL ', 'Арифметический сдвиг влево'),
        '0580': ('ASR ', 'Арифметический сдвиг вправо'),
        '0600': ('SXTB ', 'Расширение знака байта'),
        '0680': ('SWAB ', 'Обмен ст. и мл. байтов'),
        '0700': ('INC ', 'Инкремент'),
        '0740': ('DEC ', 'Декремент'),
        '0780': ('NEG ', 'Изменение знака')
    }
    return b.get(x)


def vet_com(x):
    v = {
        'F0': ('BEQ %s','Переход, если равенство'),
        'F1': ('BNE %s ', 'Переход, если неравенство'),
        'F2': ('BMI %s ', 'Переход, если минус'),
        'F3': ('BPL %s ', 'Переход, если плюс'),
        'F4': ('BLO/BCS %s ', 'Переход, если ниже/перенос'),
        'F5': ('BHIS/BCC %s ', 'Переход, если выше/нет переноса'),
        'F6': ('BVS %s ', 'Переход, если переполнение'),
        'F7': ('BVC %s ', 'Переход, если нет переполнения'),
        'F8': ('BLT %s ', 'Переход, если меньше'),
        'F9': ('BGE %s ', 'Переход, если больше или равно'),
        'CE': ('BR %s ', 'Безусловный переход (эквивалент JUMP D)'),
    }
    x_bin = hex_to_binary(x)
    offset = binary_to_signed_16(x_bin[8:16])
    if offset[0] != '-':
        m = 'IP+%s' % offset
    else:
        m = 'IP%s' % offset

    temp = v.get(x[0:2]) 
    return (temp[0] % m, temp[1])



with open('input.txt', 'r', encoding='utf-8') as input:
    for c in input:
        c = c.replace('\n', '')
        output_line = c + '| '
        if c[0] == "0":
            output_line += "{0[0]:<15} | {0[1]:<20}".format(bez_adr_com(c))
        elif c[0] == "F" or c[0:2] == "CE":
            output_line += "{0[0]:<15} | {0[1]:<20}".format(vet_com(c))
        elif c[0] == "1":
            print("Команды ввода-вывода не поддерживаются!")
        else:
            output_line += "{0[0]:<15} | {0[1]:<20} | {0[2]: <20}".format(adr_com(c))
        print(output_line, end='\n')
