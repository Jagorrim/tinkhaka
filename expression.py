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
def get_highest_divider(num):
    if num == 0:
        return 1  # Чтобы для нуля не было деления на нуль, нужно возвращать 1.

    num = abs(num)
    for i in range(ceil(num ** 0.5), 0, -1):
        if num % i == 0:
            return num / i
    return num


# Базовый шаблон для всех выражений, которые вообще будут
# Имеет:
# 1. параметры expression и answer, представляющие собой итоговые выражение и ответ
# 2. Методы представления чтобы было удобно дебажить
class MathExpression:
    def __init__(self):
        self.expression: str = ''  # список строк, которые мы будем джойнить
        self.answer: int | float = 0

    def __str__(self) -> str:
        return f'{self.__class__}:exp=<{self.expression}>,ans=<{self.answer}>'

    def __repr__(self) -> str:
        return self.__str__()


class NumericExpression(MathExpression):
    def __init__(self, nums_count, complexity=1, _sum=True, _sub=True, _mult=True, _div=True, _brackets=0):
        if not _sum and not _sub and not _mult and not _div:
            raise ValueError('Отсутствуют операторы!')
        super().__init__()

        self.expression: str = self.generate(nums_count, complexity, _sum, _sub, _mult, _div, _brackets)
        self.answer: int | float = eval(self.expression)

    # Получаем последнее выражение высшего порядка, то есть скобки, умножаемые/делимые на что-либо. Это нужно для того,
    # чтобы правильно расчитать делитель для это части
    @staticmethod
    def get_last_high_exp(expression: list[str]) -> list[str]:
        for index in range(len(expression) - 1, -1, -1):
            if expression[index] in _low_priority_operators:
                return expression[index + 1:-1]
        return expression[:-1]

    # _brackets - уровень вложенности скобок (если 0 - то скобок нет совсем).
    # complexity - размер множителя для всех чисел, который должен усложнять пример
    def generate(self, nums_count, complexity=1, _sum=True, _sub=True, _mult=True, _div=True, _brackets=1) -> str:
        operators: list[str] = []
        if _sum: operators.append('+')
        if _sub: operators.append('-')
        if _mult: operators.append('*')
        if _div: operators.append('/')
        base_complexity = 11

        raw_expression = []
        while nums_count > 0:
            num = random.randrange(1, base_complexity)
            operator = random.choice(operators)

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
                        else:
                            diff = ''
                        brackets = '(' + brackets + diff + ')'
                        raw_expression.append(brackets)
                        nums_count -= (len_brackets + 1)
                    else:
                        raw_expression.append(str(divider))
                        nums_count -= 1

                # Здесь мы рассматриваем случаи, когда можно заменить предыдущее число для удобоваримого деления
                else:
                    # Также можно попытаться заменить делимое на скобку
                    if _brackets and random.randrange(1, 6) == 1 and nums_count > 2:
                        # Суммарное значение скобки, которую мы воткнём
                        divisible = random.randrange(1, base_complexity) * num

                        len_brackets = random.randrange(2, nums_count)
                        brackets = self.generate(len_brackets, complexity=complexity, _sum=_sum, _sub=_sub,
                                                 _mult=_mult, _div=_div, _brackets=_brackets - 1)

                        diff = divisible - eval(brackets)
                        if diff > 0:
                            diff = '+' + str(diff)
                        elif diff < 0:
                            diff = str(diff)
                        else:
                            diff = ''
                        brackets = '(' + brackets + diff + ')'
                        raw_expression[-2] = brackets
                        raw_expression.append(str(num))
                        nums_count -= (len_brackets + 2)

                    # или просто на число
                    else:
                        new_num = random.randrange(1, base_complexity)
                        raw_expression[-2] = str(new_num * num)  # Заменяем старое число на нормально делимое
                        raw_expression.append(str(num))
                        nums_count -= 1

            # Если делить ничего не надо, то можно просто воткнуть скобку/число и оператор (и будет круто)
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
                raw_expression.append(operator)

        return ''.join(raw_expression)


# Тесты
if __name__ == '__main__':
    from time import time

    start = time()
    ans = True
    for _ in range(100_000):
        exp = NumericExpression(nums_count=10, _brackets=2)
        # print(eval(exp.expression) == exp.answer)
        if exp.answer % 1 != 0:
            ans = False
            break
    print(ans)
    print(time() - start)
    for _ in range(1000):
        print(NumericExpression(nums_count=5, _brackets=0).answer % 1 == 0)
