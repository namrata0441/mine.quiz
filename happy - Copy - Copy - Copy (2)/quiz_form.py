# quiz_form.py
from PyQt5 import QtWidgets, QtCore, QtGui
from quiz_ui import Ui_MainWindow  # Make sure quiz_ui.py is in the same directory or accessible via PYTHONPATH
import random


class QuizUiForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Ensure a minimum size for the widget that will hold the UI
        self.setMinimumSize(620, 650)

        self.ui = Ui_MainWindow()
        # Create a temporary QMainWindow to set up the UI, then move its central widget
        # This is a common pattern when using a .ui file designed for a QMainWindow
        # within a QWidget or a different main application structure.
        temp_quiz_window = QtWidgets.QMainWindow()
        try:
            self.ui.setupUi(temp_quiz_window)
            quiz_content_widget = temp_quiz_window.centralWidget()

            if quiz_content_widget:
                # Set the parent of the UI content widget to this QuizUiForm instance
                quiz_content_widget.setParent(self)
                # Create a layout for this QuizUiForm and add the UI content
                layout = QtWidgets.QVBoxLayout(self)
                layout.addWidget(quiz_content_widget)
                layout.setContentsMargins(0, 0, 0, 0)  # Remove extra margins
                self.setLayout(layout)
                print("Quiz UI loaded successfully into QuizUiForm.")
            else:
                layout = QtWidgets.QVBoxLayout(self)
                layout.addWidget(QtWidgets.QLabel("Error: Quiz content widget not found in UI setup."))
                self.setLayout(layout)
                print("ERROR: quiz_content_widget is None after setupUi.")
        except Exception as e:
            # Display an error message if UI loading fails
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(QtWidgets.QLabel(f"Error loading quiz UI: {e}\nCheck console for details."))
            self.setLayout(layout)
            print(f"CRITICAL ERROR: Failed to load quiz UI. Exception: {e}")
            # It might be helpful to reraise the exception for full traceback in development
            # raise
            return

        # Clean up the temporary QMainWindow immediately
        temp_quiz_window.deleteLater()

        # --- Quiz Data and State Initialization ---
        self.quiz_data = {
            "comp202": [  # Data Structures and Algorithms Questions
                {
                    "question": "Which of the following data structures is typically used for implementing a Breadth-First Search (BFS) algorithm?",
                    "options": [
                        "a. Stack",
                        "b. Queue",
                        "c. Linked List",
                        "d. Hash Table"
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "What is the worst-case time complexity of inserting an element into a sorted singly linked list?",
                    "options": [
                        "a. O(1)",
                        "b. O(log n)",
                        "c. O(n)",
                        "d. O(n log n)"
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "Which sorting algorithm has the best worst-case time complexity?",
                    "options": [
                        "a. Quick Sort",
                        "b. Bubble Sort",
                        "c. Merge Sort",
                        "d. Insertion Sort"
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "In a binary search tree, what is the maximum number of children a node can have?",
                    "options": [
                        "a. 0",
                        "b. 1",
                        "c. 2",
                        "d. Any number"
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "Which of the following is NOT a type of graph traversal?",
                    "options": [
                        "a. Depth-First Search (DFS)",
                        "b. Breadth-First Search (BFS)",
                        "c. Random Walk",
                        "d. Linear Search"
                    ],
                    "correct_option": "d"
                },
                {
                    "question": "What is the primary advantage of using a hash table?",
                    "options": [
                        "a. Guaranteed O(1) worst-case lookup time",
                        "b. Efficient memory usage for all data sizes",
                        "c. Fast average-case lookup, insertion, and deletion",
                        "d. Maintains insertion order of elements"
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "Which data structure uses LIFO (Last In, First Out) principle?",
                    "options": [
                        "a. Queue",
                        "b. Stack",
                        "c. Array",
                        "d. Linked List"
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "The process of visiting each node in a data structure exactly once is called:",
                    "options": [
                        "a. Searching",
                        "b. Sorting",
                        "c. Traversal",
                        "d. Insertion"
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "What is the time complexity of searching an element in a balanced Binary Search Tree (BST)?",
                    "options": [
                        "a. O(1)",
                        "b. O(log n)",
                        "c. O(n)",
                        "d. O(n log n)"
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "Which algorithm is used to find the shortest path in a weighted graph?",
                    "options": [
                        "a. Kruskal's Algorithm",
                        "b. Prim's Algorithm",
                        "c. Dijkstra's Algorithm",
                        "d. Bellman-Ford Algorithm"
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "Which of the following is a disadvantage of arrays?",
                    "options": [
                        "a. Elements can be accessed randomly.",
                        "b. Data elements are stored in contiguous memory locations.",
                        "c. Fixed size.",
                        "d. Easy to implement."
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "What is the time complexity of deleting an element from the beginning of a singly linked list?",
                    "options": [
                        "a. O(1)",
                        "b. O(log n)",
                        "c. O(n)",
                        "d. O(n log n)"
                    ],
                    "correct_option": "a"
                },
                {
                    "question": "What is the function of a hash function in a hash table?",
                    "options": [
                        "a. To sort the data elements.",
                        "b. To map keys to indices in an array.",
                        "c. To reverse the order of elements.",
                        "d. To check for duplicates."
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "Which data structure is suitable for implementing 'undo' operations in a text editor?",
                    "options": [
                        "a. Queue",
                        "b. Stack",
                        "c. Tree",
                        "d. Graph"
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "What is the average case time complexity of Quick Sort?",
                    "options": [
                        "a. O(n)",
                        "b. O(n log n)",
                        "c. O(n^2)",
                        "d. O(log n)"
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "Which data structure is best suited for representing hierarchical relationships?",
                    "options": [
                        "a. Array",
                        "b. Linked List",
                        "c. Tree",
                        "d. Queue"
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "In a max-heap, what is the property of the root node?",
                    "options": [
                        "a. It is the smallest element.",
                        "b. It is the largest element.",
                        "c. It is always a leaf node.",
                        "d. It has no children."
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "Which of the following is used to resolve collisions in a hash table?",
                    "options": [
                        "a. Hashing functions",
                        "b. Sorting algorithms",
                        "c. Collision resolution techniques (e.g., chaining, open addressing)",
                        "d. Binary search"
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "What is the purpose of Big O notation?",
                    "options": [
                        "a. To measure the exact execution time of an algorithm.",
                        "b. To describe the memory usage of a program.",
                        "c. To characterize the performance or complexity of an algorithm as the input size grows.",
                        "d. To determine the programming language efficiency."
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "Which data structure allows access to elements only from one end (insertion and deletion)?",
                    "options": [
                        "a. Queue (from both ends)",
                        "b. Stack (from one end)",
                        "c. Linked List (from anywhere)",
                        "d. Hash Table (direct access)"
                    ],
                    "correct_option": "b"
                }
            ],
            "mcsc202_numerical": [  # Numerical Methods / MCSC202 related Questions
                {
                    "question": "If X = 0.51 is correct to 2 decimal places, then its relative accuracy is:",
                    "options": [
                        "a. 0.0096",
                        "b. 0.0097",
                        "c. 0.0098",
                        "d. 0.0099"
                    ],
                    "correct_option": "d"
                },
                {
                    "question": "The iteration method for the equation x = φ(x) converges at x = xt if |φ'(xt)| < k such that:",
                    "options": [
                        "a. k < 0",
                        "b. k < 1",
                        "c. k > 1",
                        "d. k = 1"
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "The relation between the backward difference operator (∇) and shift operator (E) is:",
                    "options": [
                        "a. ∇ = E - 1",
                        "b. ∇ = 1 + E",
                        "c. ∇ = E^-1 - 1",
                        "d. ∇ = 1 - E^-1"
                    ],
                    "correct_option": "d"
                },
                {
                    "question": "Third order divided difference for (n+1) data points (x0,y0), (x1,y1), (x2,y2), ..., (xn,yn) is denoted by:",
                    "options": [
                        "a. [x0,x1,x2]",
                        "b. [x0,x1,x2,x3]",
                        "c. [x,x0,x1]",
                        "d. [x,x0,x1,x2]"
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "The norm of a matrix A = ||a_ij|| is defined by the formula ||A||_∞ = max_i Σ_j |a_ij|. For a given matrix A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]], ||A||_∞ is:",
                    "options": [
                        "a. 18",
                        "b. 16.88",
                        "c. 24",
                        "d. 20"
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "The forward difference approximation for y'(x) is represented by:",
                    "options": [
                        "a. (y(x+h) - y(x)) / h",
                        "b. (y(x+h) - y(x)) / (2h)",
                        "c. (y(x+h) - y(x-h)) / (2h)",
                        "d. (y(x) - y(x-h)) / h"
                    ],
                    "correct_option": "a"
                },
                {
                    "question": "The number 0.000145 has how many significant digits?",
                    "options": [
                        "a. 6",
                        "b. 5",
                        "c. 4",
                        "d. 3"
                    ],
                    "correct_option": "d"
                },
                {
                    "question": "In numerical methods, 'truncation error' refers to:",
                    "options": [
                        "a. Error due to finite precision of computer arithmetic.",
                        "b. Error due to approximating an infinite process with a finite one.",
                        "c. Error due to human mistakes in calculation.",
                        "d. Error in measuring physical quantities."
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "Which of the following methods is an open method for finding roots of an equation?",
                    "options": [
                        "a. Bisection Method",
                        "b. False Position Method",
                        "c. Secant Method",
                        "d. All of the above"
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "Newton-Raphson method is a/an _______ convergence method.",
                    "options": [
                        "a. Linear",
                        "b. Quadratic",
                        "c. Cubic",
                        "d. Sub-linear"
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "The formula for trapezoidal rule for integration over [a,b] with h = (b-a)/n is:",
                    "options": [
                        "a. h/2 * [f(a) + f(b)]",
                        "b. h/2 * [f(a) + 2Σf(xi) + f(b)]",
                        "c. h/3 * [f(a) + 4f(mid) + f(b)]",
                        "d. (b-a) * f((a+b)/2)"
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "Which interpolation method requires that the polynomial pass exactly through all given data points?",
                    "options": [
                        "a. Least Squares Regression",
                        "b. Spline Interpolation",
                        "c. Lagrange Interpolation",
                        "d. None of the above"
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "If the determinant of a matrix is zero, what does it imply about the system of linear equations Ax = b?",
                    "options": [
                        "a. A unique solution exists.",
                        "b. No solution exists.",
                        "c. Infinitely many solutions exist or no solution exists.",
                        "d. The matrix is invertible."
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "The Gauss-Seidel method is an iterative method used for:",
                    "options": [
                        "a. Finding eigenvalues of a matrix.",
                        "b. Solving systems of linear equations.",
                        "c. Numerical differentiation.",
                        "d. Numerical integration."
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "What is the order of convergence for the Bisection Method?",
                    "options": [
                        "a. 1 (linear)",
                        "b. 2 (quadratic)",
                        "c. 1.618 (golden ratio)",
                        "d. 0.5 (sub-linear)"
                    ],
                    "correct_option": "a"
                },
                {
                    "question": "Runge-Kutta methods are used for solving:",
                    "options": [
                        "a. Linear Algebraic Equations",
                        "b. Non-linear Algebraic Equations",
                        "c. Ordinary Differential Equations (ODEs)",
                        "d. Partial Differential Equations (PDEs)"
                    ],
                    "correct_option": "c"
                },
                {
                    "question": "What is 'pivoting' used for in Gaussian elimination?",
                    "options": [
                        "a. To reduce the number of steps.",
                        "b. To minimize round-off errors and avoid division by zero.",
                        "c. To increase the speed of calculation.",
                        "d. To find the inverse of the matrix."
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "Which of the following is an advantage of iterative methods over direct methods for solving linear systems?",
                    "options": [
                        "a. Always converge faster.",
                        "b. Less prone to round-off errors for large systems.",
                        "c. Guarantee a solution in a fixed number of steps.",
                        "d. Do not require an initial guess."
                    ],
                    "correct_option": "b"
                },
                {
                    "question": "If the forward difference operator is Δ, then Δf(x) is equal to:",
                    "options": [
                        "a. f(x+h) - f(x)",
                        "b. f(x) - f(x-h)",
                        "c. (f(x+h) - f(x-h)) / 2",
                        "d. (f(x) + f(x+h)) / 2"
                    ],
                    "correct_option": "a"
                },
                {
                    "question": "A matrix is said to be diagonally dominant if:",
                    "options": [
                        "a. All off-diagonal elements are zero.",
                        "b. The absolute value of each diagonal element is greater than the sum of the absolute values of the other elements in its row.",
                        "c. The sum of all elements in each row is positive.",
                        "d. All elements are positive."
                    ],
                    "correct_option": "b"
                }
            ]
        }

        self.current_quiz_questions = []
        self.current_question_index = 0
        self.correct_answers_count = 0
        self.total_questions_asked = 0
        self.selected_radio_button_id = -1  # Stores the ID of the currently selected radio button

        # --- Connect UI elements ---
        # ComboBox for Category
        if hasattr(self.ui, 'comboBox_category'):
            self.ui.comboBox_category.clear()
            for category in self.quiz_data.keys():
                self.ui.comboBox_category.addItem(category)
        else:
            print("WARNING: comboBox_category not found in UI. Please check your quiz.ui file.")

        # SpinBox for Number of Questions
        if hasattr(self.ui, 'spinBox_num_questions'):
            self.ui.spinBox_num_questions.setMinimum(1)
            # Set maximum based on the largest category data, or a reasonable hardcoded limit
            max_questions_available = max(len(v) for v in self.quiz_data.values()) if self.quiz_data else 20
            self.ui.spinBox_num_questions.setMaximum(max_questions_available)
            self.ui.spinBox_num_questions.setProperty("value", 20)  # Default to 20 if available
        else:
            print("WARNING: spinBox_num_questions not found in UI. Please check your quiz.ui file.")

        # "Get New Question" (Start Quiz) Button - Identified as 'pushButton_4' in your UI
        if hasattr(self.ui, 'pushButton_4'):
            self.ui.pushButton_4.clicked.connect(self.start_quiz)
        else:
            print("WARNING: pushButton_4 (Get New Question) not found in UI. Please check your quiz.ui file.")

        # "Try Again" (Reset Quiz) Button - Identified as 'pushButton' in your UI
        if hasattr(self.ui, 'pushButton'):
            self.ui.pushButton.clicked.connect(self.reset_quiz)
        else:
            print("WARNING: pushButton (Try Again) not found in UI. Please check your quiz.ui file.")

        # --- Submit Answer Button ---
        # Corrected name based on your quiz_ui.py: pushButton_submit_answer
        if hasattr(self.ui, 'pushButton_submit_answer'):
            self.ui.pushButton_submit_answer.clicked.connect(self.check_answer)
            self.ui.pushButton_submit_answer.setEnabled(False)  # Disable at start
        else:
            print("WARNING: pushButton_submit_answer not found in UI. Please check quiz_ui.py for the correct name.")

        # --- Next Button ---
        # Corrected name based on your quiz_ui.py: pushButton_next_question
        if hasattr(self.ui, 'pushButton_next_question'):
            self.ui.pushButton_next_question.clicked.connect(self.next_question)
            self.ui.pushButton_next_question.setEnabled(False)  # Disable at start
        else:
            print("WARNING: pushButton_next_question not found in UI. Please check quiz_ui.py for the correct name.")

        # --- Initialize Radio Button Group ---
        # It's good practice to create the QButtonGroup programmatically if it's not explicitly in the .ui
        if not hasattr(self.ui, 'buttonGroup_answers'):
            self.ui.buttonGroup_answers = QtWidgets.QButtonGroup(self)

        # Add radio buttons to the group and assign IDs
        radio_buttons = {
            1: self.ui.radioButton_opt_a,
            2: self.ui.radioButton_opt_b,
            3: self.ui.radioButton_opt_c,
            4: self.ui.radioButton_opt_d
        }
        for btn_id, btn in radio_buttons.items():
            if hasattr(self.ui, btn.objectName()):  # Check if the button exists
                self.ui.buttonGroup_answers.addButton(btn, btn_id)
            else:
                print(f"WARNING: Radio button {btn.objectName()} not found in UI.")

        self.ui.buttonGroup_answers.setExclusive(True)  # Ensure only one can be checked at a time

        # Connect the button group's clicked signal to a handler
        # Disconnect previous connections to prevent multiple signal emissions if __init__ is called multiple times
        try:
            self.ui.buttonGroup_answers.buttonClicked[int].disconnect(self.on_option_selected)
        except (TypeError, RuntimeError):  # RuntimeError if slot is not connected, TypeError if not a signal
            pass
        self.ui.buttonGroup_answers.buttonClicked[int].connect(self.on_option_selected)

        # Initial display setup
        self.display_current_question_page()  # Start on the settings page
        self.reset_quiz_state()  # Ensure initial quiz state is clean

    def reset_quiz_state(self):
        """Helper to reset internal quiz state variables."""
        self.current_quiz_questions = []
        self.current_question_index = 0
        self.correct_answers_count = 0
        self.total_questions_asked = 0
        self.selected_radio_button_id = -1

        # Clear UI elements
        self.clear_selection()
        self.ui.label_question.setText("Question Text Will Appear Here")
        self.ui.radioButton_opt_a.setText("Option A")
        self.ui.radioButton_opt_b.setText("Option B")
        self.ui.radioButton_opt_c.setText("Option C")
        self.ui.radioButton_opt_d.setText("Option D")
        self.ui.label_feedback.setText("")
        self.ui.question_count_label.setText("1/1")  # Reset display count

        # Ensure correct button states
        self.ui.radioButton_opt_a.setEnabled(True)
        self.ui.radioButton_opt_b.setEnabled(True)
        self.ui.radioButton_opt_c.setEnabled(True)
        self.ui.radioButton_opt_d.setEnabled(True)
        self.ui.pushButton_submit_answer.setEnabled(False)
        self.ui.pushButton_next_question.setEnabled(False)

    def on_option_selected(self, button_id):
        """
        Called when a radio button is clicked.
        Records the selected option and enables the 'Submit Answer' button.
        """
        self.selected_radio_button_id = button_id
        if self.ui.pushButton_submit_answer:
            self.ui.pushButton_submit_answer.setEnabled(True)
        self.ui.label_feedback.setText("")  # Clear any old feedback if user changes their mind
        print(f"Option selected: ID {button_id}")

    def display_current_question_page(self):
        """Switches the toolBox to the appropriate page (Settings or Question)."""
        if hasattr(self.ui, 'toolBox'):
            if self.current_quiz_questions:  # If questions are loaded, show question page
                self.ui.toolBox.setCurrentIndex(1)  # Assuming question page is index 1
                print("Switched to Question page.")
            else:  # Otherwise, show settings/setup page
                self.ui.toolBox.setCurrentIndex(0)  # Assuming settings page is index 0
                print("Switched to Settings page.")
        else:
            print("WARNING: toolBox not found in UI. Cannot switch pages.")

    def start_quiz(self):
        print("\n--- start_quiz method called ---")
        selected_category = self.ui.comboBox_category.currentText()
        num_questions_to_ask = self.ui.spinBox_num_questions.value()

        print(f"Selected category: {selected_category}")
        print(f"Number of questions to ask: {num_questions_to_ask}")

        if selected_category not in self.quiz_data:
            print(f"Error: Category '{selected_category}' not found in quiz_data.")
            QtWidgets.QMessageBox.warning(self, "Quiz Error",
                                          f"Category '{selected_category}' not found in quiz data. Please select a valid category.")
            self.reset_quiz_state()
            self.display_current_question_page()
            return

        available_questions = list(self.quiz_data[selected_category])
        random.shuffle(available_questions)

        self.current_quiz_questions = available_questions[:min(num_questions_to_ask, len(available_questions))]
        self.current_question_index = 0
        self.correct_answers_count = 0
        self.total_questions_asked = len(self.current_quiz_questions)
        self.selected_radio_button_id = -1  # Reset selected option for new quiz

        print(f"Total questions loaded for quiz: {self.total_questions_asked}")

        if not self.current_quiz_questions:
            print("No questions available for the selected category/number after filtering.")
            QtWidgets.QMessageBox.information(self, "Quiz Info",
                                              "No questions available for the selected category or the requested number of questions. Please choose different settings.")
            self.reset_quiz_state()
            self.display_current_question_page()
            return

        self.display_question()
        self.display_current_question_page()  # Switch to quiz page
        print("--- end of start_quiz method ---")

    def display_question(self):
        print(
            f"display_question called. Current index: {self.current_question_index}, Total questions: {self.total_questions_asked}")

        self.clear_selection()  # Clear any previous radio button selection
        self.ui.label_feedback.setText("")  # Clear previous result message
        self.selected_radio_button_id = -1  # Reset stored selection

        # Enable all radio buttons for new question
        self.ui.radioButton_opt_a.setEnabled(True)
        self.ui.radioButton_opt_b.setEnabled(True)
        self.ui.radioButton_opt_c.setEnabled(True)
        self.ui.radioButton_opt_d.setEnabled(True)

        # Disable Submit and Next buttons until an option is selected for the current question
        self.ui.pushButton_submit_answer.setEnabled(False)
        self.ui.pushButton_next_question.setEnabled(False)

        if self.current_question_index < self.total_questions_asked:
            question_data = self.current_quiz_questions[self.current_question_index]
            self.ui.label_question.setText(
                f"Question {self.current_question_index + 1}/{self.total_questions_asked}:\n{question_data['question']}")
            self.ui.radioButton_opt_a.setText(question_data["options"][0])
            self.ui.radioButton_opt_b.setText(question_data["options"][1])
            self.ui.radioButton_opt_c.setText(question_data["options"][2])
            self.ui.radioButton_opt_d.setText(question_data["options"][3])
            self.ui.question_count_label.setText(f"{self.current_question_index + 1}/{self.total_questions_asked}")

            print(f"Displayed question {self.current_question_index + 1}: {question_data['question']}")
        else:
            self.show_results()
            print("Reached end of questions. Showing results.")

    def check_answer(self):
        """
        Called when the 'Submit Answer' button is clicked.
        Checks the selected answer and provides feedback.
        """
        print(f"check_answer (via Submit button) called. Selected button ID: {self.selected_radio_button_id}")

        # Check if an option has been selected
        if self.selected_radio_button_id == -1:
            self.ui.label_feedback.setText("<font color='orange'>Please select an option before submitting.</font>")
            return  # Do not proceed if no option is selected

        # Get the currently selected radio button and its text (e.g., "a. Option A")
        # Then extract just the 'a', 'b', 'c', 'd' part.
        selected_button_text = self.ui.buttonGroup_answers.button(self.selected_radio_button_id).text()
        selected_option = selected_button_text[0]  # Gets 'a', 'b', 'c', or 'd'

        question_data = self.current_quiz_questions[self.current_question_index]
        correct_option = question_data["correct_option"]

        # Disable radio buttons and the Submit button after an answer is submitted
        self.ui.radioButton_opt_a.setEnabled(False)
        self.ui.radioButton_opt_b.setEnabled(False)
        self.ui.radioButton_opt_c.setEnabled(False)
        self.ui.radioButton_opt_d.setEnabled(False)
        self.ui.pushButton_submit_answer.setEnabled(False)

        if selected_option == correct_option:
            self.correct_answers_count += 1
            self.ui.label_feedback.setText("<font color='green'>Correct!</font>")
            print("Answer: Correct!")
        else:
            # Find the full text of the correct option to display
            correct_option_text = ""
            for option_text in question_data["options"]:
                if option_text.startswith(correct_option):
                    correct_option_text = option_text
                    break
            self.ui.label_feedback.setText(
                f"<font color='red'>Incorrect. The correct answer was: {correct_option_text}.</font>")
            print(f"Answer: Incorrect. Correct was {correct_option_text}")

        # Enable the Next button after feedback is given
        self.ui.pushButton_next_question.setEnabled(True)

    def next_question(self):
        """
        Called when the 'Next' button is clicked.
        Advances to the next question or shows results if quiz is finished.
        """
        print("next_question called.")
        self.current_question_index += 1
        self.selected_radio_button_id = -1  # Reset selection for the next question
        self.display_question()

    def show_results(self):
        print("show_results called.")
        self.ui.label_question.setText(
            f"Quiz Finished! You got {self.correct_answers_count} out of {self.total_questions_asked} correct.")
        self.ui.label_feedback.setText("")
        self.clear_selection()
        # Disable all interactive elements after quiz is finished
        self.ui.radioButton_opt_a.setEnabled(False)
        self.ui.radioButton_opt_b.setEnabled(False)
        self.ui.radioButton_opt_c.setEnabled(False)
        self.ui.radioButton_opt_d.setEnabled(False)

        self.ui.pushButton_submit_answer.setEnabled(False)
        self.ui.pushButton_next_question.setEnabled(False)

        # Ensure the 'Try Again' button is visible if it's the only way to restart
        # It should already be visible by default from your UI, but good to ensure.
        if hasattr(self.ui, 'pushButton'):  # Your 'Try Again' button
            self.ui.pushButton.setVisible(True)

    def clear_selection(self):
        """Clears the selection of all radio buttons in the group."""
        print("clear_selection called.")
        if hasattr(self.ui, 'buttonGroup_answers'):
            # Temporarily set exclusivity to False to allow unchecking all
            self.ui.buttonGroup_answers.setExclusive(False)
            # Uncheck all radio buttons
            self.ui.radioButton_opt_a.setChecked(False)
            self.ui.radioButton_opt_b.setChecked(False)
            self.ui.radioButton_opt_c.setChecked(False)
            self.ui.radioButton_opt_d.setChecked(False)
            # Set exclusivity back to True
            self.ui.buttonGroup_answers.setExclusive(True)
        else:
            # Fallback if buttonGroup_answers wasn't found/created (less likely now)
            self.ui.radioButton_opt_a.setChecked(False)
            self.ui.radioButton_opt_b.setChecked(False)
            self.ui.radioButton_opt_c.setChecked(False)
            self.ui.radioButton_opt_d.setChecked(False)

    def reset_quiz(self):
        """
        Called when the 'Try Again' button is clicked.
        Restarts the quiz immediately with the same settings.
        """
        print("\n--- reset_quiz called (Try Again) ---")
        # Store current settings before resetting to restart quiz directly
        last_selected_category = self.ui.comboBox_category.currentText()
        last_num_questions = self.ui.spinBox_num_questions.value()

        # Reset all internal state variables and UI elements to a clean slate
        self.reset_quiz_state()

        # Set the combo box and spin box values back, then call start_quiz
        if hasattr(self.ui, 'comboBox_category'):
            index = self.ui.comboBox_category.findText(last_selected_category)
            if index != -1:
                self.ui.comboBox_category.setCurrentIndex(index)
        if hasattr(self.ui, 'spinBox_num_questions'):
            self.ui.spinBox_num_questions.setValue(last_num_questions)

        # Immediately re-start the quiz with the same settings
        self.start_quiz()
        print("--- end of reset_quiz method ---")