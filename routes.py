from flask import Flask, render_template, request, redirect, url_for, session
from expression import ArithmeticExpression

app = Flask(__name__)


@app.route('/')
@app.route('/game_process', methods=['GET', 'POST'])
def game_process():
    tasks_exp = []
    tasks_ans = []
    for _ in range(3):
        expression, answer = ArithmeticExpression(5).expression, ArithmeticExpression(5).answer
        tasks_exp.append(expression)
        tasks_ans.append(answer)

    return render_template('game_process.html', tasks_exp=tasks_exp, tasks_ans=tasks_ans)


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
