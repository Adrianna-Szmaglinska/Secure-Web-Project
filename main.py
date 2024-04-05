# Importing necessary modules and libraries
from pytz import utc
from flask import Flask, render_template, request, url_for, flash, session
from werkzeug.utils import redirect
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from datetime import timedelta, datetime

# Database file path
db_file = "mySQLite.db"

# Initializing Flask app
app = Flask(__name__)
app.config['ENV'] = "Development"
app.config['DEBUG'] = True
app.config['SESSION_COOKIE_DURATION'] = timedelta(minutes=10)

# Initializing Flask Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initializing Flask Login Manager for user authentication
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loginAction'

# User class for login management
class User():
    def __init__(self, username):
        self.username = username

    # Methods required for Flask Login extension
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)

# Function to load user by username
@login_manager.user_loader
def load_user(username):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USER WHERE Username=?", (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        return User(username)
    return None

# Setting secret key for session management
app.secret_key = 'super secret key'

# Function to reset session
def reset_session():
    session.clear()

# Function to run before the first request
@app.before_first_request
def before_first_request():
    reset_session()

# Function to run before each request
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
    session.modified = True

    # Check if the user is logged in and update last activity timestamp
    if current_user.is_authenticated:
        if 'last_activity' not in session:
            session['last_activity'] = datetime.now(utc)
        else:
            # Convert stored timestamp to aware datetime
            stored_last_activity = session['last_activity']
            current_time = datetime.now(utc)

            # Check if the session has expired and log out the user
            if current_time - stored_last_activity > timedelta(minutes=10):
                logout_user()
                session.pop('last_activity', None)
            else:
                session['last_activity'] = stored_last_activity

# Route for home page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route for user signup
@app.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for('profile'))
    return render_template("signup.html")

# Route for signup form submission
@app.route('/signupAction', methods=['POST'])
def signupAction():
    username = request.form.get("username")
    password = request.form.get("password")

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    print("True Password:", password, ", Hashed Password:", hashed_password)
    password = hashed_password

    email = request.form.get("email", "")
    fname = request.form.get("fname", "")
    lname = request.form.get("lname", "")
    gender = request.form.get("gender", "")
    bio = request.form.get("bio", "")

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        myquery = "INSERT INTO USER (Username,Password,Email,First_Name,Last_Name,Gender,Bio) VALUES ('" + username + "','" + password + "','" + email + "','" + fname + "','" + lname + "','" + gender + "','" + bio + "')"
        print("My query is: ", myquery)
        cursor.execute(myquery)
        conn.commit()

        flash("Account created successfully.", "success")
        return redirect(url_for('login'))

    except Error as e:
        flash(f"Failed to signup. Error: {e}", "danger")
        return redirect(url_for('signup'))
    finally:
        if conn:
            conn.close()

    flash("Account created successfully.")
    return redirect(url_for('login'))

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    ## If user is already logged in we need to redirect them to their profile
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for('profile'))
    return render_template("login.html")

# Route for login form submission
@app.route('/loginAction', methods=['POST'])
def loginAction():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        myquery = "SELECT Password FROM USER WHERE Username='" + username + "'"
        data = cursor.execute(myquery)
        passwordInDB = None
        for row in data:
            passwordInDB = row[0]

        if passwordInDB:
            validPassword = bcrypt.check_password_hash(passwordInDB, password)

            if validPassword:
                login_user(User(username))
                session['last_activity'] = datetime.now(utc)
                flash("You are now logged in.", "success")
                return redirect(url_for('profile'))
            else:
                flash("Your username or password are incorrect! Try to login again.", "danger")
                return redirect(url_for('login'))
        else:
            flash("Your username or password are incorrect! Try to login again.", "danger")
            return redirect(url_for('login'))

    except Error as e:
        flash(f"Failed to login. Error: {e}", "danger")
        return redirect(url_for('login'))
    finally:
        if conn:
            conn.close()

    flash("You are now logged in.")
    return redirect(url_for('profile'))

