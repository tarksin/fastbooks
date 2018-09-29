
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
