from flask import (
    Flask, render_template, redirect,
    flash, request, url_for, session,
)

from dbconnect import connection
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
from functools import wraps
import gc

from forms import RegistrationForm


app = Flask(__name__)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You have to login first')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash('You have been logged out!')
    gc.collect()
    return redirect(url_for('halloffame'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = ''
    try:
        c, conn = connection()
        if request.method == 'POST':
            data = c.execute('SELECT * FROM users WHERE username = (%s)',
                             (thwart(request.form['username']), ))
            data = c.fetchone()[2]

            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash("You are logged in as {}".format(session['username']))
                return redirect(url_for('halloffame'))
            else:
                error = 'Invalid credentials, try again'
        gc.collect()

        return render_template('account/login.html', error=error)
    except Exception as e:
        error = 'Invalid credentials, try again'
        return render_template('account/login.html', error=error)


@app.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
    try:
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt(str(form.password.data))
            c, conn = connection()

            sql = 'SELECT * FROM users WHERE username = (%s)'
            x = c.execute(sql, (thwart(username), ))

            if int(x) > 0:
                flash("This user is already registrated")
                return render_template('account/sign-up.html', form=form)
            c.execute("INSERT INTO users (username, email, password, tracking) "
                      "VALUES (%s, %s, %s, %s)",
                      (thwart(username), thwart(email), thwart(password),
                       thwart('/')))

            conn.commit()
            flash("Thanks for registration")
            c.close()
            conn.close()
            gc.collect()

            session['logged_in'] = True
            session['username'] = username

            return redirect(url_for('halloffame'))

        return render_template('account/sign-up.html', form=form)
    except Exception as e:
        return str(e)


@app.route('/jaselnik/halloffame/')
def halloffame():
    flash('In a few days you will be able to create your own Hall Of Fame. Check it out!')
    flash('Stupid GERLLs!')
    flash('Sergio Tamkovich')
    return render_template('halloffame/jaselnik.html')


@app.errorhandler(404)
def page_not_fond(e):
    return render_template('error/404.html')


if __name__ == '__main__':
    app.config['SECRET_KEY'] = '123456'
    app.run()