# Route for user profile
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    myusername = current_user.username
    user_id = current_user.get_id()

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Retrieve user details
        user_query = "SELECT Email, First_Name, Last_Name, Gender, Bio FROM USER WHERE Username=?"
        user_data = cursor.execute(user_query, (myusername,))
        user_row = user_data.fetchone()

        if not user_row:
            return "Error: the Username does not exist"

        myemail, myfname, mylname, mygender, mybio = user_row

        # Retrieve user's recipes
        recipes_query = "SELECT * FROM RECIPES WHERE User_Id=?"
        recipes_data = cursor.execute(recipes_query, (user_id,))
        user_recipes = recipes_data.fetchall()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

    return render_template("profile.html", username=myusername, email=myemail, fname=myfname, lname=mylname,
                           gender=mygender, bio=mybio, user_recipes=user_recipes)

# Route for displaying another user's profile
@app.route('/user_profile/<username>', methods=['GET', 'POST'])
@login_required
def user_profile(username):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Retrieve user details
        user_query = "SELECT Email, First_Name, Last_Name, Gender, Bio FROM USER WHERE Username=?"
        user_data = cursor.execute(user_query, (username,))
        user_row = user_data.fetchone()

        if not user_row:
            return "Error: the Username does not exist"

        myemail, myfname, mylname, mygender, mybio = user_row

        # Retrieve user's recipes
        user_id_query = "SELECT Username FROM USER WHERE Username=?"
        cursor.execute(user_id_query, (username,))
        user_id = cursor.fetchone()[0]

        recipes_query = "SELECT * FROM RECIPES WHERE User_Id=?"
        cursor.execute(recipes_query, (user_id,))
        user_recipes = cursor.fetchall()

        return render_template("profile.html", username=username, email=myemail, fname=myfname, lname=mylname,
                               gender=mygender, bio=mybio, user_recipes=user_recipes)

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

    return "Error fetching user profile"

# Route for user profile editing
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

    if request.method == 'POST':
        # Retrieve form data
        email = request.form.get("email")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        gender = request.form.get("gender")
        bio = request.form.get("bio")

        # Update profile information in the database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        try:
            update_query = "UPDATE USER SET Email=?, First_Name=?, Last_Name=?, Gender=?, Bio=? WHERE Username=?"
            cursor.execute(update_query, (email, fname, lname, gender, bio, current_user.username))
            conn.commit()
            flash("Profile updated successfully", "success")
            return redirect(url_for('profile'))
        except Error as e:
            flash(f"Failed to update profile. Error: {e}", "danger")
        finally:
            conn.close()

    # Retrieve user details for pre-filling the form
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT Email, First_Name, Last_Name, Gender, Bio FROM USER WHERE Username=?", (current_user.username,))
    user_data = cursor.fetchone()
    conn.close()

    # Check if user_data is not None
    if user_data:
        user = {
            'email': user_data[0],
            'fname': user_data[1],
            'lname': user_data[2],
            'gender': user_data[3],
            'bio': user_data[4]
        }
    else:
        flash("User data not found", "danger")
        return redirect(url_for('profile'))

    return render_template("edit_profile.html", user=user)

# Route for searching users
@app.route('/search', methods=['POST'])
@login_required
def search():
    search_input = request.form.get('search_input')

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Perform the search in the 'users' table
        search_query = "SELECT Username FROM USER WHERE Username LIKE ?"
        cursor.execute(search_query, ('%' + search_input + '%',))
        search_results = [{'username': row[0]} for row in cursor.fetchall()]

        return render_template('search_results.html', search_query=search_input, search_results=search_results)

    except Error as e:
        flash(f"Error during search: {e}", "danger")
        return redirect(url_for('search'))

    finally:
        if conn:
            conn.close()

