from flask import render_template, flash, redirect, url_for, jsonify, request, session
# from flask_login import current_user, login_user, logout_user
from app.models import User, Expense, BankItem, Expcat, Todo, Project, Report
from app import app
from app.forms import LoginForm, AddExpenseForm, AddBankItemForm, AddExpcatForm, AddTodoForm, AddProjectForm, GetSalesTaxForm, ReportForm, RegistrationForm
import pymysql.cursors
import pymysql
from client import AvataxClient
import logging
import json
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


@app.route('/report', methods=["GET","POST"])
def report():
    form = ReportForm()
    if request.method == "POST":
        # alpha = request.form['by_cat']
        # alpha = request.form['startdate']
        # beta = request.form['enddate']
        #
        is_checked = request.form.get('by_cat')
        single_cat_id = request.form.get('single_cat_id')
        if is_checked:
            # return render_template('404.html')
            cat_list = Report.expenses_by_cat(request.form['startdate'], request.form['enddate'])
            return render_template('report_cats.html', cats=cat_list, header_text="Category totals")

        elif single_cat_id:
            single_list = Report.expenses_single_cat(request.form['startdate'], request.form['enddate'], single_cat_id)
            # return render_template('report_cats.html', cats=cat_list, header_text="Category totals")
            return render_template('expenses.html', expense_list=single_list, header_text="Expenses for cat {}".format(single_cat_id))

        else:
            expense_list = Report.expense_report(request.form['startdate'], request.form['enddate'])
        #
        # r = Report(
        #         request.form['startdate'],
        #         request.form['enddate'],
        #         request.form['by_cat']
        #         )
        # cats = [{"cat":"alpha", "total":"111.11"}, {"cat":"beta", "total":"222.2"}]
        # cats = r.exp_report_by_cat()

            return render_template('report_results.html', expense_list=expense_list, bankitems=bankitems, header_text="Expenses")
    return render_template('report.html', form=form, header_text="Reports")


#--------------------  /e404         -----------------------------------

@app.route('/e404')
def e404():
    # return render_template('expenses.html', expense_list=expense_list, bankitems=bankitems, header_text="Expenses")
    return render_template('404.html')

#--------------------  /expenses         -----------------------------------

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

    if request.method == 'POST':
    #    return redirect(url_for ('xxxxxxtodotodo'))
        x = request.form['formname']

        if x == 'project_form':
            p = Project( request.form['project'])
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

# -------------------------------------------------------
@app.route('/test12', methods=['GET','POST'])
def return12():
    city='Manhattan'
    line1='301 Bluemont Ave'
    postalCode='66502'
    region='KS'
    purchase_amount=10000

    client = AvataxClient('fastbooks','1.0','W540','production')
    client = client.add_credentials('2000102624','74C6AC3D78E9E859')

    tax_document = {
      'addresses': {'SingleLocation': {'city': city,
                                       'country': 'US',
                                       'line1': line1,
                                       'postalCode': postalCode,
                                       'region': region}},
      'commit': False,
      'companyCode': 'DEFAULT',
      'currencyCode': 'USD',
      'customerCode': 'XYZ',
      'date': '2018-10-13',
      'description': 'Silk',
      "lines": [ { "amount": purchase_amount } ],
      'purchaseOrderNo': '2018-04-12-001',
      'type': 'SalesInvoice'}

    transaction_response = client.create_transaction(tax_document)
    data = transaction_response.text

    # OK to here
    data = '[' + data + ']'
    data = json.loads(str(data))
    if data:
        return "Tax amount: {}".format(data[0]["totalTax"])


    return tax_document['addresses']['SingleLocation']['line1']
    # return "return from /test12"

