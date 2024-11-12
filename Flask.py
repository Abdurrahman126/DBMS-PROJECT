from flask import Flask, render_template, redirect, request, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from pymysql.cursors import DictCursor
app = Flask(__name__)
app.config['SECRET_KEY'] = 'k224150'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Function to get a connection using PyMySQL
def get_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='newuser',
            password='@Akhan25',
            database='Society_Management_System'
        )
        print("Connection successful!")
        return connection
    except pymysql.MySQLError as err:
        print(f"Error connecting to the database: {err}")
        return None

@app.route('/')
def home():
    return render_template('login_page.html')

@app.route('/login_page')
def login_page():
    return render_template('login_page.html')

@app.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role_as = 'admin'
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO users (email, pwd,role_as, is_admin) VALUES (%s, %s,%s, %s)", 
                                   (email, hashed_password,role_as, True))
                connection.commit()
                flash("Admin created successfully!", "success")
            except pymysql.MySQLError as err:
                print(f"Error: {err}")
                return "Error while inserting data into database."
            finally:
                connection.close()
            return redirect('/login_page')
        else:
            return "Database connection failed."
    
    return render_template('create_admin.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role_as = 'user'
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO users (email, pwd,role_as, is_admin) VALUES (%s, %s,%s, %s)", 
                                   (email, hashed_password,role_as, False))
                connection.commit()
                flash("User created successfully!", "success")
            except pymysql.MySQLError as err:
                print(f"Error: {err}")
                return "Error while inserting data into database."
            finally:
                connection.close()
            return redirect('/login_page')
        else:
            return "Database connection failed."
    
    return render_template('create_user.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('pwd')

        connection = get_connection()
        if connection:
            try:
                with connection.cursor(DictCursor) as cursor:
                    cursor.execute("SELECT * FROM users WHERE email = %s AND is_admin = TRUE", (email,))
                    admin = cursor.fetchone()

                if admin and check_password_hash(admin['pwd'], pwd):
                    session['user_id'] = admin['user_id']
                    session['is_admin'] = True
                    flash("Login successful! Welcome Admin!", "success")
                    return redirect('/admin_dashboard')
                else:
                    flash("Incorrect email or password", "error")
            finally:
                connection.close()
            return redirect('/admin_login')
        else:
            return "Database connection failed."

    return render_template('admin_login.html')

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('pwd')

        connection = get_connection()
        if connection:
            try:
                with connection.cursor(DictCursor) as cursor:
                    cursor.execute("SELECT * FROM users WHERE email = %s AND is_admin = FALSE", (email,))
                    user = cursor.fetchone()

                if user and check_password_hash(user['pwd'], pwd):
                    session['user_id'] = user['user_id']
                    session['is_admin'] = False
                    flash("Login successful! Welcome back!", "success")
                    return redirect('/user_dashboard')
                else:
                    flash("Incorrect email or password", "error")
            finally:
                connection.close()
            return redirect('/user_login')
        else:
            return "Database connection failed."

    return render_template('user_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('is_admin'):
      
      return  render_template('admin_dashboard.html')

@app.route('/user_dashboard')
def user_dashboard():
    if not session.get('is_admin'):
       
      return  render_template('user_dashboard.html')


@app.route('/add_announcement', methods=['GET','POST'])
def add_announcement():
    title = request.form.get('announcement_title')
    content = request.form.get('content')

    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO announcements (announcement_title, content) VALUES (%s, %s)", 
                               (title, content))
            connection.commit()
            flash("Announcement posted successfully!", "success")
        except pymysql.MySQLError as err:
            print(f"Error: {err}")
            flash("Error while posting announcement.", "error")
        finally:
            connection.close()
    else:
        flash("Database connection failed.", "error")
        return redirect('/admin_dashboard')
    return render_template('add_announcement.html')


@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    applicants = []  # Initialize an empty list for applicants
    connection = get_connection()
    
    if connection:
        try:
            with connection.cursor(DictCursor) as cursor:
                # Fetch the list of applicants from the inductions table
                cursor.execute("SELECT applicant_name FROM inductions")  # Adjust the query as needed
                applicants = cursor.fetchall()
        finally:
            connection.close()

    if request.method == 'POST':
       
        appointed_as = request.form.get('appointed_as')
        applicant_name = request.form.get('applicant_name')
        # Ensure user_id is retrieved from the session

        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Insert the new member using the applicant_id
                    cursor.execute("INSERT INTO members (member_name, appointed_as) VALUES (%s, %s)", 
                                   (applicant_name, appointed_as)) 
                    connection.commit()  # Commit the transaction
                    flash("Member appointed successfully!", "success")
                    return redirect('/admin_dashboard')  # Redirect after successful appointment
            except pymysql.MySQLError as err:
                print(f"Error: {err}")  # Print the error for debugging
                flash("Error while appointing member.", "error")
            finally:
                connection.close()
        else:
            flash("Database connection failed.", "error")
            return redirect('/admin_dashboard')

    return render_template('add_member.html', applicants=applicants)  # Pass the applicants to the templateo the template
@app.route('/add_event', methods=['GET','POST'])
def add_event():
    event_title = request.form.get('event_title')
    about_event = request.form.get('about_event')
    event_date = request.form.get('event_date')
    venue = request.form.get('venue')

    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO society_events (event_title, about_event, event_date, venue) VALUES (%s, %s, %s, %s)", 
                               (event_title, about_event, event_date, venue))
            connection.commit()
            flash("Event created successfully!", "success")
        except pymysql.MySQLError as err:
            print(f"Error: {err}")
            flash("Error while creating event.", "error")
        finally:
            connection.close()
    else:
        flash("Database connection failed.", "error")
        return redirect('/admin_dashboard')
    return render_template('add_event.html')
    

