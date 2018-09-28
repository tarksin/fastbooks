from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, FloatField, DateField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('&#945', validators=[DataRequired('Please enter your username')])
    password = StringField('&#946', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class AddExpenseForm(FlaskForm):
    expdate = DateField('Date', validators=[DataRequired()])
    expdesc = StringField('Item', validators=[DataRequired()])
    expamount = FloatField('Amount', validators=[DataRequired()])
    expcat = SelectField('Category',  coerce=int, validators=[DataRequired()])
    vendor = StringField('Vendor', validators=[DataRequired()])
    submit = SubmitField('Save')

class AddExpcatForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    expcat = StringField('expcat', validators=[DataRequired()])
    submit = SubmitField('Save')

class AddTodoForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    todo = StringField('Item', validators=[DataRequired()])
    project_id = IntegerField('project_id', validators=[DataRequired()])
    submit = SubmitField('Save')


class AddBankItemForm(FlaskForm):
    bi_date =     DateField('Date', validators=[DataRequired()])
    bank_id =  IntegerField('Bank', validators=[DataRequired()])
    bi_amount =  FloatField('Amount', validators=[DataRequired()])
    vendor = StringField('Vendor', validators=[DataRequired()])
    submit = SubmitField('Save')



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    password2 = StringField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user_exists = User.check_user_exists(username.data)
        if user_exists:
            raise ValidationError('That username is already in use.')

    def validate_email(self, email):
        user_exists = User.check_email_exists(email.data)
        if email_exists:
            raise ValidationError('That email address is already in use.')
