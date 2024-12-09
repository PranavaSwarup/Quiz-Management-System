import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv


class QuizLeaderboard:
    def __init__(self, root, quiz_details_file="quiz_details"):
        self.root = root
        self.quiz_details_file = quiz_details_file
        self.leaderboard = {}
        self.loading_label = None  # Label for loading message
        self.load_quiz_details()

    def load_quiz_details(self):
        """Load quiz details from the CSV file asynchronously."""
        self.show_loading_message()  # Show loading message

        # Use root.after to call load_quiz_details in a non-blocking way
        self.root.after(100, self._load_quiz_details)

    def _load_quiz_details(self):
        """Load quiz details in the background."""
        try:
            with open(self.quiz_details_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    if row and len(row) > 3:
                        username = row[0]
                        quiz_name = row[1]
                        score = int(row[2])
                        total_questions = int(row[3])

                        # Initialize leaderboard for the quiz if not already present
                        if quiz_name not in self.leaderboard:
                            self.leaderboard[quiz_name] = []

                        # Add the user score and total questions to the leaderboard
                        self.leaderboard[quiz_name].append({
                            "username": username,
                            "score": score,
                            "total_questions": total_questions
                        })
            print(f"Leaderboard loaded: {self.leaderboard}")  # Debugging line

            self.sort_leaderboard()  # Sort leaderboard after loading
            self.hide_loading_message()  # Hide loading message
            self.display_all_leaderboards()  # Display the leaderboards

        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"The file {self.quiz_details_file} was not found.")
            self.hide_loading_message()

    def show_loading_message(self):
        """Show a loading message while data is being loaded."""
        if not self.loading_label:
            self.loading_label = tk.Label(self.root, text="Loading quiz details...", font=("Arial", 16))
            self.loading_label.grid(row=0, column=0, pady=20)

    def hide_loading_message(self):
        """Hide the loading message once data is loaded."""
        if self.loading_label:
            self.loading_label.grid_forget()

    def sort_leaderboard(self):
        """Sort the leaderboard by score and then by total_questions."""
        for quiz_name, users in self.leaderboard.items():
            # Sort users by score (descending), then by total_questions (descending)
            users.sort(key=lambda x: (x["score"], x["total_questions"]), reverse=True)

    def display_leaderboard(self, quiz_name):
        """Display the leaderboard for the given quiz in Tkinter."""
        print(f"Displaying leaderboard for {quiz_name}...")  # Debugging line
        # Clear previous leaderboard widgets if any
        self.clear_widgets()

        if quiz_name not in self.leaderboard:
            messagebox.showwarning("No Data", f"No leaderboard available for {quiz_name}")
            return

        leaderboard_frame = self.create_leaderboard_frame()

        # Create Treeview to display the leaderboard in tabular format
        tree = self.create_treeview(leaderboard_frame)

        # Insert leaderboard data into the treeview
        self.insert_leaderboard_data(tree, quiz_name)

        # Add a button to return to quiz selection or previous screen
        self.add_back_button()

    def clear_widgets(self):
        """Clear all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.grid_forget()

    def create_leaderboard_frame(self):
        """Create and return a frame to hold the leaderboard content."""
        leaderboard_frame = tk.Frame(self.root)
        leaderboard_frame.grid(row=0, column=0, padx=20, pady=20)
        return leaderboard_frame

    def create_treeview(self, leaderboard_frame):
        """Create and return a Treeview widget to display the leaderboard."""
        tree = ttk.Treeview(leaderboard_frame, columns=("Rank", "Username", "Score", "Total Questions"), show="headings")
        tree.grid(row=1, column=0, columnspan=4, pady=10)

        # Define headings and set font to bold for header
        tree.heading("Rank", text="Rank")
        tree.heading("Username", text="Username")
        tree.heading("Score", text="Score")
        tree.heading("Total Questions", text="Total Questions")

        tree.column("Rank", width=50, anchor="center")
        tree.column("Username", width=150, anchor="w")
        tree.column("Score", width=80, anchor="center")
        tree.column("Total Questions", width=120, anchor="center")

        # Style the headings to be bold and highlighted
        tree.tag_configure("heading", font=("Arial", 12, "bold"), background="#d3d3d3")
        return tree

    def insert_leaderboard_data(self, tree, quiz_name):
        """Insert leaderboard data into the treeview."""
        print(f"Inserting data for quiz: {quiz_name}")  # Debugging line
        for rank, user in enumerate(self.leaderboard[quiz_name], start=1):
            print(f"Inserting rank {rank} - {user['username']}")  # Debugging line
            tree.insert("", "end", values=(rank, user["username"], user["score"], user["total_questions"]))

    def add_back_button(self):
        """Add a button to return to quiz selection screen."""
        back_button = tk.Button(self.root, text="Back to Quiz Selection", command=self.back_to_quiz_selection)
        back_button.grid(row=2, column=0, padx=20, pady=20)

    def display_all_leaderboards(self):
        """Display the leaderboard for all quizzes in Tkinter."""
        print("Displaying all leaderboards...")  # Debugging line
        # Clear previous leaderboard widgets if any
        self.clear_widgets()

        all_quiz_names = list(self.leaderboard.keys())
        if not all_quiz_names:
            messagebox.showwarning("No Data", "No leaderboards available.")
            return

        leaderboard_frame = self.create_leaderboard_frame()

        tk.Label(leaderboard_frame, text="Select a quiz to view the leaderboard", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Create a listbox to show all available quizzes
        quiz_listbox = self.create_quiz_listbox(leaderboard_frame)

        # Button to display leaderboard of the selected quiz
        self.add_view_button(leaderboard_frame, quiz_listbox)

    def create_quiz_listbox(self, leaderboard_frame):
        """Create and return a listbox to show available quizzes."""
        quiz_listbox = tk.Listbox(leaderboard_frame, height=10, width=40)
        quiz_listbox.grid(row=1, column=0, columnspan=2, pady=10)

        all_quiz_names = list(self.leaderboard.keys())
        for quiz_name in all_quiz_names:
            quiz_listbox.insert(tk.END, quiz_name)

        print(f"Available quizzes: {all_quiz_names}")  # Debugging line
        return quiz_listbox

    def add_view_button(self, leaderboard_frame, quiz_listbox):
        """Add a button to view the leaderboard of the selected quiz."""
        view_button = tk.Button(leaderboard_frame, text="View Leaderboard", command=lambda: self.view_leaderboard(quiz_listbox))
        view_button.grid(row=2, column=0, columnspan=2, pady=10)

    def view_leaderboard(self, quiz_listbox):
        """View the leaderboard for the selected quiz."""
        selected_index = quiz_listbox.curselection()
        if selected_index:
            selected_quiz = quiz_listbox.get(selected_index)
            self.display_leaderboard(selected_quiz)
        else:
            messagebox.showwarning("No Selection", "Please select a quiz to view the leaderboard.")

    def back_to_quiz_selection(self):
        """Go back to quiz selection screen."""
        self.display_all_leaderboards()

    def sort_column(self, tree, col, reverse):
        """Sort the treeview by column."""
        items = [(tree.set(item, col), item) for item in tree.get_children()]
        items.sort(reverse=reverse)

        for ix, (_, item) in enumerate(items):
            tree.move(item, '', ix)

        tree.heading(col, command=lambda: self.sort_column(tree, col, not reverse))


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizLeaderboard(root)
    root.mainloop()
