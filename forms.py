from wtforms import (
    Form,
    validators,
    TextField,
    PasswordField,
    BooleanField,
)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Adress', [validators.Length(min=4, max=20)])
    password = PasswordField('Password', [validators.Required(),
                                          validators.EqualTo('confirm', message='Password must mutch')])
    confirm = PasswordField('Repeat Password')

    accept_tos = BooleanField('I accept the Terms of Service and the Privacy Notice '
                              '(Last upadate Jul 17 2018', [validators.Required()])


