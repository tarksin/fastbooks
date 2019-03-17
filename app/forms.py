from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, FloatField, DateField, SelectField, SubmitField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired('Please enter your username')])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class AddExpenseForm(FlaskForm):
    expdate = DateField('Date', validators=[DataRequired()])
    expdesc = StringField('Item', validators=[DataRequired()])
    expamount = FloatField('Amount', validators=[DataRequired()])
    expcat = SelectField('Category',  coerce=int, validators=[DataRequired()])
    vendor = StringField('Vendor', validators=[DataRequired()])
    submit = SubmitField('Save')

class ReportForm(FlaskForm):
    startdate = DateField('From', validators=[DataRequired()])
    enddate =   DateField('To', validators=[DataRequired()])
    single_cat_id = IntegerField('Single cat id')
    by_cat =    BooleanField('Group by cat')
    submit =    SubmitField('Go')

class AddExpcatForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    expcat = StringField('expcat', validators=[DataRequired()])
    submit = SubmitField('Save')

class AddTodoForm(FlaskForm):
    formname =HiddenField('formname')
    id = IntegerField('id', validators=[DataRequired()])
    todo = StringField('Item', validators=[DataRequired()])
    project_id = IntegerField('project_id', validators=[DataRequired()])
    submit = SubmitField('Save')

class AddProjectForm(FlaskForm):
    # id = IntegerField('id', validators=[DataRequired()])
    # expcat = StringField('expcat', validators=[DataRequired()])
    # submit = SubmitField('Save')
#    id = IntegerField('id', validators=[DataRequired()])
    formname =HiddenField('formname')
    project = StringField('Item', validators=[DataRequired()])
    submit = SubmitField('Save')

# class AddProjectForm(FlaskForm):
#     id = IntegerField('id', validators=[DataRequired()])
#     project = StringField('Item', validators=[DataRequired()])
#     submit = SubmitField('Save')


class AddBankItemForm(FlaskForm):
    bi_date =     DateField('Date', validators=[DataRequired()])
    bank_id =  IntegerField('Bank', validators=[DataRequired()])
    bi_amount =  FloatField('Amount', validators=[DataRequired()])
    vendor = StringField('Vendor', validators=[DataRequired()])
    submit = SubmitField('Save')

class GetSalesTaxForm(FlaskForm):
    street = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip = StringField('ZIP', validators=[DataRequired()])
    purchase_amount =  FloatField('Purchase Amount', validators=[DataRequired()])
    submit = SubmitField('Get tax amount')



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
        email_exists = User.check_email_exists(email.data)
        if email_exists:
            raise ValidationError('That email address is already in use.')
