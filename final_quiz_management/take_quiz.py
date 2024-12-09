import tkinter as tk
from tkinter import messagebox
import csv
import os
import create_quiz_ as cq  # Alias the import for create_quiz_ as cq


class QuizTakingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Taking App")
        self.quiz = None
        self.user_answers = []
        self.current_question_index = 0
        self.username = ""  # Initialize username as an empty string
        self.selected_quiz_name = ""  # Initialize the selected quiz name

        self.ask_for_username()

    def ask_for_username(self):
        """Ask the user for their name before proceeding to the quiz selection."""
        self.username_label = tk.Label(self.root, text="Please enter your name:", font=("Arial", 14))
        self.username_label.pack(pady=20)

        self.username_entry = tk.Entry(self.root, font=("Arial", 14))
        self.username_entry.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.save_username)
        self.submit_button.pack(pady=10)

    def save_username(self):
        """Save the user's name and proceed to quiz selection."""
        self.username = self.username_entry.get().strip()  # Get the entered username and remove leading/trailing spaces
        if not self.username:
            messagebox.showwarning("Input Error", "Please enter a valid name.")
            return

        # Clear the previous widgets (username entry) and proceed to quiz selection
        self.username_label.pack_forget()
        self.username_entry.pack_forget()
        self.submit_button.pack_forget()

        self.choose_quiz()

    def choose_quiz(self):
        """Create a Listbox to show quizzes and allow selection."""
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(pady=20)

        # Open the CSV file containing the quizzes
        try:
            with open('quizzes_created', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and len(row) > 1:
                        quiz_name = str(row[0])  # Quiz name
                        quiz_type = str(row[1])  # Quiz type
                        quiz_item = f"Quiz name: {quiz_name}, Quiz type: {quiz_type}"
                        self.listbox.insert(tk.END, quiz_item)
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "The quiz file 'quizzes_created' does not exist.")
            self.root.quit()

        # Add a button to start the quiz after a selection
        start_button = tk.Button(self.root, text="Start Quiz", command=self.start_selected_quiz)
        start_button.pack(pady=10)

    def start_selected_quiz(self):
        """Start the selected quiz by loading its file."""
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_quiz_info = self.listbox.get(selected_index)
            self.selected_quiz_name = selected_quiz_info.split(",")[0].split(":")[1].strip()  # Extract quiz name

            # Dynamically determine the quiz file based on the selected name
            quiz_file = f"{self.selected_quiz_name}.csv"
            self.load_quiz(quiz_file)
            self.display_question()
        else:
            messagebox.showwarning("No Selection", "Please select a quiz to start.")

    def load_quiz(self, quiz_file):
        """Load the quiz from the given file."""
        try:
            with open(quiz_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)

                quiz_title = rows[0][1]
                quiz_description = rows[1][1]
                quiz_type = rows[2][1]

                self.quiz = self.create_quiz(quiz_title, quiz_description, quiz_type)

                for row in rows[4:]:
                    question = row[0]
                    if quiz_type == "MCQ":
                        options = row[1].split("|")
                        correct_option = int(row[2])  # Correct option is 0-based, no change needed here
                        self.quiz.add_question(question, options, correct_option, score=1)  # Ensure 'score' is passed
                    elif quiz_type == "True/False":
                        correct_option = int(row[2])  # 0 for True, 1 for False
                        self.quiz.add_question(question, correct_option, score=1)  # Ensure 'score' is passed
                    elif quiz_type == "Short Answer":
                        correct_answer = row[2]  # Short answer (correct_answer is the answer itself)
                        self.quiz.add_question(question, correct_answer, score=1)  # Ensure 'score' is passed

        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"The quiz file {quiz_file} does not exist.")
            self.root.quit()

    def create_quiz(self, title, description, quiz_type):
        """Create an appropriate quiz object based on the type."""
        if quiz_type == "MCQ":
            return cq.MultipleChoiceQuiz(title, description)
        elif quiz_type == "True/False":
            return cq.TrueFalseQuiz(title, description)
        elif quiz_type == "Short Answer":
            return cq.ShortAnswerQuiz(title, description)
        else:
            raise ValueError("Unsupported quiz type")

    def display_question(self):
        """Display the current question based on the quiz type."""
        question_data = self.quiz.questions[self.current_question_index]
        question_text = question_data["question"]

        # Clear previous widgets if any
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Display question
        tk.Label(self.root, text=question_text, font=("Arial", 16)).pack(pady=20)

        if question_data["type"] == "MCQ":
            self.display_mcq_options(question_data)
        elif question_data["type"] == "True/False":
            self.display_tf_options(question_data)
        elif question_data["type"] == "Short Answer":
            self.display_short_answer_field()

        self.create_navigation_buttons()

    def display_mcq_options(self, question_data):
        """Display MCQ options using Listbox."""
        self.mcq_listbox = tk.Listbox(self.root)
        self.mcq_listbox.pack(pady=10)

        # Add options to the Listbox
        for idx, option in enumerate(question_data["options"]):
            self.mcq_listbox.insert(tk.END, option)

        # Store selected option in a variable to be retrieved later
        self.mcq_listbox.bind('<<ListboxSelect>>', self.on_mcq_select)

    def on_mcq_select(self, event):
        """Handle MCQ selection."""
        selected_idx = self.mcq_listbox.curselection()
        if selected_idx:
            self.selected_mcq_answer = selected_idx[0]  # Get the index of the selected option

    def display_tf_options(self, question_data):
        """Display True/False options using Listbox."""
        self.tf_listbox = tk.Listbox(self.root)
        self.tf_listbox.pack(pady=10)

        # Add True and False options to the Listbox
        self.tf_listbox.insert(tk.END, "True")
        self.tf_listbox.insert(tk.END, "False")

        # Store selected option in a variable to be retrieved later
        self.tf_listbox.bind('<<ListboxSelect>>', self.on_tf_select)

    def on_tf_select(self, event):
        """Handle True/False selection."""
        selected_idx = self.tf_listbox.curselection()
        if selected_idx:
            self.selected_tf_answer = selected_idx[0]  # Get the index of the selected option (0 for True, 1 for False)

    def display_short_answer_field(self):
        """Display Short Answer input field."""
        self.sa_entry = tk.Entry(self.root, width=50)
        self.sa_entry.pack(pady=10)

    def create_navigation_buttons(self):
        """Create navigation buttons for next and submit."""
        if self.current_question_index < len(self.quiz.questions) - 1:
            # If not the last question, show the Next button
            next_button = tk.Button(self.root, text="Next", command=self.next_question)
            next_button.pack(pady=10)
        else:
            # If it's the last question, show the Submit Quiz button
            submit_button = tk.Button(self.root, text="Submit Quiz", command=self.submit_quiz)
            submit_button.pack(pady=10)

    def next_question(self):
        """Handle moving to the next question."""
        self.save_answer()
        self.current_question_index += 1
        self.display_question()

    def save_answer(self):
        """Save the user's answer to the current question."""
        question_data = self.quiz.questions[self.current_question_index]
        if question_data["type"] == "MCQ":
            self.user_answers.append(self.selected_mcq_answer)  # Save the selected index (int)
        elif question_data["type"] == "True/False":
            self.user_answers.append(self.selected_tf_answer)  # Save 0 (True) or 1 (False)
        elif question_data["type"] == "Short Answer":
            self.user_answers.append(self.sa_entry.get())
    def submit_quiz(self):
        """Calculate and display the user's score."""
        self.save_answer()

        score = 0
        for i, question_data in enumerate(self.quiz.questions):
            # Check the answer based on question type
            if question_data["type"] == "MCQ":
                correct_option = question_data["correct_option"]
                if self.user_answers[i] == correct_option:
                    score += 1
            elif question_data["type"] == "True/False":
                correct_option = question_data["correct_option"]
                if self.user_answers[i] == correct_option:
                    score += 1
            elif question_data["type"] == "Short Answer":
                correct_answer = question_data["correct_answer"]
                if self.user_answers[i].strip().lower() == correct_answer.strip().lower():
                    score += 1

        # Save the results with the username
        try:
            with open('quiz_details', 'a+') as file:
                writer = csv.writer(file)
                # Save the selected quiz name properly now
                writer.writerow([self.username, self.selected_quiz_name, score, len(self.quiz.questions)])
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving results: {e}")

        # Show the results in a pop-up (this only closes the pop-up, not the main window)
        messagebox.showinfo("Quiz Completed", f"Your Score: {score}/{len(self.quiz.questions)}")

        # Optionally clear any navigation buttons or move to the next phase (e.g., show a message)
        """Display the final message after quiz completion."""
        # Clear all quiz-related widgets (not the entire window)
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Listbox, tk.Button, tk.Entry)):  # Clear only the quiz-related widgets
                widget.pack_forget()

        # Display the final message in front
        final_message = f"Thank you for taking the quiz, {self.username}!\nYour score: {score}."
        final_message_label = tk.Label(self.root, text=final_message, font=("Arial", 16))
        final_message_label.pack(pady=20)

        # Bring the window to the front to ensure the message appears
        self.root.lift()  # Brings the window to the front
        self.root.attributes("-topmost", True)  # Keeps the window on top
        self.root.after(1000, lambda: self.root.attributes("-topmost", False))  # Optionally removes "topmost" after 1 second

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizTakingApp(root)
    root.mainloop()
