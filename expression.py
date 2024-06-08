import random
from math import ceil

_reverse_operators = {
    '+': '-',
    '-': '+',
    '*': '/',
    '/': '*'
}

_low_priority_operators = ('+', '-')
_high_priority_operators = ('*', '/')


# Нужно для получения наибольшего делителя. В случае простоты числа просто вернём само число, лол
def get_highest_divider(num: float | int) -> float | int:
    if num == 0:
        return 1  # Чтобы для нуля не было деления на нуль, нужно возвращать 1.

    num = abs(num)
    for i in range(2, ceil(num ** 0.5) + 1):
        if num % i == 0:
            return num / i

    return num


def get_new_num(complexity: int | float, min_num: int, max_num: int) -> float | int:
    return random.randrange(min_num, max_num) * complexity


# Базовый шаблон для всех выражений, которые вообще будут
# Имеет:
# 1. параметры expression и answer, представляющие собой итоговые выражение и ответ
# 2. Методы представления чтобы было удобно дебажить
class MathExpression:
    def __init__(self):
        self.expression: str = ''  # само выражение
        self.answer: float | int = 0

    def __str__(self) -> str:
        return f'{self.__class__}:exp=<{self.expression}>,ans=<{self.answer}>'

    def __repr__(self) -> str:
        return self.__str__()


