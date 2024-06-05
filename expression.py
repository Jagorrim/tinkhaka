import random

_reverse_operators = {
    '+': '-',
    '-': '+',
    '*': '/',
    '/': '*'
}


# Базовый шаблон для всех выражений, которые вообще будут
# Имеет:
# 1. параметры expression и answer, представляющие собой итоговые выражение и ответ
# 2. Методы представления чтобы было удобно дебажить
class MathExpression:
    def __init__(self):
        self.expression: str = ''  # список строк, которые мы будем джойнить
        self.answer: str = ''

    def __str__(self) -> str:
        return f'{self.__class__}:exp=<{self.expression}>,ans=<{self.answer}>'

    def __repr__(self) -> str:
        return self.__str__()


class NumericExpression(MathExpression):
    def __init__(self, nums_count, complexity=1, _sum=True, _sub=True, _mult=True, _div=True, _brackets=True):
        if not _sum and not _sub and not _mult and not _div:
            raise ValueError('Отсутствуют операторы!')
        super().__init__()

        self.expression = '1 + 2 + 3'
        self.answer = '6'

        # self.expression = self.generate(nums_count, complexity, _sum, _sub, _mult, _div, _brackets)
        # self.answer = eval(self.expression)

    # _brackets - уровень вложенности скобок (если 0 - то скобок нет совсем).
    # complexity - размер множителя для всех чисел, который должен усложнять пример
    def generate(self, nums_count, complexity=1, _sum=True, _sub=True, _mult=True, _div=True, _brackets=1):
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

            # Если из чисел от 1 до 5 выпало 1, то можно воткнуть скобки (шанс - 20%), и при этом скобки можно поставить
            # и если для них есть место (нельзя, чтобы было 1 число в скобках)
            if _brackets and random.randrange(1, 6) == 1 and nums_count > 1:
                len_brackets = random.randrange(2, nums_count + 1)
                brackets = '(' + self.generate(len_brackets, complexity=complexity, _sum=_sum, _sub=_sub, _mult=_mult,
                                               _div=_div, _brackets=_brackets - 1) + ')'
                nums_count -= len_brackets

                raw_expression.append(brackets)
                if nums_count > 1:
                    raw_expression.append(operator)

            else:
                if len(raw_expression) > 1 and raw_expression[-1] == '/':
                    new_num = random.randrange(1, base_complexity)
                    raw_expression[-2] = new_num * num  # Заменяем старое число на норм делимое

                raw_expression.append(num)

                if nums_count > 1:
                    raw_expression.append(operator)
                nums_count -= 1

        return ''.join(raw_expression)

    #
    # # raw_expression = [8, '*', 2, '-', 4, '*', 3]
    # self.expression = []
    #
    # for i in range(len(raw_expression)):
    #     # Если мы добавляем первый элемент, перед которым ничего быть не может
    #     if len(self.expression) == 0:
    #         self.expression.append(raw_expression[i])
    #         continue
    #
    #     # Добавляем операторы только вкупе с самими числами
    #     if raw_expression[i] in operators:
    #         continue
    #
    #     if raw_expression[i - 1] in ('-', '+'):
    #         self.expression.append(raw_expression[i - 1] + raw_expression[i])
    #     else:
    #         for j in range(len(self.expression)):
    #             self.expression[j] += raw_expression[i - 1] + raw_expression[i]
    #
    # self.answer = asnwer


# Тесты
if __name__ == '__main__':
    a = NumericExpression(nums_count=6)
    print(a)