# -------------------------------------------------------
def getTax(city,line1,postalCode,region,purchase_amount):
    tax_document = {
      'addresses': {'SingleLocation': {'city': city,
                                       'country': 'US',
                                       'line1': line1,
                                       'postalCode': postalCode,
                                       'region': region}},
      'commit': False,
      'companyCode': 'DEFAULT',
      'currencyCode': 'USD',
      'customerCode': 'XYZ',
      'date': '2018-10-13',
      'description': 'Silk',
      "lines": [ { "amount": purchase_amount } ],
      'purchaseOrderNo': '2018-04-12-001',
      'type': 'SalesInvoice'}
    print('131 getTax')
    client = AvataxClient('fastbooks','1.0','W540','production')
    client = client.add_credentials('2000102624','74C6AC3D78E9E859')
    print('134 getTax')
    transaction_response = client.create_transaction(tax_document)
    print('136 getTax')
    data = transaction_response.text #json.loads(
    print('138 getTax')
    return data

#------------------------------------------------------------------------
@app.route('/tax', methods = ['GET', 'POST'])
def get_sales_tax():
    form = GetSalesTaxForm()
    tax_amount = 9.99
    display_string1 =' '
    display_string2 = ' '
    # progress='0'
    # app.logger.debug('147 routes.py')
    if request.method == "POST":
    #    try:
        # progress+='1'

        city = request.form['city']
        state = request.form['state']
        postalCode= request.form['zip']
        line1 = request.form['street']
        purchase_amount = request.form['purchase_amount']

            # city,line1,postalCode,region,amount
        # app.logger.debug('156 routes.py: {}'.format(line1))
        # progress+='2'

        tax_amount = getTax(city,line1,postalCode,state,purchase_amount)

        tax2 = json.loads(tax_amount)

        # we_got_to_here = "159:{}".format(str(tax_amount))
    #    except:
        # print('161 Exception:')
        # print('162 {}'.format(tax_amount))
        #session["sales_tax"] = tax_amount

        # street = StringField('Street Address', validators=[DataRequired()])
        # city = StringField('City', validators=[DataRequired()])
        # state = StringField('State', validators=[DataRequired()])
        # zip = StringField('ZIP', validators=[DataRequired()])
        # purchase_amount =  FloatField('Purchase Amount', validators=[DataRequired()])
        # submit = SubmitField('Save')
        # app.logger.debug('172 routes.py')
        # ret =  # {} {}}: ".format(progress, line1)
        taxObj = {}
        taxObj['city'] = city
        taxObj['state'] = state
        taxObj['purchase_amount'] = purchase_amount
        taxObj['sales_tax'] = tax2['totalTax']

        print('228 type:{}',format(type(purchase_amount)))  #string
        print('229 type:{}',format(type(tax2['totalTax'])))  #float
        totalsale=float(purchase_amount) + tax2['totalTax']

        # "{:.2f}".format(float(value))

        display_string1 = "The sales tax on ${} at {} in {}, {} is ${}.".format(   "{:.2f}".format(float(purchase_amount)), line1, city, state,"{:.2f}".format(tax2['totalTax']))

        display_string2 = "The total cost of that item is ${}.".format( "{:.2f}".format(totalsale))
        # return render_template('test2.html', taxObj=taxObj, display_string1 = display_string1, display_string2 = display_string2)# testdata = tax2['totalTax'] ) # "return from POST /tax 133"
        return render_template('get_sales_tax.html', form=form, header_text="Get sales tax amount",display_string1=display_string1, display_string2 = display_string2)
    return render_template('get_sales_tax.html', form=form, header_text="Get sales tax amount")

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
                request.form['vendor'])
        e.create()

        return redirect(url_for('expenses'))
#  "> [{'expcat': 'Books/magazine', 'id': 2}, {'expcat': 'Cars: gas', 'id': 14},
#      {'expcat': 'maxxixma', 'id': 150},     {'expcat': 'Miscellaneous', 'id': 98}, {'expcat': 'coffee', 'id': 39}]

    taxes = [8.75, 8.95, 9.25]
    the_cats = Expcat.get_expcats()
    form.expcat.choices=[(c['id'], c['expcat']) for c in the_cats]
    #choices =  Expcat.get_expcats()
    return render_template('add_expense.html', form=form, header_text="Add expense", taxes=taxes)





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
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash('1a: {}'.format(form.username.data))
        user = User(form.username.data, 'dummy@email.com', form.password.data)

        if user is None or not user.check_password(form.password.data):
            flash('2a  Invalid username or password: {}'.format(form.username.data))
            return redirect(url_for('login'))
        else:
            flash('3a  Valid username and password(?): {}'.format(form.username.data))
            session['logged_in'] = form.username.data
        # login_user(user)
        return redirect(url_for('index'))

        # user_exists = User.check_user_exists(form.username.data) # User.check_user_exists(form.username.data)
        # expenses = User.get_expenses(form.username.data) # User.check_user_exists(form.username.data)


        # flash('1b user_exists = {}'. format(user_exists))
        # flash(expenses)
        # if not user_exists:
        #     flash('2 User name is incorrect')
        #     return redirect(url_for('login'))