# Класс для обычных арифметических примеров
class ArithmeticExpression(MathExpression):
    def __init__(self, nums_count: int, complexity: int = 1,
                 _sum: bool = False, _sub: bool = False, _mult: bool = False, _div: bool = False,
                 _brackets: int = 0):

        if not _sum and not _sub and not _mult and not _div:
            raise ValueError('Отсутствуют операторы!')

        if complexity > 3:  # Иначе пойдут слишком большие числа и float такое не потянет
            raise ValueError('Неподдерживаемая сложность!')

        super().__init__()
        if complexity != 1:
            complexity = random.randrange(10 ** (complexity - 1), 10 ** complexity + 1)

        while True:
            try:
                self.expression: str = self.generate(nums_count, complexity, _sum, _sub, _mult, _div, _brackets)
                self.answer: float | int = eval(self.expression)
                break
            # Тут мы игнорируем моменты, когда при сложности 3 и только умножении и делении тип float может сойти с ума
            except Exception:
                pass

    # Получаем последнее выражение высшего порядка, то есть скобки, умножаемые/делимые на что-либо. Это нужно для того,
    # чтобы правильно расчитать делитель для это части
    @staticmethod
    def get_last_high_exp(expression: list[str]) -> list[str]:
        for index in range(len(expression) - 1, -1, -1):
            if expression[index] in _low_priority_operators:
                return expression[index + 1:-1]
        return expression[:-1]

    # Формируем словарь количества операторов, исходя из возможности их добавления и количества чисел
    @staticmethod
    def get_available_operators(nums_count: int, _sum: bool, _sub: bool, _mult: bool, _div: bool) -> dict[str, int]:
        operators_places = nums_count - 1
        operators: dict[str, int] = {}

        if _sum: operators['+'] = 0
        if _sub: operators['-'] = 0
        if _mult: operators['*'] = 0
        if _div: operators['/'] = 0

        operator_usages = ceil(operators_places / len(operators))
        for i in operators: operators[i] = operator_usages
        return operators

    # _brackets - уровень вложенности скобок (если 0 - то скобок нет совсем).
    # complexity - размер множителя для всех чисел, который должен усложнять пример
    def generate(self, nums_count: int, complexity: int,
                 _sum: bool, _sub: bool, _mult: bool, _div: bool,
                 _brackets: int) -> str:

        operators = self.get_available_operators(nums_count, _sum, _sub, _mult, _div)

        min_num = 1
        max_num = 11

        raw_expression = []
        while nums_count > 0:
            num = get_new_num(complexity, min_num, max_num)

            # Если текущее число является делителем,
            # то нужно всё это обработать чтобы было круто и не было тяжело делимого говна
            if len(raw_expression) > 1 and raw_expression[-1] == '/':

                # Если предыдущее число - тоже делитель (как и то, число/скобка, которые мы сейчас добавим) ИЛИ
                # если предыдущее число - скобка, то мы не будем менять предыдущее число на что-либо,
                # ибо скобку менять смысла нет (зачем мы её генерили тогда),
                # а если менять делитель, то всё может сломаться
                if len(raw_expression) > 3 and raw_expression[-3] in _high_priority_operators \
                        or raw_expression[-2][0] == '(':
                    # последняя часть выражения с высшим приоритетом (скобки/умножение/деление)
                    calculated = eval(''.join(self.get_last_high_exp(raw_expression)))
                    divider = get_highest_divider(calculated)

                    # Можем делить скобки на скобки с шансом в 20%
                    # и если можем из воткнуть на этом уровне вложенности и если для них есть место
                    if _brackets and random.randrange(1, 6) == 1 and nums_count > 2:
                        len_brackets = random.randrange(2, nums_count)
                        brackets = self.generate(len_brackets, complexity=complexity, _sum=_sum, _sub=_sub,
                                                 _mult=_mult, _div=_div, _brackets=_brackets - 1)

                        # Разница между скобкой и делителем, которую надо компенсировать
                        diff = divider - eval(brackets)
                        if diff > 0:
                            diff = '+' + str(diff)
                        elif diff < 0:
                            diff = str(diff)
                        else:  # Тут мы рассматриваем случай, когда разница нулевая => ничего и добавлять не надо
                            diff = ''
                        brackets = '(' + brackets + diff + ')'
                        raw_expression.append(brackets)
                        nums_count -= (len_brackets + 1)
                    else:
                        raw_expression.append(str(divider))
                        nums_count -= 1

                # Здесь мы рассматриваем случаи, когда можно заменить предыдущее число для удобоваримого деления
                # (и для меньших затрат по производительности)
                else:
                    # Также можно попытаться заменить делимое на скобку
                    if _brackets and random.randrange(1, 6) == 1 and nums_count > 2:
                        # Суммарное значение скобки, которую мы воткнём
                        divisible = get_new_num(complexity, min_num, max_num) * num

                        len_brackets = random.randrange(2, nums_count)
                        brackets = self.generate(len_brackets, complexity=complexity, _sum=_sum, _sub=_sub,
                                                 _mult=_mult, _div=_div, _brackets=_brackets - 1)

                        # Разница между скобкой и делимым, которую надо компенсировать
                        diff = divisible - eval(brackets)
                        if diff > 0:
                            diff = '+' + str(diff)
                        elif diff < 0:
                            diff = str(diff)
                        else:  # Тут мы рассматриваем случай, когда разница нулевая => ничего и добавлять не надо
                            diff = ''
                        brackets = '(' + brackets + diff + ')'
                        raw_expression[-2] = brackets
                        raw_expression.append(str(num))
                        nums_count -= (len_brackets + 2)

                    # или просто на число
                    else:
                        new_num = get_new_num(complexity, min_num, max_num)
                        raw_expression[-2] = str(new_num * num)  # Заменяем старое число на нормально делимое
                        raw_expression.append(str(num))
                        nums_count -= 1

            # Если делить ничего не надо, то можно просто воткнуть скобку/число (и будет круто)
            else:
                # Если из чисел от 1 до 5 выпало 1, то можно воткнуть скобки (шанс - 20%),
                # и при этом скобки можно поставить
                # и если для них есть место (нельзя, чтобы было 1 число в скобках)
                if _brackets and random.randrange(1, 6) == 1 and nums_count > 1:
                    len_brackets = random.randrange(2, nums_count + 1)
                    brackets = '(' + self.generate(len_brackets, complexity=complexity, _sum=_sum, _sub=_sub,
                                                   _mult=_mult, _div=_div, _brackets=_brackets - 1) + ')'

                    raw_expression.append(brackets)
                    nums_count -= len_brackets
                else:
                    raw_expression.append(str(num))
                    nums_count -= 1

            # После всех манипуляций можно поставить оператор для следующего числа (если следующее число вообще будет)
            if nums_count > 0:
                operator = random.choice(list(operators.keys()))
                operators[operator] -= 1
                if operators[operator] == 0:
                    del operators[operator]
                raw_expression.append(operator)

        return ''.join(raw_expression)


# Тесты (запустятся только в случае запуска именно этого конкретного файла)
if __name__ == '__main__':
    from time import time

    start = time()
    for _ in range(100_000):
        exp = ArithmeticExpression(nums_count=10, _brackets=2, _mult=True, _div=True, _sub=True, _sum=True,
                                   complexity=3)
        # print(exp)

    print('time -', time() - start)
