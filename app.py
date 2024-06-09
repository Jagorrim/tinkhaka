import flask_login
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
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
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"),
                     rating=0,
                     solved=0)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("home.html")


@flask_login.login_required
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
    app.run()