@app.route('/manage_account', methods=['GET','POST'])
def manage_account():
    account_balance = request.form.get('account_balance')
    budget = request.form.get('budget')

    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute( "INSERT INTO accounts(account_balance,budget) VALUES (%s, %s)",
                               (account_balance, budget))
            connection.commit()
            flash("Account managed successfully!", "success")
        except pymysql.MySQLError as err:
            print(f"Error: {err}")
            flash("Error while managing account.", "error")
        finally:
            connection.close()
    else:
        flash("Database connection failed.", "error")
        return redirect('/admin_dashboard')
    return render_template('manage_account.html')
    

@app.route('/mark_attendance', methods=['GET','POST'])
def mark_attendance():
    user_id = request.form.get('user_id')
    event_id = request.form.get('event_id')
    was_present = request.form.get('was_present')

    print(f"User ID: {user_id}, Event ID: {event_id}, Was Present: {was_present}")  # Debugging

    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO attendance (user_id, event_id, was_present) VALUES (%s, %s, %s)", 
                               (user_id, event_id, was_present))
            connection.commit()
            flash("Attendance marked successfully!", "success")
        except pymysql.MySQLError as err:
            print(f"Error: {err}")  # Print the error
            flash("Error while marking attendance.", "error")
        finally:
            connection.close()
    else:
        flash("Database connection failed.", "error")
        return redirect('/admin_dashboard')
    return render_template('mark_attendence.html')

@app.route('/add_achievement', methods=['GET','POST'])
def add_achievement():
    user_id = request.form.get('user_id')
    achievement_title = request.form.get('achievement_title')
    description = request.form.get('description')
    date_of_achievement = request.form.get('date_of_achievement')

    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO achievements (user_id, achievement_title, description, date_of_achievement) VALUES (%s, %s, %s, %s)", 
                               (user_id, achievement_title, description, date_of_achievement))
            connection.commit()
            flash("Achievement added successfully!", "success")
        except pymysql.MySQLError as err:
            print(f"Error: {err}")
            flash("Error while adding achievement.", "error")
        finally:
            connection.close()
    else:
        flash("Database connection failed.", "error")
        return redirect('/admin_dashboard')
    return render_template('add_achievements.html')

