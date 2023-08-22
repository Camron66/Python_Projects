import tkinter as tk
import psycopg2

# Function to connect to the PostgreSQL database
def connect_to_database():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5415",
            database="studentregistration",
            user="postgres",
            password="J@den.2001"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# Function to handle the login button click
def login():
    student_id = student_id_entry.get()
    password = password_entry.get()
    # Connect to the database
    conn = connect_to_database()
    if conn is not None:
        cursor = conn.cursor()
        # Execute a SELECT query to check if the student ID and password match in the database
        query = f"SELECT * FROM students WHERE student_id = {student_id} AND pass = '{password}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            # TODO: Navigate to the home page
            login_register_frame.pack_forget()
            home_page(student_id)
        else:
            print("Invalid credentials")
        # Close the cursor and connection
        cursor.close()
        conn.close()

# Function to handle the register button click
def register():
    # Connect to the database
    conn = connect_to_database()
    if conn is not None:
        cursor = conn.cursor()
        # Hide the login/register frame
        login_register_frame.pack_forget()
        # Show the registration frame
        # Create and configure the registration page
        registration_frame = tk.Frame(window)
        # Add registration page elements (labels, entry fields, buttons, etc.)
        student_id_label_reg = tk.Label(registration_frame, text="Student ID:")
        student_id_label_reg.pack()
        student_id_entry_reg = tk.Entry(registration_frame)
        student_id_entry_reg.pack()

        first_name_label = tk.Label(registration_frame, text="First Name:")
        first_name_label.pack()
        first_name_entry = tk.Entry(registration_frame)
        first_name_entry.pack()

        last_name_label = tk.Label(registration_frame, text="Last Name:")
        last_name_label.pack()
        last_name_entry = tk.Entry(registration_frame)
        last_name_entry.pack()

        address_label = tk.Label(registration_frame, text="Address:")
        address_label.pack()
        address_entry = tk.Entry(registration_frame)
        address_entry.pack()

        phone_number_label = tk.Label(registration_frame, text="Phone Number:")
        phone_number_label.pack()
        phone_number_entry = tk.Entry(registration_frame)
        phone_number_entry.pack()

        email_label = tk.Label(registration_frame, text="Email:")
        email_label.pack()
        email_entry = tk.Entry(registration_frame)
        email_entry.pack()

        dob_label = tk.Label(registration_frame, text="Date of Birth:")
        dob_label.pack()
        dob_entry = tk.Entry(registration_frame)
        dob_entry.pack()

        password_label_reg = tk.Label(registration_frame, text="Password:")
        password_label_reg.pack()
        password_entry_reg = tk.Entry(registration_frame, show="*")
        password_entry_reg.pack()

        register_button_reg = tk.Button(registration_frame, text="Register",
                                        command=lambda: submit_registration(student_id_entry_reg.get(),
                                                                            first_name_entry.get(),
                                                                            last_name_entry.get(),
                                                                            address_entry.get(),
                                                                            phone_number_entry.get(),
                                                                            email_entry.get(),
                                                                            dob_entry.get(),
                                                                            password_entry_reg.get(),
                                                                            registration_frame))
        register_button_reg.pack()
        registration_frame.pack()
        back_button = tk.Button(registration_frame, text="Back", command=lambda: go_back_login(registration_frame))
        back_button.pack()
        # Close the cursor and connection
        cursor.close()
        conn.close()
def go_back_login(previous_frame):
    # Hide the registration frame
    previous_frame.pack_forget()
    # Show the login/register frame
    login_register_frame.pack()
# Function to handle the submit registration button click
def submit_registration(student_id, first_name, last_name, address, phone_number, email, date_of_birth, password,registration_frame):
    # Get the student information from the entry fields
    """
    student_id = student_id_entry_reg.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    address = address_entry.get()
    phone_number = phone_number_entry.get()
    email = email_entry.get()
    date_of_birth = dob_entry.get()
    password = password_entry_reg.get()
    """
    # Connect to the database
    conn = connect_to_database()
    if conn is not None:
        cursor = conn.cursor()
        # Execute an INSERT query to add the new student to the database
        query = f"INSERT INTO students (student_id, first_name, last_name, address, phone_number, email, date_of_birth, pass) " \
                f"VALUES ({student_id}, '{first_name}', '{last_name}', '{address}', '{phone_number}', '{email}', '{date_of_birth}', '{password}')"
        cursor.execute(query)
        # Commit the changes to the database
        conn.commit()
        # Close the cursor and connection
        cursor.close()
        conn.close()
        print("Registration successful")
        # Hide the registration frame
        registration_frame.pack_forget()
        # Show the login/register frame
        login_register_frame.pack()

