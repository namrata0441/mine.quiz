import sys
from PyQt5 import QtCore, QtGui, QtWidgets # QtGui is now used explicitly for QIcon.Normal/Off
import requests # Import requests for backend communication

# Import your UI classes
from dashboard_form import Ui_MainWindow
from register_form import RegisterUi_Form
# Import the custom widgets directly here if they are not part of dashboard_form.py's Ui_MainWindow setup
# from profile_widget import ProfileWidget # Already imported/instantiated in dashboard_form.py
# from aboutUs import AboutUsWidget # Already imported/instantiated in dashboard_form.py
# from settings import SettingsWidget # Already imported/instantiated in dashboard_form.py

# CRITICAL FIX: Import LoginUi_Form from login_form.py instead of defining it internally
from login_form import LoginUi_Form # Assuming login_form.py contains the LoginUi_Form class

# Corrected class name to follow CapWords convention
class MainApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MindZap Application")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.current_username = None # To store the username (email) of the logged-in user

        # Initialize page instances within __init__
        self.login_page = LoginUi_Form() # Use the imported LoginUi_Form
        self.register_page = RegisterUi_Form()

        # Initialize Dashboard Page (create an actual QMainWindow to host the UI)
        self.dashboard_window = QtWidgets.QMainWindow()
        # Instantiate Ui_MainWindow and set up the UI on dashboard_window
        self.dashboard_ui = Ui_MainWindow()
        self.dashboard_ui.setupUi(self.dashboard_window)

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.dashboard_window) # Add the actual QMainWindow here

        self.init_connections() # Separate method for connections for clarity
        self.show_login_page() # Start with the login page

    def init_connections(self):
        # Connect signals and slots for login/register flow
        # CRITICAL FIX: The login_successful_signal from login_form.py emits (username, password)
        # We need to adapt the slot to accept these arguments, or modify the signal in login_form.py
        # For now, let's adapt the slot to accept both, though password isn't needed here.
        self.login_page.login_successful_signal.connect(self._handle_login_attempt) # Connect to the existing handler
        self.login_page.switch_to_register_signal.connect(self.show_register_page) # Use the correct signal name

        self.register_page.registration_successful_signal.connect(self.show_login_page)
        self.register_page.switch_to_login_signal.connect(self.show_login_page)

        # Connect settings buttons from dashboard_ui to switch to settings page
        # and also pass the current user email
        self.dashboard_ui.setting_1.clicked.connect(self.show_settings_page)
        self.dashboard_ui.setting_2.clicked.connect(self.show_settings_page)

        # Connect the user_btn from the dashboard_ui to the show_profile_page method in MainApplicationWindow
        # This ensures that when the user clicks the profile icon, data is fetched.
        self.dashboard_ui.user_btn.clicked.connect(self.show_profile_page)

    def _handle_login_attempt(self, username, password):
        """
        Handles the login attempt by making a request to the backend.
        This method is connected to login_page.login_successful_signal.
        It now receives both username and password from the LoginUi_Form.
        """
        backend_url = "http://127.0.0.1:5000/login"
        login_data = {
            "username": username, # This is the email
            "password": password
        }

        print(f"Frontend Debug (MainApp - Login): Sending data to backend: {login_data}")

        response = None # Initialize response to None to prevent "might be referenced before assignment" error
        try:
            response = requests.post(backend_url, json=login_data)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            response_data = response.json()
            print(f"Frontend Debug (MainApp - Login): Received response: {response_data}")

            if response.status_code == 200: # HTTP 200 OK for successful login
                QtWidgets.QMessageBox.information(self, "Login Success", response_data.get("message", "Login successful!"))
                self.login_page.clear_fields() # Clear login fields on success
                self.current_username = response_data.get("username", username) # Store username (email)
                self.show_dashboard_page(self.current_username) # Pass username to dashboard
            else:
                QtWidgets.QMessageBox.warning(self, "Login Failed", response_data.get("message", "Invalid credentials."))

        except requests.exceptions.ConnectionError:
            QtWidgets.QMessageBox.critical(self, "Connection Error",
                                           "Could not connect to the backend server. Please ensure Flask app is running.")
        except requests.exceptions.HTTPError as e:
            error_message = f"Backend returned an error: {e.response.status_code}"
            try:
                # Ensure response is not None before trying to parse JSON
                if response:
                    error_json = response.json()
                    error_message += f" - {error_json.get('message', response.text)}"
                else:
                    error_message += f" - No response received."
            except requests.exceptions.JSONDecodeError:
                if response:
                    error_message += f" - {response.text}" # Fallback to raw text if not JSON
                else:
                    error_message += f" - No response received."
            QtWidgets.QMessageBox.critical(self, "Server Error", error_message)
            print(f"Frontend Debug (MainApp - Login): HTTP error: {error_message}")
        except requests.exceptions.JSONDecodeError as e:
            # This catches cases where the backend response is not valid JSON
            QtWidgets.QMessageBox.critical(self, "Response Error",
                                           f"Failed to parse server response as JSON. Error: {e}. Raw Response: '{response.text if response else 'No response'}'")
            print(f"Frontend Debug (MainApp - Login): JSON decode error: {e}. Raw Response: '{response.text if response else 'No response'}'")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred during login: {e}")
            print(f"Frontend Debug (MainApp - Login): Unexpected error: {e}")

    def _fetch_profile_data(self, username):
        """Fetches user profile data from the backend."""
        if not username:
            print("Error: No username available to fetch profile.")
            return None

        backend_url = f"http://127.0.0.1:5000/profile/{username}"
        response = None # Initialize response to None to prevent "might be referenced before assignment" error
        try:
            response = requests.get(backend_url)
            response.raise_for_status()
            profile_data = response.json()
            print(f"Frontend Debug (MainApp - Profile Fetch): Fetched profile: {profile_data}")
            return profile_data
        except requests.exceptions.ConnectionError:
            QtWidgets.QMessageBox.critical(self, "Connection Error", "Could not connect to backend to fetch profile.")
        except requests.exceptions.HTTPError as e:
            error_message = f"Backend returned an error: {e.response.status_code}"
            try:
                # Ensure response is not None before trying to parse JSON
                if response:
                    error_json = response.json()
                    error_message += f" - {error_json.get('message', response.text)}"
                else:
                    error_message += f" - No response received."
            except requests.exceptions.JSONDecodeError:
                if response:
                    error_message += f" - {response.text}" # Fallback to raw text if not JSON
                else:
                    error_message += f" - No response received."
            QtWidgets.QMessageBox.critical(self, "Server Error", error_message)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred fetching profile: {e}")
        return None

    def show_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)
        self.setWindowTitle("MindZap - Login") # Set window title dynamically
        self.current_username = None # Clear username on logout/return to login
        print("Switched to Login Page")

    def show_register_page(self):
        self.stacked_widget.setCurrentWidget(self.register_page)
        self.setWindowTitle("MindZap - Register") # Set window title dynamically
        print("Switched to Register Page")

    def show_dashboard_page(self, username):
        # Call the set_username_display method on the dashboard_ui instance
        self.dashboard_ui.set_username_display(username)
        self.stacked_widget.setCurrentWidget(self.dashboard_window)
        self.setWindowTitle(f"MindZap - Dashboard ({username})") # Set window title dynamically
        print(f"Switched to Dashboard Page for user: {username}")

    def show_settings_page(self): # No 'checked' argument needed with .clicked signal
        """
        This method is called when a settings button is clicked.
        It passes the current user's email to the SettingsWidget before displaying it.
        """
        if self.current_username:
            # CRITICAL: Ensure the settings widget receives the current user email
            self.dashboard_ui.page_5.set_current_user_email(self.current_username)
            print(f"Debug MainApp: Passed email '{self.current_username}' to SettingsWidget.") # Added debug print
            self.dashboard_ui.stackedWidget.setCurrentIndex(5) # Index 5 is the Settings Page (self.page_5)
            self.setWindowTitle(f"MindZap - Settings ({self.current_username})")
            print(f"Switched to Settings Page for user: {self.current_username}")
        else:
            QtWidgets.QMessageBox.warning(self, "Settings Error", "No user logged in to access settings.")
            self.show_login_page() # Redirect to login if no user is logged in

    def show_profile_page(self):
        """
        This method is called when the user clicks the profile button on the dashboard.
        It fetches the profile data and loads it into the ProfileWidget.
        """
        if self.current_username:
            profile_data = self._fetch_profile_data(self.current_username)
            if profile_data:
                # Load data into the ProfileWidget instance (self.dashboard_ui.page_7)
                self.dashboard_ui.page_7.load_profile_data(profile_data)
                # Tell the dashboard's stackedWidget to show the profile page
                self.dashboard_ui.stackedWidget.setCurrentIndex(1) # Index 1 is the Profile Page (self.page_7)
                self.setWindowTitle(f"MindZap - Profile ({self.current_username})")
                print(f"Switched to Profile Page for user: {self.current_username}")
            else:
                QtWidgets.QMessageBox.warning(self, "Profile Error", "Could not load profile data.")
        else:
            QtWidgets.QMessageBox.warning(self, "Profile Error", "No user logged in to view profile.")
            self.show_login_page() # Redirect to login if no user is logged in


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApplicationWindow()
    main_app.show()
    sys.exit(app.exec_())