@app.route('/add_certification', methods=['GET','POST'])
def add_certification():
        certification_for = request.form.get('certification_for')
        participant_id = request.form.get('participant_id')
        person_name = request.form.get('person_name')

        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO certifications (person_name,participant_id,certification_for) VALUES (%s,%s, %s)", 
                                   (person_name, participant_id,certification_for))
                connection.commit()
                flash("Certification added successfully!", "success")
            except pymysql.MySQLError as err:
                 print(f"Error: {err}")
                 flash("Error while adding certification.", "error")
            finally:
                 connection.close()
        else:
                 flash("Database connection failed.", "error")
                 return redirect('/admin_dashboard')
    
            
        return render_template('add_certification.html')
@app.route('/track_attendance', methods=['GET', 'POST'])
def track_attendance():
    attendance_percentage = None  # Initialize attendance percentage
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        connection = get_connection()
        
        if connection:
            try:
                with connection.cursor(DictCursor) as cursor:
                    # Total events for the user
                    cursor.execute("SELECT COUNT(*) as total_events FROM attendance WHERE user_id = %s", (user_id,))
                    total_events = cursor.fetchone()['total_events']

                    # Attended events for the user
                    cursor.execute("SELECT COUNT(*) as attended_events FROM attendance WHERE user_id = %s AND was_present = TRUE", (user_id,))
                    attended_events = cursor.fetchone()['attended_events']

                # Calculate attendance percentage
                if total_events > 0:
                    attendance_percentage = (attended_events / total_events) * 100
                else:
                    attendance_percentage = 0

                flash(f"Attendance Percentage: {attendance_percentage:.2f}%", "info")

            except pymysql.MySQLError as err:
                print(f"Error: {err}")
                flash("Error while calculating attendance.", "error")
            finally:
                connection.close()
        else:
            flash("Database connection failed.", "error")

    return render_template('track_attendence.html', attendance_percentage=attendance_percentage)

@app.route('/register_participant', methods=['GET', 'POST'])
def register_participant():
    if request.method == 'POST':
        participant_id = request.form.get('participant_id')
        user_id = request.form.get('user_id')
        competition_id = request.form.get('competition_id')
        participant_name = request.form.get('participant_name')

        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO participants (participant_id, user_id, competition_id, participant_name) VALUES (%s, %s, %s, %s)", 
                                   (participant_id, user_id, competition_id, participant_name))
                connection.commit()
                flash("Participant registered successfully!", "success")
            except pymysql.MySQLError as err:
                print(f"Error: {err}")
                flash("Error while registering participant.", "error")
            finally:
                connection.close()
            return redirect('/user_dashboard')
        else:
            flash("Database connection failed.", "error")
            return redirect('/user_dashboard')

    return render_template('register_participant.html')

@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        feedback_content = request.form.get('feedback_content')

        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO feedback (user_id, feedback_content) VALUES (%s, %s)", 
                                   (user_id, feedback_content))
                connection.commit()
                flash("Feedback submitted successfully!", "success")
            except pymysql.MySQLError as err:
                print(f"Error: {err}")
                flash("Error while submitting feedback.", "error")
            finally:
                connection.close()
        else:
            flash("Database connection failed.", "error")
            return redirect('/user_dashboard')
    
    return render_template('submit_feedback.html')

@app.route('/read_announcements', methods=['GET'])
def read_announcements():
    connection = get_connection()
    announcements = []
    if connection:
        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute("SELECT * FROM announcements")
                announcements = cursor.fetchall()
        finally:
            connection.close()
    return render_template('read_announcements.html', announcements=announcements)

@app.route('/register_induction', methods=['GET', 'POST'])
def register_induction():
    if request.method == 'POST':
        applying_for = request.form.get('applying_for')

        applying_name = request.form.get('applicant_name')

        user_id = session.get('user_id')
        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO inductions (applying_for,applicant_name,applicant_id) VALUES (%s, %s,%s)", 
                                   ( applying_for,applying_name,user_id))
                connection.commit()
                flash("Successfully registered for induction!", "success")
                return redirect('/user_dashboard')  # Ensure you return a response here
            except pymysql.MySQLError as err:
                print(f"Error: {err}")
                flash("Error while registering for induction.", "error")
            finally:
                connection.close()
        else:
            flash("Database connection failed.", "error")
            return redirect('/user_dashboard')  # Ensure you return a response here

    return render_template('register_induction.html')  # Ensure you return a response for GET requests

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True, port=5003)
