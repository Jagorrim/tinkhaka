import flask_login
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from expression import ArithmeticExpression, Equation

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    solved = db.Column(db.Integer, nullable=False)


db.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not password:
            flash("Требуется пароль!", "danger")
            return redirect(url_for("register"))

        if Users.query.filter_by(username=username).first():
            flash("Данное имя занято!", "danger")
            return redirect(url_for("register"))

        user = Users(username=username, password=password, rating=0, solved=0)
        db.session.add(user)
        db.session.commit()
        flash("👍", "success")
        return redirect(url_for("login"))

    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            user = Users.query.filter_by(
                username=request.form.get("username")).first()
            if user.password == request.form.get("password"):
                login_user(user)
                return redirect(url_for("home"))
        except AttributeError:
            pass
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/game_process', methods=['GET', 'POST'])
@flask_login.login_required
def game_process():
    if request.method == 'GET':
        return render_template('game_process.html')

    # Если POST, то надо занести в БД данные о юзере и его рейтинге и кол-ве решённых задач
    data = request.get_json(force=True)

    user = Users.query.filter_by(id=current_user.id).first()
    user.rating += data['rating']
    db.session.commit()
    user.solved += data['solved']
    db.session.commit()
    print(Users.query.filter_by(id=current_user.id).first().rating)
    return 'allright'


@app.route('/game_create', methods=['GET'])
@flask_login.login_required
def game_create():
    return render_template('game_create.html')


@app.route('/get_exps', methods=['GET', 'POST'])
@flask_login.login_required
def get_exps():
    try:
        data = request.json.copy()
        if data['type'] == 'arithmetic':
            _exp = ArithmeticExpression
            if None in [data['_brackets'], data['nums_count'], data['complexity']]:
                raise ValueError('Не все поля заполнены!')
        else:
            _exp = Equation
            if data['complexity'] is None:
                raise ValueError('Не задана сложность!')
        del data['type']
        tasks_exp = []
        tasks_ans = []
        for _ in range(3):
            exp = _exp(**data)
            tasks_exp.append(exp.expression)
            tasks_ans.append(exp.answer)
        return [tasks_exp, tasks_ans]
    except Exception as error:
        return f'Ошибка: {error}'


if __name__ == "__main__":
    app.run()
