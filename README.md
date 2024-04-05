<div align="center">

<br />
<h1 align="center">CT5173 - Final Project</h1>
<h3 align="center">CA1: Building a Secure Website</h3>

  <p align="center">
    The purpose of this project is to build a secure website using technologies covered in lecture and lab material. 

<br />

</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#introduction">Introduction</a></li>
    <li><a href="#running-the-project">Running the Project</a></li>
    <li><a href="#website-usage-guidelines">Website Usage Guidelines</a></li>
    <li><a href="#use-cases-description">Use-Cases Description</a></li>
    <li><a href="#page-structure">Page Structure</a></li>
    <li><a href="#security-features">Security Features</a></li>
    <ol type="i">
      <li><a href="#i-project-baseline-security-features">Project Baseline Security Features</a></li>
      <li><a href="#ii-additional-security-features">Additional Security Features</a></li>
    </ol>
    <li><a href="#technologies-used">Technologies Used</a></li>
  </ol>
</details>

<!-- INTRODUCTION -->
## Introduction

This project is a secure website built using Flask, a micro web framework in Python. The website allows users to sign up, log in, and interact with a database to manage their profiles and recipes. The primary goal of the website is to demonstrate secure web programming practices, including authentication, password hashing, session management, and input sanitization.

<!-- GETTING STARTED -->
## Running the Project

<ol> 
  <li><b>Download the Source Code:</b></li>
    <ul>
      <li>Receive a copy of the source code in a zip file.</li>
    </ul>
  <li><b>Extract the Zip File:</b></li>
    <ul>
      <li>Extract the contents of the zip file to a desired location on your local machine.</li>
    </ul>
  <li><b>Import the Project into IDE (PyCharm/VSCode):</b></li>
    <ul>
      <li>Import the project into an IDE of choice (PyCharm/VSCode), by either dragging and dropping the unzipped folder inot the IDE or using "Open Folder".</li>
    </ul>
  <li><b>Install Dependencies:</b></li>
    <ul>
      <li>Open a terminal and navigate to the project directory.</li>
      <li>Run the following command to install dependencies: <code>pip install -r requirements.txt</code></li>
      <li>Or follow IDE prompts to install dependencies.</li>       
    </ul>
  <li><b>Set Up the Database:</b></li>
    <ul>
      <li>Ensure you have SQLite installed on your local machine.</li>
    </ul>
  <li><b>Run the Application:</b></li>
    <ul>
      <li>Execute the following command in the terminal: <code>python main.py</code></li>
      <li>Or simply run the <code>main.py</code> using the run button.</li>
      <li>The website will be accessible at <code>http://localhost:5000</code> (or <code>http://127.0.0.1:5000/</code>) by default.</li>
    </ul>
</ol>

<!-- USAGE GUIDELINES -->
## Website Usage Guidelines

<ol>
  <li><b>Sign Up:</b></li>
    <ul>
      <li>Navigate to the sign-up page and fill in the required details.</li>
      <li>Click the "Sign Up" button to create an account.</li>
    </ul>
  <li><b>Log In:</b></li>
    <ul>
      <li>After signing up, navigate to the log-in page and enter your credentials.</li>
      <li>Click the "Log In" button to access your profile.</li>
    </ul>
  <li><b>Profile Management:</b></li>
    <ul>
      <li>Once logged in, you can:</li>
        <ul>
          <li>View and edit your profile details, including email, name, gender, and bio.</li>
          <li>Add, edit, or delete recipes associated with your profile.</li>
          <li>View all recipes added by you and other users.</li>
        </ul>
    </ul>
  <li><b>Search Users:</b></li>
    <ul>
      <li>Users can search for other users by entering their username in the search bar.</li>
    </ul>
  <li><b>Log Out:</b></li>
    <ul>
      <li>To log out, simply click the "Log Out" button at the bottom of the page.</li>
    </ul>
</ol>

<!-- USE-CASES -->
## Use-Cases Description 