# Function to create and configure the home page
def home_page(student_id):
    home_frame = tk.Frame(window)

    # Query the database for the student's schedule
    conn = connect_to_database()
    if conn is not None:
        cursor = conn.cursor()
        query = f"SELECT c.course_ID, c.course_name, c.instructor_name, c.start_time, c.end_time " \
                f"FROM courses c " \
                f"JOIN enrollments e ON c.course_id = e.course_id " \
                f"WHERE e.student_id = {student_id}"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if result:
            for course in result:
                course_label = tk.Label(home_frame, text=f"Course ID: {course[0]}\n"
                                                         f"Course Name: {course[1]}\n"
                                                         f"Instructor: {course[2]}\n"
                                                         f"Start Time: {course[3]}\n"
                                                         f"End Time: {course[4]}\n")
                course_label.pack()
                delete_button = tk.Button(home_frame, text="Delete",
                                          command=lambda course_id=course[0]: delete_course(course_id, student_id,home_frame))
                delete_button.pack()
        else:
            no_courses_label = tk.Label(home_frame, text="You currently have no courses, please add a course.")
            no_courses_label.pack()

    # Add Course button
    add_course_button = tk.Button(home_frame, text="Add Course", command=lambda: add_course(home_frame, student_id))
    add_course_button.pack()

    # Update Information button
    update_info_button = tk.Button(home_frame, text="View Personal Information",
                                   command=lambda: update_information(student_id,home_frame))
    update_info_button.pack()

    # Log out button
    logout_button = tk.Button(home_frame, text="Log Out", command=lambda: logout(home_frame))
    logout_button.pack()

    home_frame.pack()


def delete_course(course_id, student_id,previous_frame):
    previous_frame.pack_forget()
    # Connect to the database
    conn = connect_to_database()
    if conn is not None:
        cursor = conn.cursor()
        # Execute a DELETE query to remove the course from the student's schedule
        query = f"DELETE FROM enrollments WHERE student_id = {student_id} AND course_id = {course_id}"
        cursor.execute(query)
        # Commit the changes to the database
        conn.commit()
        # Close the cursor and connection
        cursor.close()
        conn.close()
        print("Course deleted from schedule")
        # Refresh the home page
        home_page(student_id)
# Function to handle the add course button click
def add_course(previous_frame, student_id):
    previous_frame.pack_forget()

    add_course_frame = tk.Frame(window)

    # Query the database for available courses that the student doesn't already have
    conn = connect_to_database()
    if conn is not None:
        cursor = conn.cursor()
        query = f"SELECT c.course_id, c.course_name, c.instructor_name, c.start_time, c.end_time " \
                f"FROM courses c " \
                f"WHERE c.course_id NOT IN " \
                f"(SELECT e.course_id FROM enrollments e WHERE e.student_id = {student_id})"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if result:
            for course in result:
                course_info = f"Course ID: {course[0]}\n" \
                              f"Course Name: {course[1]}\n" \
                              f"Instructor: {course[2]}\n" \
                              f"Start Time: {course[3]}\n" \
                              f"End Time: {course[4]}"
                course_label = tk.Label(add_course_frame, text=course_info)
                course_label.pack()

                # Add Course button
                add_button = tk.Button(add_course_frame, text="Add", command=lambda course_id=course[0]: add_course_to_schedule(student_id, course_id, add_course_frame))
                add_button.pack()

        else:
            no_courses_label = tk.Label(add_course_frame, text="No available courses to add.")
            no_courses_label.pack()

    # Back button
    back_button = tk.Button(add_course_frame, text="Back", command=lambda: go_back(add_course_frame, student_id))
    back_button.pack()

    add_course_frame.pack()

# Function to handle the add course to schedule functionality
def add_course_to_schedule(student_id, course_id, previous_frame):
    # Connect to the database
    conn = connect_to_database()
    if conn is not None:
        cursor = conn.cursor()
        # Generate a new enrollment_id
        cursor.execute("SELECT MAX(enrollment_id) FROM enrollments")
        result = cursor.fetchone()
        enrollment_id = result[0] + 1 if result[0] else 1

        # Execute an INSERT query to add the course to the student's schedule with the generated enrollment_id
        query = f"INSERT INTO enrollments (enrollment_id, student_id, course_id) " \
                f"VALUES ({enrollment_id}, {student_id}, {course_id})"
        cursor.execute(query)
        # Commit the changes to the database
        conn.commit()
        # Close the cursor and connection
        cursor.close()
        conn.close()
        print("Course added to schedule")
        # Return to the home page
        previous_frame.pack_forget()
        home_page(student_id)

