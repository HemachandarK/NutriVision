import streamlit as st
import psycopg2

# Function to connect to PostgreSQL
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="pythonexample",
            user="postgres",
            password="Neelu@0303",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to create a new user
def create_user(username, email, password):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            conn.commit()
        except Exception as e:
            st.error(f"Error creating user: {e}")
        finally:
            cursor.close()
            conn.close()

# Function to check if a user exists
def check_user_exists(username):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            st.error(f"Error checking user existence: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None

# Function to verify user login
def verify_user(username, password):
    user = check_user_exists(username)
    if user:
        stored_password = user[3]  # Password is the fourth column in the table
        if password == stored_password:
            return True
    return False

# Streamlit app
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    def show_home():
        st.subheader("Home")
        st.write(f"Welcome to the home page, {st.session_state.username}. You are logged in.")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.experimental_rerun()

    def show_login():
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
        if st.button("Login"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.experimental_rerun()
            else:
                st.error("Incorrect username or password.")

    def show_signup():
        st.subheader("Sign Up")

        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        password_confirmation = st.text_input("Confirm Password", type='password')
        
        if st.button("Sign Up"):
            if password == password_confirmation:
                if not check_user_exists(username):
                    create_user(username, email, password)
                    st.success("You have successfully signed up!")
                    st.info("You can now log in.")
                else:
                    st.error("Username already exists. Please choose a different username.")
            else:
                st.error("Passwords do not match.")

    st.title("Streamlit Authentication with PostgreSQL")

    if st.session_state.logged_in:
        show_home()
    else:
        menu = ["Login", "Sign Up"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            show_login()
        elif choice == "Sign Up":
            show_signup()

if __name__ == "__main__":
    main()