# Route for adding a new recipe
@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        method = request.form['method']
        recipe_type = request.form['type']

        if not title or not ingredients or not method or not recipe_type:
            flash('All fields are required', 'danger')
        else:
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO RECIPES (Title, Ingredients, Method, Type, User_Id) VALUES (?, ?, ?, ?, ?)
                """, (title, ingredients, method, recipe_type, current_user.get_id()))

                conn.commit()

                flash('Recipe added successfully', 'success')
                return redirect(url_for('profile'))
            except Error as e:
                flash(f"Failed to add recipe. Error: {e}", "danger")
                return redirect(url_for('add_recipe'))

            except Error as e:
                flash("Failed to add recipe. Try again!")
                return redirect(url_for('add_recipe'))
            finally:
                if conn:
                    conn.close()

            flash('Recipe added successfully', 'success')
            return redirect(url_for('profile'))

    return render_template('add_recipe.html')

# Route for adding a recipe action
@app.route('/add_recipe_action', methods=['POST'])
@login_required
def add_recipe_action():
    title = request.form['title']
    ingredients = request.form['ingredients']
    method = request.form['method']
    recipe_type = request.form['type']

    if not title or not ingredients or not method or not recipe_type:
        flash('All fields are required', 'danger')
        return redirect(url_for('add_recipe'))

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO RECIPES (Title, Ingredients, Method, Type, User_Id) VALUES (?, ?, ?, ?, ?)
        """, (title, ingredients, method, recipe_type, current_user.get_id()))

        conn.commit()

    except Error as e:
        flash(f"Failed to add recipe. Error: {e}")
        return redirect(url_for('add_recipe'))
    finally:
        if conn:
            conn.close()

    flash('Recipe added successfully', 'success')
    return redirect(url_for('profile'))

# Route for displaying recipe details
@app.route('/recipe_details/<int:recipe_id>', methods=['GET'])
@login_required
def recipe_details(recipe_id):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Fetch details of the specified recipe_id from the RECIPES table
        cursor.execute("SELECT * FROM RECIPES WHERE Id=?", (recipe_id,))
        recipe_data = cursor.fetchone()

        if not recipe_data:
            return "Recipe not found"

        recipe = {
            'id': recipe_data[0],
            'title': recipe_data[1],
            'ingredients': recipe_data[2],
            'method': recipe_data[3],
            'type': recipe_data[4],
            'user_id': recipe_data[5],
        }

        return render_template('recipe_details.html', recipe=recipe)

    except Error as e:
        print(e)
        return "Error fetching recipe details"

    finally:
        if conn:
            conn.close()

# Route for displaying all recipes
@app.route('/all_recipes', methods=['GET'])
@login_required
def all_recipes():
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Fetch all recipes from the RECIPES table
        cursor.execute("SELECT * FROM RECIPES")
        recipes = cursor.fetchall()

        return render_template('all_recipes.html', recipes=recipes)

    except Error as e:
        flash("Failed to retrieve recipes. Try again!")
        return redirect(url_for('profile'))

    finally:
        if conn:
            conn.close()

# Route for editing a recipe
@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("""
                SELECT Title, Ingredients, Method, Type FROM RECIPES WHERE Id=? AND User_Id=?
            """, (recipe_id, current_user.get_id()))
        row = cursor.fetchone()

        if not row:
            flash("Recipe not found or you don't have permission to edit", 'danger')
            return redirect(url_for('profile'))

        if request.method == 'POST':
            title = request.form['title']
            ingredients = request.form['ingredients']
            method = request.form['method']
            recipe_type = request.form['type']

            if not title or not ingredients or not method or not recipe_type:
                flash('All fields are required', 'danger')
            else:
                cursor.execute("""
                        UPDATE RECIPES SET Title=?, Ingredients=?, Method=?, Type=? WHERE Id=? AND User_Id=?
                    """, (title, ingredients, method, recipe_type, recipe_id, current_user.get_id()))

                conn.commit()
                flash('Recipe edited successfully', 'success')
                return redirect(url_for('profile'))

    except Error as e:
        flash("Failed to edit recipe. Try again!")
        return redirect(url_for('profile'))
    finally:
        if conn:
            conn.close()

    return render_template('edit_recipe.html', recipe_id=recipe_id, recipe={'id': recipe_id, 'title': row[0], 'ingredients': row[1], 'method': row[2], 'type': row[3]})

# Route for deleting a recipe
@app.route('/delete_recipe/<int:recipe_id>')
@login_required
def delete_recipe(recipe_id):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM RECIPES WHERE Id=? AND User_Id=?
        """, (recipe_id, current_user.get_id()))

        conn.commit()
        flash('Recipe deleted successfully', 'success')

    except Error as e:
        flash("Failed to delete recipe. Try again!")
    finally:
        if conn:
            conn.close()

    return redirect(url_for('profile'))

# Route for user logout
@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    flash("Logout successful.")
    return redirect(url_for('login'))

# Main block to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)