<ol>
<li><b>User Registration:</b></li>
<ul>
<li><b>Actor:</b> New User</li>
<li><b>Description:</b> A new user visits the website and registers for an account by providing their username, email, password, and other optional details like first name, last name, gender, and bio.</li>
<li><b>Steps:</b></li>
<ol>
<li>User navigates to the signup page.</li>
<li>User fills out the registration form.</li>
<li>User submits the form.</li>
<li>System validates the input data.</li>
<li>If validation is successful, the system creates a new user account and redirects the user to the login page.</li>
<li>If validation fails, appropriate error messages are displayed.</li>
</ol>
</ul>
<li><b>User Login:</b></li>
<uL>
<li><b>Actor:</b> Registered User</li>
<li><b>Description:</b> An existing user logs in to their account to access the website's features and functionalities.</li>
<li><b>Steps:</b></li>
<ol>
<li>User navigates to the login page.</li>
<li>User enters their username and password.</li>
<li>User submits the login form.</li>
<li>System validates the user's credentials.</li>
<li>If the credentials are correct, the system logs the user in and redirects them to their profile page.</li>
If the credentials are incorrect, appropriate error messages are displayed.</li>
</ol>
</ul>
<li><b>View Profile:</b></li>
<ul>
<li><b>Actor:</b> Registered User</li>
<li><b>Description:</b> A user views their own profile information, including username, email, first name, last name, gender, bio, and their own recipes.</li>
<li><b>Steps:</b></li>
<ol>
<li>User logs in to their account.</li>
<li>User navigates to the profile page.</li>
<li>System retrieves and displays the user's profile information and recipes.</li>
</ol>
</ul>
<li><b>Edit Profile:</b></li>
<ul>
<li><b>Actor:</b> Registered User</li>
<li><b>Description:</b> A user updates their profile information such as email, first name, last name, gender, or bio.</li>
<li><b>Steps:</b></li>
<ol>
<li>User logs in to their account.</li>
<li>User navigates to the edit profile page.</li>
<li>User modifies their profile information.</li>
<li>User submits the form.</li>
<li>System validates the input data.</li>
<li>If validation is successful, the system updates the user's profile information in the database and redirects the user to their profile page.</li>
<li>If validation fails, appropriate error messages are displayed.</li>
</ol>
</ul>
<li><b>Add Recipe:</b></li>
<ul>
<li><b>Actor:</b> Registered User</li>
<li><b>Description:</b> A user adds a new recipe to their profile.</li>
<li><b>Steps:</b></li>
<ol>
<li>User logs in to their account.</li>
<li>User navigates to the add recipe page.</li>
<li>User fills out the recipe details such as title, ingredients, method, and type.</li>
<li>User submits the form.</li>
<li>System validates the input data.</li>
<li>If validation is successful, the system adds the new recipe to the user's profile and redirects the user to their profile page.</li>
<li>If validation fails, appropriate error messages are displayed.</li>
</ol>
</ul>
<li><b>Search Users:</b></li>
<ul>
<li><b>Actor:</b> Registered User</li>
<li><b>Description:</b> A user searches for other users by their usernames.</li>
<li><b>Steps:</b></li>
<ol>
<li>User logs in to their account.</li>
<li>User enters a username in the search bar.</li>
<li>User submits the search query.</li>
<li>System retrieves and displays a list of users matching the search query.</li>
<li>User clicks on a username to view the profile of the selected user.</li>
</ol>
</ul>
</ol>

<!-- PAGE STRUCTURE -->
## Page Structure
<ol>
  <li><b><code>index.html</code> (Homepage):</b></li>
    <ul>
      <li>Landing page of the website.</li>
      <li>Provides a brief overview of the website's features and functionalities.</li>
      <li>Includes options for sign-up and log-in.</li>
    </ul>
  <li><b><code>signup.html</code> (Sign-Up Page):</b></li>
    <ul>
      <li>Allows new users to create an account by providing necessary details like username, password, email, etc.</li>
      <li>Contains a form for user registration.</li>
      <li>Upon submission, redirects to the login page.</li>
    </ul>
  <li><b><code>login.html</code> (Log-In Page):</b></li>
    <ul>
      <li>Allows existing users to log in to their accounts.</li>
      <li>Requires username and password for authentication.</li>
      <li>Upon successful login, redirects to the user's profile page.</li>
    </ul>
  <li><b><code>profile.html</code> (User Profile Page):</b></li>
    <ul>
      <li>Displays the user's profile information, including username, email, name, gender, bio, etc.</li>
      <li>Provides options to edit profile details and manage recipes.</li>
      <li>Includes links to view/edit individual recipes and search for other users.</li>
    </ul>
  <li><b><code>edit_profile.html</code> (Edit Profile Page):</b></li>
    <ul>
      <li>Allows users to modify their profile information, including email, name, gender, bio, etc.</li>
      <li>Contains a form for updating profile details.</li>
      <li>Upon submission, updates the user's profile and redirects to the profile page.</li>
    </ul>
  <li><b><code>add_recipe.html</code> (Add Recipe Page):</b></li>
    <ul>
      <li>Enables users to add new recipes to their profile.</li>
      <li>Requires users to input recipe title, ingredients, method, and type (main, desert, side, appetizer).</li>
      <li>Upon submission, adds the new recipe to the user's profile and redirects to the profile page.</li>
    </ul>
  <li><b><code>edit_recipe.html</code> (Edit Recipe Page):</b></li>
    <ul>
      <li>Allows users to edit existing recipes associated with their profile.</li>
      <li>Displays the current recipe details and allows users to modify them.</li>
      <li>Upon submission, updates the recipe details and redirects to the recipe details page.</li>
    </ul>
  <li><b><code>delete_recipe.html</code> (Delete Recipe Page):</b></li>
    <ul>
      <li>Provides an option for users to delete a recipe from their profile.</li>
      <li>Confirms the deletion action before permanently removing the recipe.</li>
      <li>Upon confirmation, deletes the recipe and redirects to the profile page.</li>
    </ul>
  <li><b><code>all_recipes.html</code> (All Recipes Page):</b></li>
    <ul>
      <li>Displays a list of all recipes added by all users.</li>
      <li>Allows users to browse through different recipes available on the website.</li>
      <li>Provides links to view individual recipe details.</li>
    </ul>
  <li><b><code>recipe_details.html</code> (Recipe Details Page):</b></li>
    <ul>
      <li>Shows detailed information about a specific recipe, including title, ingredients, method, type, etc.</li>
      <li>Allows users to view and interact with the recipe, such as editing (if the recipe belongs to the logged-in user) or deleting it.</li>
    </ul>
  <li><b><code>search_results.html</code> (Search Results Page):</b></li>
    <ul>
      <li>Displays search results based on the user's query.</li>
      <li>Shows a list of users or recipes matching the search criteria.</li>
    </ul>
