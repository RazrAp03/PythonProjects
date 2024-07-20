from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Ticket
from datetime import datetime
import pytz
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

# Define the IST timezone
ist = pytz.timezone('Asia/Kolkata')
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

# Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://rooter:@localhost/watchdog_prod2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Flask-Login initialization
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Function for user authentication
def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        login_user(user)
        return user

# Routes...

@app.route('/', methods=['GET', 'POST'])
def home():
    message = None  # Initialize message variable

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)

        if user:
            session['username'] = username
            if user.role == 'admin':
                session['is_admin'] = True
            login_user(user)  # Log in the user using Flask-Login
            return redirect(url_for('dashboard'))
        else:
            message = 'Invalid credentials. Please login again.'
    return render_template('login.html', message=message)

@app.route('/dashboard')
@login_required
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('home'))

    user = User.query.filter_by(username=username).first()
    if user.role == 'admin':
        tickets = Ticket.query.all()
        return render_template('admin_dashboard.html', tickets=tickets)
    else:
        student_tickets = user.created_tickets
        return render_template('student_dashboard.html', student_tickets=student_tickets)

@app.route('/ticket/<int:ticket_id>')
@login_required
def ticket_details(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    return render_template('ticket_details.html', ticket=ticket)

@app.route('/my_tickets')
@login_required
def my_tickets():
    username = session.get('username')
    if not username:
        return redirect(url_for('home'))

    user = User.query.filter_by(username=username).first()
    student_tickets = user.tickets
    return render_template('my_tickets.html', student_tickets=student_tickets)

@app.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    # Get the logged-in user or handle authentication however you have implemented it
    username = session.get('username')

    if not username:
        return redirect(url_for('home'))  # Redirect to login if not authenticated

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        asset = request.form['asset']
        estimatedTimetoComplete = request.form.get('estimatedTimetoComplete')  # Handle optional field
        # Fetch other fields as needed

        # Get the user instance for the logged-in user
        user = User.query.filter_by(username=username).first()

        if user:
            # Get the current time in IST
            current_time_ist = datetime.now(ist)

            # Create a new ticket for the logged-in user and set createdAt field to IST time
            new_ticket = Ticket(
                title=title,
                description=description,
                asset=asset,
                estimatedTimetoComplete=estimatedTimetoComplete,
                createdBy=user.id,  # Ensure to set the createdBy field properly
                createdAt=current_time_ist  # Set createdAt field to current IST timestamp
                # Add other fields from the form to match the Ticket model
            )
            db.session.add(new_ticket)
            db.session.commit()

            return redirect(url_for('dashboard'))  # Redirect back to the student dashboard after creating the ticket

    return render_template('create_ticket.html')  # Render the create ticket form for GET requests

@app.route('/edit_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    # Fetch the ticket by ID
    ticket = Ticket.query.get(ticket_id)

    if not ticket:
        # Handle case where the ticket with the provided ID does not exist
        return render_template('error.html', message='Ticket not found')

    if request.method == 'GET':
        return render_template('edit_ticket.html', ticket=ticket)

    if request.method == 'POST':
        # Get the form inputs
        new_status = request.form.get('status')
        new_remark = request.form.get('remark')
        new_estimated_time = request.form.get('estimatedTimetoComplete')

        # Update ticket fields based on the form input, only if the field is not empty


        if new_remark:
            ticket.remark = new_remark
        if new_estimated_time:
            ticket.estimatedTimetoComplete = new_estimated_time
        if new_status:
            ticket.status = new_status
            if new_status == 'Completed':
                ticket.estimatedTimetoComplete = 'Completed'

        # Update the lastUpdated timestamp
        ticket.lastUpdated = datetime.utcnow()

        # Save changes to the database
        db.session.commit()

        # Redirect to the ticket details page after editing
        return redirect(url_for('ticket_details', ticket_id=ticket_id))

    # Render the ticket edit form for GET requests
    return render_template('edit_ticket.html', ticket=ticket)
from sqlalchemy.orm import joinedload


from sqlalchemy.orm import joinedload
from flask import session, redirect, url_for

# ...
@app.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    # Get the logged-in user or handle authentication however you have implemented it
    username = session.get('username')

    if not username:
        return redirect(url_for('home'))  # Redirect to login if not authenticated

    # Get the ticket by ID and ensure it belongs to the logged-in user
    ticket = (
        Ticket.query
        .options(joinedload(Ticket.created_user))
        .filter(
            Ticket.id == ticket_id,
            Ticket.created_user.has(User.username == username)
        )
        .first()
    )

    if ticket:
        # Delete the ticket
        db.session.delete(ticket)
        db.session.commit()

    return redirect(url_for('dashboard'))  # Redirect back to the student dashboard


@app.route('/update_status/<int:ticket_id>', methods=['POST', 'GET'])
@login_required
def update_status(ticket_id):
    # Check if the logged-in user is an admin (you can implement your own admin check)
    # For simplicity, using a session variable for demonstration (you might use more secure methods)
    is_admin = session.get('is_admin')

    if not is_admin:
        return redirect(url_for('home'))  # Redirect to login if not an admin
    if request.method == 'GET':
        return redirect(url_for('edit_ticket', ticket_id=ticket_id))

    if request.method == 'POST':
        new_status = request.form['status']

        # Get the ticket by ID
        ticket = Ticket.query.get(ticket_id)

        if ticket:
            # Update the ticket status
            ticket.status = new_status
            db.session.commit()

    return redirect(url_for('dashboard'))  # Redirect back to the admin dashboard after updating the status

# ... (previous code)
# ... (previous code)


@app.route('/register_user', methods=['GET', 'POST'])
@login_required
def register_user():

    if request.method == 'POST':
        # Get form inputs
        user_type = 'student'
        username = request.form['username']
        password = request.form['password']
        role = 'student'
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Check if the username is unique
        if User.query.filter_by(username=username).first():
            return render_template('error.html', message='Username already exists')

        # Create a new user based on user_type
        if user_type == 'student':
            studentCId = request.form['studentCId']
            course = request.form['course']
            passingYear = request.form['passingYear']
            branch = request.form['branch']

            new_user = User(
                username=username,
                password=password,
                role=role,
                name=name,
                email=email,
                phone=phone,
                studentCId=studentCId,
                course=course,
                passingYear=passingYear,
                branch=branch
            )
        else:
            return render_template('error.html', message='Invalid user type')

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return render_template('login.html', message='Please login now')
 # Redirect back to the admin dashboard after creating the user

    return render_template('register_user.html')  # Render the create user form for GET requests


@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    # Check if the logged-in user is an admin
    is_admin = session.get('is_admin')

    if not is_admin:
        return redirect(url_for('home'))  # Redirect to login if not an admin

    if request.method == 'POST':
        # Get form inputs
        user_type = request.form['user_type']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Check if the username is unique
        if User.query.filter_by(username=username).first():
            return render_template('error.html', message='Username already exists')

        # Create a new user based on user_type
        if user_type == 'student':
            studentCId = request.form['studentCId']
            course = request.form['course']
            passingYear = request.form['passingYear']
            branch = request.form['branch']

            new_user = User(
                username=username,
                password=password,
                role=role,
                name=name,
                email=email,
                phone=phone,
                studentCId=studentCId,
                course=course,
                passingYear=passingYear,
                branch=branch
            )
        elif user_type == 'admin':
            new_user = User(
                username=username,
                password=password,
                role=role,
                name=name,
                email=email,
                phone=phone
            )
        else:
            return render_template('error.html', message='Invalid user type')

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('dashboard'))  # Redirect back to the admin dashboard after creating the user

    return render_template('create_user.html')  # Render the create user form for GET requests

# ... (remaining code)
# ... (previous code)

# Route to display all registered users
@app.route('/all_users')
@login_required
def all_users():
    # Check if the logged-in user is an admin
    is_admin = session.get('is_admin')

    if not is_admin:
        return redirect(url_for('home'))  # Redirect to login if not an admin

    # Get all users from the database
    all_users = User.query.all()

    return render_template('all_users.html', all_users=all_users)

# ... (remaining code)

@app.route('/logout')
@login_required  # Import login_required decorator
def logout():
    logout_user()
    return render_template('login.html', message='Logged Out Successfully')
    # Redirect to the home page after logout
# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
