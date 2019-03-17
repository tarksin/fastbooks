from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_login import current_user, login_user, logout_user
from app.models import User, Expense, BankItem, Expcat, Todo, Project
from app import app
from app.forms import LoginForm, AddExpenseForm, AddBankItemForm, AddExpcatForm, AddTodoForm, AddProjectForm
import pymysql.cursors
import pymysql
# import maxxDB


#--------------------------------  /index         -----------------------------------
@app.route('/')
@app.route('/index')
def index():
    centers = [
    {'name':'Cyclotron Pathology Lab', 'director':'Julia Spasm, PhD'},
    {'name':'Magnetic Resonance Nutrition Center', 'director':'Carlos Hechtmann, PhD'},
    {'name':'Curiosity Integration Center', 'director':'Miguel Unamuno, PhD'},

    ]
    return render_template('index.html', headline='K-State Research Centers', centers=centers)


#--------------------  /expenses and /bankitems         -----------------------------------
@app.route('/bankitems')
def bankitems():
    expense_list = Expense.get_expenses()
    bankitems = BankItem.get_bankitems()
    return render_template('expenses.html', expense_list=expense_list, bankitems=bankitems, header_text="Expenses")


@app.route('/expenses')
def expenses():
    expense_list = Expense.get_expenses()
    bankitems = BankItem.get_bankitems()
    return render_template('expenses.html', expense_list=expense_list, bankitems=bankitems, header_text="Expenses")

#--------------------  /expcat         -----------------------------------
@app.route('/expcats', methods=["GET", "POST"])
def expcats():
    form = AddExpcatForm()
    expcats = Expcat.get_expcats()
    if request.method== 'POST':
        ex = Expcat(
            request.form['id'],
            request.form['expcat']
            )
        ex.create()
        return redirect(url_for('expenses'))

    return render_template('expcats.html', form=form, expcats=expcats, header_text="Expense categories")

#---------------------- add_todo  ------------------------------------
# @app.route('/add_todo', methods=["GET","POST"])
# def todo():
#     add_todo_form = AddTodoForm(request.form)
    #add_project_form = AddProjectForm()
    # todos = Todo.get_todos()
    # if request.method== 'POST':
    #     t = Todo(
    #         request.form['todo'], request.form['project_id']
    #          )
    #     t.create()
    #     return redirect(url_for ('todo'))

    # return render_template('test.html',  testdata = "Testing add_todo 65")



#--------------------  /todo         -----------------------------------
@app.route('/todo', methods=["GET","POST"])
def todo():
    # if user logged in ...
    #add_todo_form = AddTodoForm()
    project_form = AddProjectForm(formname='project_form')
    add_todo_form = AddTodoForm(formname='todo_form')

    todos = Todo.get_todos()
    projects = Project.get_projects()

    if  request.method == 'POST':
    #    return redirect(url_for ('xxxxxxtodotodo'))
        x = request.form['formname']

        if x == 'project_form':
            p = Project( request.form['project']
                )
            p.create()
            todos = Todo.get_todos()
            projects = Project.get_projects()

            return render_template('todo.html', todo_form=add_todo_form, project_form=project_form, header_text = x,
                                                todos=todos, projects=projects)


        elif x == 'todo_form':
            #td = request.form['todo']
            t = Todo(
                request.form['todo'], request.form['project_id']
                )
            t.create()
            todos = Todo.get_todos()
            projects = Project.get_projects()
            return render_template('todo.html', todo_form=add_todo_form, project_form=project_form, header_text = x,
                                                todos=todos, projects=projects)

#    add_project_form = AddProjectForm()
#  projectform=AddProjectForm,
    return render_template('todo.html', todo_form=add_todo_form, project_form=project_form,  header_text="GET /todo()",
                                        todos=todos, projects=projects)
#------------------------------------------------------------------------

#--------------------  /add_expense         -----------------------------------
@app.route('/add_expense', methods=["GET","POST"])
def add_expense():
    form = AddExpenseForm()
    if request.method == "POST":