</ol>

<!-- SECURITY FEATURES  -->
## Security Features

### i. Project Baseline Security Features
These baseline features are imported into the project from secure website created as part of lab work during the course of the semester.

<ul>
  <li><b>Password Hashing:</b> User passwords are securely hashed using bcrypt before storage in the database, ensuring that plain-text passwords are not stored.</li>

  <li><b>Session Management:</b> Sessions are managed securely by storing session data server-side and protecting it with a secret key, mitigating the risk of session hijacking.</li>

  <li><b>Login Manager:</b> User authentication is facilitated through Flask-Login's LoginManager, enabling secure management of user sessions and login-related functionalities.</li>

  <li><b>Input Sanitization:</b> User input is sanitized to prevent SQL injection attacks, reducing the risk of unauthorized database access.</li>
  
</ul>

### ii. Additional Security Features
These additional features are implemented in the project to ensure greater security of the website.

<ul>
  <li><b>Session Expiry Handling:</b> Implementation of session expiry handling using a <code style="color:orange">before_request</code> hook to check for session expiration, automatically logging out users if the session has expired to mitigate session fixation attacks.</li>

  <li><b>Session Lifetime Configuration:</b> Configuration of session lifetime to a specific duration, ensuring automatic expiration of user sessions after a set period (<i>10 minutes</i>), reducing the window of opportunity for attackers.</li>

  <li><b>Resetting Session on First Request:</b>  Utilization of a <code style="color:orange">before_first_request</code> hook to reset the session on the first request, ensuring a clean session state for each user and minimizing session-related vulnerabilities.</li>

  <li><b>Route Protection:</b> Certain routes, such as <code style="color:green">/profile</code> and <code style="color:green">/add_recipe</code>, are safeguarded with the <code style="color:orange">@login_required</code> decorator, ensuring that only authenticated users can access these routes and protecting sensitive functionalities from unauthorized access.</li>
  
  <li><b>Authorization:</b> Certain routes and functionalities are restricted to authenticated users only, ensuring that sensitive actions can only be performed by authorized individuals.</li>
</ul>

<!-- TECHNOLOGIES USED -->
## Technologies Used

<ol>
<li><b>Framework:</b> Flask</li>
<li><b>Languages:</b> Python, HTML</li>
<li><b>Database:</b> SQLite</li>
<li><b>Other Tools/Libraries:</b></li>
<ul>
<li><b>Flask-Bcrypt:</b> Flask extension used for password hashing.</li>
<li><b>Flask-Login:</b> Flask extension used for user session management and authentication.</li>
<li><b>Werkzeug:</b> A WSGI utility library for Python, used for password hashing and redirection.</li>
<li><b>sqlite3:</b> Standard Python module for working with SQLite databases.</li>
<li><b>pytz:</b> Python library used for working with time zones.</li>
<li><b>datetime:</b> Python module used for working with dates and times.</li>
</ul>
</ol>