# Function to handle the update information button click
def update_information(student_id,previous_frame):
    previous_frame.pack_forget()

    # Create the update information frame
    view_info_frame = tk.Frame(window)

    # Query the database to retrieve the student's information
    conn = connect_to_database()
    if conn is not None:
        cursor = conn.cursor()
        query = f"SELECT * FROM students WHERE student_id = {student_id}"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            # Display the student's information
            student_info = f"Student ID: {result[0]}\n" \
                           f"First Name: {result[1]}\n" \
                           f"Last Name: {result[2]}\n" \
                           f"Address: {result[3]}\n" \
                           f"Phone Number: {result[4]}\n" \
                           f"Email: {result[5]}\n" \
                           f"Date of Birth: {result[6]}"
            student_info_label = tk.Label(view_info_frame, text=student_info)
            student_info_label.pack()

            # Update Information button
            update_button = tk.Button(view_info_frame, text="Update", command=lambda: update_student_information(student_id, view_info_frame))
            update_button.pack()

        else:
            no_info_label = tk.Label(view_info_frame, text="No information found for the student.")
            no_info_label.pack()

    # Back button
    back_button = tk.Button(view_info_frame, text="Back", command=lambda: go_back(view_info_frame, student_id))
    back_button.pack()

    view_info_frame.pack()

# Function to handle the update student information functionality
def update_student_information(student_id, previous_frame):
    previous_frame.pack_forget()

    # Create and configure the update frame
    update_frame = tk.Frame(window)

    # Address
    address_label = tk.Label(update_frame, text="Address:")
    address_label.pack()
    address_entry = tk.Entry(update_frame)
    address_entry.pack()

    # Phone Number
    phone_number_label = tk.Label(update_frame, text="Phone Number:")
    phone_number_label.pack()
    phone_number_entry = tk.Entry(update_frame)
    phone_number_entry.pack()

    # Email
    email_label = tk.Label(update_frame, text="Email:")
    email_label.pack()
    email_entry = tk.Entry(update_frame)
    email_entry.pack()

    # Update Information button
    update_button = tk.Button(update_frame, text="Update", command=lambda: execute_update(student_id, address_entry.get(), phone_number_entry.get(), email_entry.get(), update_frame))
    update_button.pack()

    # Back button
    back_button = tk.Button(update_frame, text="Back", command=lambda: go_back(update_frame, student_id))
    back_button.pack()

    update_frame.pack()


def execute_update(student_id, address, phone_number, email, previous_frame):
    # Connect to the database
    conn = connect_to_database()
    if conn is not None:
        cursor = conn.cursor()

        # Execute an UPDATE query to update the student's information
        query = f"UPDATE students " \
                f"SET address = '{address}', " \
                f"phone_number = '{phone_number}', " \
                f"email = '{email}' " \
                f"WHERE student_id = {student_id}"
        cursor.execute(query)

        # Commit the changes to the database
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        print("Information updated")

        # Return to the home page
        previous_frame.pack_forget()
        home_page(student_id)

# Function to handle the log out functionality
def logout(previous_frame):
    previous_frame.pack_forget()
    login_register_frame.pack()

# Function to handle going back to the previous frame
def go_back(previous_frame, student_id):
    previous_frame.pack_forget()
    home_page(student_id)

# Create the main window
window = tk.Tk()

# Create and configure the login/register page
login_register_frame = tk.Frame(window)
# Add login/register page elements (labels, entry fields, buttons, etc.)
student_id_label = tk.Label(login_register_frame, text="Student ID:")
student_id_label.pack()
student_id_entry = tk.Entry(login_register_frame)
student_id_entry.pack()

password_label = tk.Label(login_register_frame, text="Password:")
password_label.pack()
password_entry = tk.Entry(login_register_frame, show="*")
password_entry.pack()

login_button = tk.Button(login_register_frame, text="Login", command=login)
login_button.pack()

register_button = tk.Button(login_register_frame, text="Register", command=register)
register_button.pack()

login_register_frame.pack()
# Run the GUI event loop
window.mainloop()