#     def __init__(expdate, expdesc, expamount, expcat, vendor):

        e = Expense(
                request.form['expdate'],
                request.form['expdesc'],
                request.form['expamount'],
                request.form['expcat'],
                request.form['vendor'] )
        e.create()

        return redirect(url_for('expenses'))
#  "> [{'expcat': 'Books/magazine', 'id': 2}, {'expcat': 'Cars: gas', 'id': 14},
#      {'expcat': 'maxxixma', 'id': 150},     {'expcat': 'Miscellaneous', 'id': 98}, {'expcat': 'coffee', 'id': 39}]
    the_cats = Expcat.get_expcats()
    form.expcat.choices=[(c['id'], c['expcat']) for c in the_cats]
    #choices =  Expcat.get_expcats()
    return render_template('add_expense.html', form=form, header_text="Add expense")





#--------------------  /add_bankitem         -----------------------------------
@app.route('/add_bankitem', methods=["GET","POST"])
def add_bankitem():
    form = AddBankItemForm()
    if request.method == "POST":

        b = BankItem(
                request.form['bi_date'],
                request.form['bank_id'],
                request.form['bi_amount'],
                request.form['vendor'] )
        b.create()

        return redirect(url_for('expenses'))

    return render_template('add_bankitem.html', form=form, header_text="Add bankitem")

#--------------------  /login         -----------------------------------
@app.route('/login', methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # user = User( username=form.username.data,  pwhash=form.password.data)
        flash('1a form data: {}'.format(form.username.data))

        # user_exists = User.check_user_exists(form.username.data) # User.check_user_exists(form.username.data)
        expenses = User.get_expenses(form.username.data) # User.check_user_exists(form.username.data)


        # flash('1b user_exists = {}'. format(user_exists))
        flash(expenses)
        # if not user_exists:
        #     flash('2 User name is incorrect')
        #     return redirect(url_for('login'))
        flash('3 User name is correct: {}'.format(form.username.data))

        password_exists =  User.check_password_exists(form.password.data)
        if not password_exists:
            flash('4 Password is incorrect')
            return redirect(url_for('login'))
            #flash('Invalid username or password')

#        login_user(user, remember=form.remember_me.data)
        flash('5 Password is correct: {}'.format(form.password.data))

        flash('6 Login is requested for user {}, remember_me={}'.format(
                 form.username.data, form.remember_me.data))
        #return redirect(url_for('expenses',  expense_list=expenses))
        return render_template('expenses.html', expense_list=expenses, header_text="Expenses")



    return render_template('login.html', form=form)

#--------------------  /register         -----------------------------------
@app.route('/register', methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('form data: {}'.format(form.username.data))

        user_exists = User.check_user_exists(form.username.data)
        if user_exists: # is None or not user.check_password(form.password.data):
            flash('User account already exists')
            return redirect(url_for('register'))
        else:
            flash('username is {}'.format(form.username.data))

        # email_exists = User.check_email_exists(form.email.data)
        # if email_exists: #    is None or not user.check_password(form.password.data):
        #     flash('Email address already registered')
        #     return redirect(url_for('register'))
        # else:
        #     flash('email: {}'.format(form.email.data))

        #login_user(user, remember=form.remember_me.data)
        flash('Login is requested for user {}, remember_me={}'.format(
                 form.username.data, form.remember_me.data))
        return redirect(url_for('index'))

    return render_template('register.html', form=form, header_text="Log in")



#--------------------  /logout         -----------------------------------
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# ---------------------- TEST  --------------------------
# Connect to the database
@app.route('/mysql')
def mysql():

    connection = pymysql.connect(host='localhost',
                             user='maxxblog',
                             password='xnynzn987',
                             db='fastbooks',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
        # Create a new record
            sql = "SELECT * FROM expenses"
            cursor.execute(sql)

            result = cursor.fetchone()

    finally:
        connection.close()
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    #connection.commit()
    if result:
        return jsonify(result)
    else:
        return "No joy"
#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
#         cursor.execute(sql, ('webmaster@python.org',))
#         result = cursor.fetchone()
#         print(result)
# finally:
#     connection.close()
#-----------------------------------------------------------
