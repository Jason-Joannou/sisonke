from flask import Blueprint, render_template, request, redirect, url_for, flash,session,jsonify
import sqlite3
from database import get_db_connection

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('landingpage.html')


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        id_type = request.form['id_type']
        id_number = request.form['id_number']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Users (phone_number, password, first_name, last_name, date_of_birth, id_type, id_number)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (phone_number, password, first_name, last_name, date_of_birth, id_type, id_number))
            conn.commit()
            print(f"User added successfully: {phone_number}")  # Debug print
            flash('Account created successfully', 'success')
            return redirect(url_for('main.login'))
        except sqlite3.IntegrityError as e:
            print(f"Database integrity error: {e}")  # Debug print
            flash('Phone number already exists', 'error')
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")  # Debug print
            flash(f'An error occurred: {str(e)}', 'error')
        finally:
            if conn:
                conn.close()

    return render_template('signup.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        password = request.form['password']

        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            user = cursor.execute('SELECT * FROM Users WHERE phone_number = ?', (phone_number,)).fetchone()

            if user:
                print(f"User found: {dict(user)}")
                stored_password = user['password'].strip()  # Remove leading/trailing whitespace
                if stored_password == password:
                    print(f"User logged in successfully: {phone_number}")
                    session['user_id'] = user['user_id']
                    flash('Logged in successfully', 'success')
                    return redirect(url_for('main.dashboard'))
                else:
                    print(f"Invalid password for user: {phone_number}")
                    flash('Invalid phone number or password', 'error')
            else:
                print(f"No user found with phone number: {phone_number}")
                flash('Invalid phone number or password', 'error')
        except sqlite3.Error as e:
            print(f"An error occurred during login: {e}")
            flash('An error occurred. Please try again later.', 'error')
        finally:
            conn.close()

    return render_template('login.html')


@main.route('/dashboard')
def dashboard():
    # Add authentication check here
    return render_template('dashboard.html')


@main.route('/items', methods=['GET','POST'])
def items():
    # Add authentication check here
    return render_template('items.html')

@main.route('/add_policy', methods=['POST'])
def add_policy():
    # Extract data from the form
    job_name = request.form.get('job_name')
    company = request.form.get('company')
    employer_number = request.form.get('employer_number')
    phone_number = request.form.get('phone_number')
    industry = request.form.get('industry')
    current_income = request.form.get('current_income')

    # Create a dictionary with the extracted data
    new_policy = {
        'job_name': job_name,
        'company': company,
        'employer_number': employer_number,
        'phone_number': phone_number,
        'industry': industry,
        'current_income': current_income
    }

    # Here you would typically save the data to a database
    # For this example, we'll just print the data and return it as JSON
    print("New policy added:", new_policy)

    return jsonify({"message": "Policy added successfully", "policy": new_policy}), 201

@main.route('/claims')
def claims():
    # Add authentication check here
    return render_template('claims.html')

@main.route('/insurance-pools')
def insurance_pools():
    # Add authentication check here
    return render_template('insurancepools.html')