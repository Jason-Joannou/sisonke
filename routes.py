from flask import Blueprint, render_template, request, redirect, url_for, flash,session
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

@main.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # Process the form data
        item_name = request.form.get('item_name')
        item_type = request.form.get('item_type')
        insured_amount = request.form.get('insured_amount')
        purchase_date = request.form.get('purchase_date')
        description = request.form.get('description')

        # Handle file uploads
        item_photo = request.files.get('item_photo')
        receipt_photo = request.files.get('receipt_photo')

        # Save the data to your database or perform any other necessary operations

        # Redirect to a success page or back to the items list
        return redirect(url_for('items'))

    # If it's a GET request, just render the form
    return render_template('items.html')

@main.route('/claims')
def claims():
    # Add authentication check here
    return render_template('claims.html')

@main.route('/insurance-pools')
def insurance_pools():
    # Add authentication check here
    return render_template('insurancepools.html')