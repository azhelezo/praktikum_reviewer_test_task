"""Привет!
В общем хорошо, но есть что исправить.

Кроме комментариев в коде, обрати внимание на консистентность стиля:
1 - Возврат (return) строк почти каждый раз выглядит по-разному -
подстановка значений и через f'', и через .format(); 
перенос длинных строк с бэкслешами и без, в общем есть над чем поработать:
    - Не использовать бекслеш для переноса.
    Другие варианты тут: https://www.pythonpool.com/python-multiline-string/
    - Если строка будет состоять из нескольких частей, f-строками
    должны быть только те части, в которых подставляются переменные.
2 - В коде используется два варианта сложения - 'x += y' и 'x = x + y':
    >>> week_stats += record.amount
    >>> today_stats = today_stats + Record.amount
    Надо выбрать один и придерживаться его.
Код в едином стиле проще читать.

В конце стоит добавить несколько вариантов использования кода.
Если код не покрыт тестами, это покажет тебе, где что-то работает не так.
"""

import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        """Надо исправить.
        Тернарный оператор это красиво, но его использование может
        усложнить понимание кода.
        Он хорошо подходит для коротких и простых однострочных варажений,
        а здесь лучше использовать просто if/else.
        """
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        """Можно лучше.
        Субъективное мнение, необязательно:
        Если в init часть значений присваивается сразу из полученных данных,
        а часть - в результате выполнения какой-то логики,
        лучше сначала присвоить "готовые", а логику оставить в конце."""
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Можно лучше.
        Этот метод должен принимать объект класса Record.
        Сейчас в него можно передать что угодно (число, строку, None,
        другой Calculator), и это сломает дальнейшую логику.
        Стоит добавить соответствующую проверку.
        """
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        """Надо исправить.
        Здесь, в цикле for, Record - это название переменной для цикла,
        но у нас в коде присутствует одноименный класс Record.
        Интерпретатор такой код выполнит, а человек может запутаться.
        Код должен быть понятен тому, кто будет его читать после тебя,
        поэтому лучше назвать переменную иначе.
        В self.records действительно хранятся объекты класса Record,
        но это не значит что к ним нужно обращаться именно так -
        циклу for неважно, как ты назовешь переменную.
        Попробуй перечитать главу про циклы.
        """
        for Record in self.records:
            """Надо исправить.
            Здесь у нас на каждой итерации для проверки условия происходит
            вызов dt.datetime.now().date() - так делать не надо)
            Во-первых, это лишняя работа. Если наш массив состоит из
            20000 элементов - код 20000 раз вычислит сегодняшнюю дату.
            А если это будет не вычисление даты, а например запрос данных
            от стороннего сервиса - пиши пропало.
            Во-вторых, если вдруг за время прохождения цикла сменится дата,
            функция вернет некорректный результат.
            Когда пользователь запрашивает данные за какой-то период,
            он должен получать данные за этот период без поправки
            на смену даты.
            Нужно вычислить "сегодня" один раз до запуска цикла, сохранить
            в переменную и сравнивать с ней.
            """
            if Record.date == dt.datetime.now().date():
                """Можно лучше.
                Стоит придерживаться единого стиля операций:
                'x += y' или 'x = x + y'
                """
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        """Отлично.
        Тут как раз правильно - один раз сохранили "сегодня" в переменную
        и работаем с ней в цикле.
        """
        today = dt.datetime.now().date()
        for record in self.records:
            """Надо исправить.
            Здесь мы на каждом шаге выполняем по две одинаковые операции.
            Как минимум, стоит выполнять эту операцию один раз за итерацию,
            сохранять ее результат в переменную и в условии сравнивать с ней.
            Но можно обойтись и без переменной.
            В python мы можем выстраивать цепочку сравнений: например,
            >>> (x > 0 and x <= 10)
            эквивалентно выражению
            >>> 0 < x <= 10
            Разница в том, что в первом случае 'x' вычисляется два раза,
            а во втором - один.
            """
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                """Можно лучше.
                Стоит придерживаться единого стиля операций:
                'x += y' или 'x = x + y'
                """
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    """Надо исправить.
    Если хочешь комментировать функции, надо оформить как докстринги:
    https://www.python.org/dev/peps/pep-0257/
    """
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            """Надо исправить.
            Приведи return строк к единому стилю.
            """
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
            """Можно лучше.
            Здесь можно обойтись без else, т.к. под if есть return.
            Если условие выполнено, метод возвращает одно значение,
            если нет - другое.
            """
        else:
            """Надо исправить.
            Приведи return строк к единому стилю.
            """
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    """Надо исправить.
    В задании так:
        Метод get_today_cash_remained(currency) денежного калькулятора
        должен принимать на вход код валюты:
        одну из строк "rub", "usd" или "eur".
    У нас получается, что метод будет принимать курсы и работать с ними,
    это в задачу не входит.
    """
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        """Надо исправить.
        Создание переменной currency_type тут излишне, т.к. ниже она
        будет объявлена в любом случае в зависимости от значения currency.
        """
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        """Надо исправить.
        Если нам понадобится расширить список валют, придется дописывать
        по else на каждую валюту.
        Расписывать if на 10-20-50 условий - не наш метод)
        Почитай https://blog.teclado.com/simplify-long-if-statements-python/,
        прикинь как можно тут применить.
        """
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            """Надо исправить.
            Эта строка сравнивает cash_remained и 1.00,
            если они равны - возвращает True.
            Результат этого сравнения не сохраняется и не используется,
            назначение строки непноятно, по мне - строку можно удалить.
            """
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            """Надо исправить.
            Мы не используем вычисления в f-строках,
            результат round() надо вынести в переменную и подставить её.
            + приведи return строк к единому стилю.
            """
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            """Надо исправить.
            Приведи return строк к единому стилю.
            """
            return 'Денег нет, держись'
        elif cash_remained < 0:
            """Надо исправить.
            Приведи return строк к единому стилю.
            """
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    """Надо исправить.
    Метод get_week_stats уже наследуется от родительского класса Calculator,
    объявлять или переопределять его тут не нужно.
    К тому же, описанный таким образом метод ничего не возвращает - 
    результат вызова super().get_week_stats() никак не используется.
    """
    def get_week_stats(self):
        super().get_week_stats()
