from flask import Flask, render_template, flash

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/login/')
def login():
    return render_template('account/login.html')


@app.route('/sign-up/')
def sign_up():
    return render_template('account/sign-up.html')


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
