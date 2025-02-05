from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'meow',
    'database': 'bookhub'
}

@app.route('/login-register', methods=['GET', 'POST'])
def auth():
    action = request.args.get('action', 'login')  # Default action is login

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Handle Registration
        if action == 'register':
            name = request.form['name']
            phone = request.form['phone']
            hashed_password = generate_password_hash(password)

            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (name, email, password, phone)
                    VALUES (%s, %s, %s, %s)
                """, (name, email, hashed_password, phone))
                conn.commit()
                flash("Registration successful! Please login.", "success")
                return redirect('/login-register?action=login')  # Fixed redirect URL
            except mysql.connector.Error as err:
                flash(f"Error: {err}", "danger")
            finally:
                cursor.close()
                conn.close()

        # Handle Login
        elif action == 'login':
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()

                if user and check_password_hash(user['password'], password):
                    session['user_id'] = user['id']
                    session['user_name'] = user['name']
                    flash(f"Welcome, {user['name']}!", "success")
                    return redirect('/dashboard')
                else:
                    flash("Invalid email or password.", "danger")
            finally:
                cursor.close()
                conn.close()

    return render_template('login-register.html', action=action)  # Updated template name

if __name__ == '__main__':
    app.run(debug=True)
