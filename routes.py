from flask import Flask, render_template, request, redirect, url_for, session
from expression import ArithmeticExpression

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/game_process', methods=['GET', 'POST'])
def game_process():
    if request.method == 'GET':
        return render_template('game_process.html')

    tasks_exp = []
    tasks_ans = []
    for _ in range(3):
        exp = ArithmeticExpression(5, _sub=True)
        tasks_exp.append(exp.expression)
        tasks_ans.append(exp.answer)

    return [tasks_exp, tasks_ans]


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
