from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource
from data import trans_resources
from translator import translatee
from data import db_session, trans_api
from data.user import User
from data.trans import Trans
from forms.users import RegisterForm, LoginForm
from forms.translation import TransForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)

api.add_resource(trans_resources.TransListResource, '/api/v2/trans')

api.add_resource(trans_resources.TransResource, '/api/v2/trans/<int:trans_id>')
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/trans_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def trans_delete(id):
    db_sess = db_session.create_session()
    trans = db_sess.query(Trans).filter(Trans.id == id, Trans.user == current_user).first()
    if trans:
        db_sess.delete(trans)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/history')


@app.route('/main', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def main():
    form = TransForm()
    if form.lang.data == 'Morsecode':
        form.trans_lang.choices = [('English', 'English'), ('Russian', 'Russian')]
    else:
        form.trans_lang.choices = [('Morsecode', 'Morsecode')]
    if form.validate_on_submit():
        trans_text = translatee(form.lang.data, form.trans_lang.data, form.content.data)
        if current_user.is_authenticated and trans_text is not None:
            db_sess = db_session.create_session()
            trans = Trans(
                content=form.content.data,
                lang=form.lang.data,
                translation=trans_text,
                trans_lang=form.trans_lang.data,
                user_id=current_user.id
            )
            db_sess.add(trans)
            db_sess.commit()
        if trans_text is not None:
            return render_template('main.html', text=trans_text, form=form)
        else:
            return render_template('main.html', text='Неправильный формат ввода', form=form)

    return render_template('main.html', form=form)


@app.route('/history')
def history():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        trans = db_sess.query(Trans).filter(Trans.user == current_user)
        return render_template("history.html", trans=trans)
    else:
        return render_template("history.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/facilities')
def facilities():
    return render_template("facilities.html")


@app.route('/reg', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('reg.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('reg.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('reg.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST', 'PUT'])
def login():
    form = LoginForm()
    if form.validate_on_submit ():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('log.html', message="Неправильный логин или пароль", form=form)
    return render_template('log.html', title='Авторизация', form=form)


if __name__ == '__main__':
    db_session.global_init("db/trans.db")
    app.register_blueprint(trans_api.blueprint)
    app.run(port=8080, host='127.0.0.1')