#         flash('3 User name is correct: {}'.format(form.username.data))
#
#         password_exists =  User.check_password_exists(form.password.data)
#         if not password_exists:
#             flash('4 Password is incorrect')
#             return redirect(url_for('login'))
#             #flash('Invalid username or password')
#
# #
#         flash('5 Password is correct: {}'.format(form.password.data))
#
#         flash('6 Login is requested for user {}, remember_me={}'.format(
#                  form.username.data, form.remember_me.data))
#         return redirect(url_for('index'))
        # return render_template('expenses.html', expense_list=expenses, header_text="Expenses")



    return render_template('login.html', form=form)

#--------------------  /register         -----------------------------------
@app.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('form data: {}'.format(form.username.data))

        user_exists = User.check_user_exists(form.username.data)
        if user_exists:  # is None or not user.check_password(form.password.data):
            flash('User account already exists')
            return redirect(url_for('register'))
        else:
            flash('username is {}'.format(form.username.data))
            user = User(form.username.data,form.email.data, form.password.data)
            user.create()
        # email_exists = User.check_email_exists(form.email.data)
        # if email_exists: #    is None or not user.check_password(form.password.data):
        #     flash('Email address already registered')
        #     return redirect(url_for('register'))
        # else:
        #     flash('email: {}'.format(form.email.data))

        #login_user(user, remember=form.remember_me.data)
            flash('Registered: {}'.format(form.username.data))
            return redirect(url_for('index'))

    return render_template('register.html', form=form, header_text="Log in")


#--------------------  /logout         -----------------------------------
@app.route('/logout')
def logout():
    session['logged_in'] = None
    return redirect(url_for('index'))


#--------------------  /ab         -----------------------------------
@app.route('/hb2u')
def hb2u():
    return render_template('ab.html')


#--------------------  /ab         -----------------------------------
@app.route('/maxxdoc')
def maxxdoc():
    return render_template('maxxdoc.html')



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
#--------------------  /logout         -----------------------------------
@app.route('/data_science')
def lc101_index():
    return render_template('data_science.html')


@app.route('/lcsignup', methods=["GET", "POST"])
def lcsignup():
    username = ''
    email = ''
    if request.method=="POST":
        username_error = ''
        password_error = ''
        email_error = ''

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        verify = request.form["verify"]


        if len(email) > 0:
            count_amp = 0
            count_sp = 0
            count_punto = 0
            for  c in email:
                if c == '@':
                    count_amp +=1
                if c == ' ':
                    count_sp +=1
                if c == '.':
                    count_punto +=1

            if not ( count_amp == 1 and count_punto == 1 and count_sp == 0):
                email_error = 'Email address must contain one "@", one period, and no spaces'
            if (len(email) < 3 or len(email) > 20):
                email_error = 'Email address must contain between 3 and 20 characters'

        if len(username)==0:
            username_error = 'You must provide a username'
        if ' ' in username:
            username_error = 'Spaces not allowed in username'
        if len(username) < 3:
            username_error = 'Username must contain at least three characters'
        if len(username) > 20:
            username_error = 'Username must contain no more than 20 characters'

        if len(password)==0:
            password_error = 'You must provide a password'
        elif (len(password) < 3 or len(password) > 20):
            password_error = 'Password must contain between 3 and 20 characters'
        else:
            if not password==verify:
                password_error = 'Passwords do not match'

        if username_error or email_error or password_error:
            return render_template('home.html',username=username, email=email, username_error=username_error, email_error=email_error,password_error=password_error  )
        else:
            return render_template('welcome.html', username=username)

    return render_template('home.html')
