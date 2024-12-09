import tkinter as tk
from tkinter import messagebox
import csv
import os


class Quiz:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.questions = []


class MultipleChoiceQuiz(Quiz):
    def add_question(self, question, options, correct_option, score):
        self.questions.append({
            "type": "MCQ",
            "question": question,
            "options": options,
            "correct_option": correct_option,
            "score": score
        })


class TrueFalseQuiz(Quiz):
    def add_question(self, question, correct_option, score):
        self.questions.append({
            "type": "True/False",
            "question": question,
            "options": ["True", "False"],
            "correct_option": correct_option,
            "score": score
        })


class ShortAnswerQuiz(Quiz):
    def add_question(self, question, correct_answer, score):
        self.questions.append({
            "type": "Short Answer",
            "question": question,
            "correct_answer": correct_answer,
            "score": score
        })


class QuizCreationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Creation System")
        self.quiz = None

        self.quiz_type = None
        self.setup_quiz_type_page()

    def setup_quiz_type_page(self):
        """Setup the quiz type selection page."""
        self.type_frame = tk.Frame(self.root)
        self.type_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.type_frame, text="Select Quiz Type", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.type_frame, text="Multiple Choice Quiz", command=lambda: self.setup_title_page("MCQ")).pack(pady=10)
        tk.Button(self.type_frame, text="True/False Quiz", command=lambda: self.setup_title_page("True/False")).pack(pady=10)
        tk.Button(self.type_frame, text="Short Answer Quiz", command=lambda: self.setup_title_page("Short Answer")).pack(pady=10)

    def setup_title_page(self, quiz_type):
        self.quiz_type = quiz_type
        self.type_frame.destroy()

        self.title_frame = tk.Frame(self.root)
        self.title_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.title_frame, text=f"{quiz_type} Quiz", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.title_frame, text="Quiz Title:").pack()
        self.title_entry = tk.Entry(self.title_frame, width=50)
        self.title_entry.pack()

        tk.Label(self.title_frame, text="Quiz Description:").pack()
        self.description_entry = tk.Entry(self.title_frame, width=50)
        self.description_entry.pack()

        tk.Button(self.title_frame, text="Next", command=self.setup_quiz_creation_page).pack(pady=20)

    def setup_quiz_creation_page(self):
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()

        if not title or not description:
            messagebox.showwarning("Input Error", "Please provide a title and description for the quiz.")
            return

        if self.quiz_type == "MCQ":
            self.quiz = MultipleChoiceQuiz(title, description)
        elif self.quiz_type == "True/False":
            self.quiz = TrueFalseQuiz(title, description)
        elif self.quiz_type == "Short Answer":
            self.quiz = ShortAnswerQuiz(title, description)

        self.title_frame.destroy()
        self.creation_frame = tk.Frame(self.root)
        self.creation_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.creation_frame, text=f"Create {self.quiz_type} Quiz", font=("Arial", 18)).pack(pady=20)

        if self.quiz_type == "MCQ":
            self.setup_mcq_creation_page()
        elif self.quiz_type == "True/False":
            self.setup_tf_creation_page()
        elif self.quiz_type == "Short Answer":
            self.setup_sa_creation_page()

    def setup_mcq_creation_page(self):
        """Setup Multiple Choice Question creation page."""
        tk.Label(self.creation_frame, text="Question:").pack()
        self.question_entry = tk.Entry(self.creation_frame, width=50)
        self.question_entry.pack()

        tk.Label(self.creation_frame, text="Options:").pack()
        self.options_frame = tk.Frame(self.creation_frame)
        self.options_frame.pack()

        self.option_entry = tk.Entry(self.options_frame, width=40)
        self.option_entry.pack(side=tk.LEFT, padx=5)

        self.add_option_button = tk.Button(self.options_frame, text="Add Option", command=self.add_option)
        self.add_option_button.pack(side=tk.LEFT, padx=5)

        self.options_listbox = tk.Listbox(self.creation_frame, width=50, height=5)
        self.options_listbox.pack(pady=10)

        self.delete_option_button = tk.Button(self.creation_frame, text="Delete Selected Option", command=self.delete_option)
        self.delete_option_button.pack(pady=5)

        tk.Label(self.creation_frame, text="Correct Option (Enter Index 1-4):").pack()
        self.correct_option_entry = tk.Entry(self.creation_frame, width=50)
        self.correct_option_entry.pack()

        tk.Label(self.creation_frame, text="Score for this question:").pack()
        self.score_entry = tk.Entry(self.creation_frame, width=50)
        self.score_entry.pack()

        self.add_common_controls()

    def setup_tf_creation_page(self):
        tk.Label(self.creation_frame, text="Question:").pack()
        self.question_entry = tk.Entry(self.creation_frame, width=50)
        self.question_entry.pack()

        tk.Label(self.creation_frame, text="Correct Answer (True/False):").pack()
        self.correct_option_entry = tk.Entry(self.creation_frame, width=50)
        self.correct_option_entry.pack()

        tk.Label(self.creation_frame, text="Score for this question:").pack()
        self.score_entry = tk.Entry(self.creation_frame, width=50)
        self.score_entry.pack()

        self.add_common_controls()

    def setup_sa_creation_page(self):
        """Setup Short Answer Question creation page."""
        tk.Label(self.creation_frame, text="Question:").pack()
        self.question_entry = tk.Entry(self.creation_frame, width=50)
        self.question_entry.pack()

        tk.Label(self.creation_frame, text="Correct Answer:").pack()
        self.correct_option_entry = tk.Entry(self.creation_frame, width=50)
        self.correct_option_entry.pack()

        tk.Label(self.creation_frame, text="Score for this question:").pack()
        self.score_entry = tk.Entry(self.creation_frame, width=50)
        self.score_entry.pack()

        self.add_common_controls()

    def add_common_controls(self):
        tk.Button(self.creation_frame, text="Add Question", command=self.add_question).pack(pady=10)
        tk.Label(self.creation_frame, text="Questions:").pack()
        self.questions_listbox = tk.Listbox(self.creation_frame, width=80, height=10)
        self.questions_listbox.pack(pady=10)

        self.delete_question_button = tk.Button(self.creation_frame, text="Delete Selected Question", command=self.delete_question)
        self.delete_question_button.pack(pady=5)

        self.save_quiz_button = tk.Button(self.creation_frame, text="Save Quiz", command=self.save_quiz)
        self.save_quiz_button.pack(pady=20)

    def add_option(self):
        option = self.option_entry.get().strip()
        if not option:
            messagebox.showwarning("Input Error", "Option cannot be empty.")
            return
        current_options = self.options_listbox.size() + 1
        if current_options > 4:
            messagebox.showwarning("Input Error", "You can only add up to 4 options.")
            return
        self.options_listbox.insert(tk.END, f"{current_options}. {option}")
        self.option_entry.delete(0, tk.END)

    def delete_option(self):
        selected_option = self.options_listbox.curselection()
        if not selected_option:
            messagebox.showwarning("Selection Error", "No option selected.")
            return
        self.options_listbox.delete(selected_option)

    def add_question(self):
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Input Error", "Question cannot be empty.")
            return

        score = self.score_entry.get().strip()
        if not score:
            messagebox.showwarning("Input Error", "Score cannot be empty.")
            return

        try:
            score = float(score)
            if score < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Score must be a number greater than or equal to 0.")
            return

        if self.quiz_type == "MCQ":
            options = list(self.options_listbox.get(0, tk.END))
            if len(options) < 2:
                messagebox.showwarning("Input Error", "At least two options are required.")
                return

            try:
                correct_option = int(self.correct_option_entry.get().strip())
                if not (1 <= correct_option <= len(options)):
                    messagebox.showwarning("Input Error", "Correct option index is out of range.")
                    return
            except ValueError:
                messagebox.showwarning("Input Error", "Correct option must be an integer.")
                return

            self.quiz.add_question(
                question,
                [opt.split(". ", 1)[1] for opt in options],
                correct_option - 1,
                score
            )
        elif self.quiz_type == "True/False":
            correct_option = self.correct_option_entry.get().strip().capitalize()
            if correct_option not in ["True", "False"]:
                messagebox.showwarning("Input Error", "Correct answer must be 'True' or 'False'.")
                return
            self.quiz.add_question(question, 0 if correct_option == "True" else 1, score)
        elif self.quiz_type == "Short Answer":
            correct_answer = self.correct_option_entry.get().strip()
            if not correct_answer:
                messagebox.showwarning("Input Error", "Correct answer cannot be empty.")
                return
            self.quiz.add_question(question, correct_answer, score)

        self.update_question_list()
        self.clear_fields()

    def update_question_list(self):
        self.questions_listbox.delete(0, tk.END)
        for index, question in enumerate(self.quiz.questions, start=1):
            self.questions_listbox.insert(tk.END, f"{index}. {question['question']}")

    def delete_question(self):
        selected_index = self.questions_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No question selected.")
            return
        self.questions_listbox.delete(selected_index)
        del self.quiz.questions[selected_index[0]]
        self.update_question_list()

    def clear_fields(self):
        """Clear input fields."""
        self.question_entry.delete(0, tk.END)
        if self.quiz_type == "MCQ":
            self.options_listbox.delete(0, tk.END)
        self.correct_option_entry.delete(0, tk.END)
        self.score_entry.delete(0, tk.END)

    def save_quiz(self):
        if not self.quiz.questions:
            messagebox.showwarning("Save Error", "Please add at least one question before saving.")
            return

        os.makedirs("quizzes", exist_ok=True)
        filename = f"quizzes/{self.quiz.title.replace(' ', '_')}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", self.quiz.title])
            writer.writerow(["Description", self.quiz.description])

            writer.writerow(["Type", self.quiz_type])
            writer.writerow(["Questions"])
            for question in self.quiz.questions:
                if question["type"] == "MCQ":
                    writer.writerow([
                        question["question"],
                        "|".join(question["options"]),
                        question["correct_option"],
                        question["score"]
                    ])
                elif question["type"] == "True/False":
                    writer.writerow([
                        question["question"],
                        "True/False",
                        question["correct_option"],
                        question["score"]
                    ])
                elif question["type"] == "Short Answer":
                    writer.writerow([
                        question["question"],
                        "Short Answer",
                        question["correct_answer"],
                        question["score"]
                    ])

        messagebox.showinfo("Quiz Saved", f"Quiz saved successfully as '{filename}'.")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizCreationApp(root)
    root.mainloop()
