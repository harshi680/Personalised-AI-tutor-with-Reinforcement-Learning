import sys
import tkinter as tk
from tkinter import messagebox, ttk
import csv
import random
import os
import webbrowser
import subprocess







class QuizApp:
    def __init__(self, master):
        self.master = master
        master.title("Student Quiz System")
        master.geometry("800x650")
        master.configure(bg="#F0F8FF")
        subprocess.run(["python", "facetracking.py"])
        self.questions = self.load_questions_from_csv("pretestnew.csv")
        self.selected_questions = []
        self.answer_vars = []

        self.setup_styles()

        # Tkinter variables to hold dropdown selections
        self.class_var = tk.StringVar(master)
        self.subject_var = tk.StringVar(master)
        self.chapter_var = tk.StringVar(master)  # New variable for chapter

        self.create_input_frame()
        self.create_quiz_frame()
        self.create_result_frame()

        self.show_frame(self.input_frame)

    def setup_styles(self):
        """Sets up custom ttk styles for a more colorful GUI."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Arial', 11), background='#F0F8FF', foreground='#333333')
        style.configure('Heading.TLabel', font=('Arial', 22, 'bold'), foreground='#4682B4', background='#F0F8FF')
        style.configure('SubHeading.TLabel', font=('Arial', 14, 'bold'), foreground='#2F4F4F', background='#F0F8FF')
        style.configure('TEntry', fieldbackground='#FFFFFF', foreground='#333333', borderwidth=1, relief="solid")
        style.configure('TButton',
                        font=('Arial', 12, 'bold'),
                        background='#4CAF50',
                        foreground='white',
                        padding=10,
                        borderwidth=0,
                        relief="flat")
        style.map('TButton',
                  background=[('active', '#45a049')],
                  foreground=[('active', 'white')])
        style.configure('TRadiobutton', font=('Arial', 11), background='#F0F8FF', foreground='#444444')
        style.map('TRadiobutton',
                  background=[('active', '#E0FFFF')])
        style.configure('TMenubutton',
                        font=('Arial', 11),
                        background='#87CEEB',
                        foreground='#333333',
                        padding=5,
                        borderwidth=1,
                        relief="solid")
        style.map('TMenubutton',
                  background=[('active', '#7AC5CD')])
        style.configure('QuizFrame.TFrame', background='#F8F8FF', borderwidth=2, relief="groove")
        style.configure('InputFrame.TFrame', background='#F0F8FF', borderwidth=2, relief="groove")
        style.configure('ResultFrame.TFrame', background='#F0F8FF', borderwidth=2, relief="groove")

    def load_questions_from_csv(self, filename):
        """Loads questions from a CSV file."""
        questions_list = []
        try:
            current_dir = os.getcwd()
            filepath = os.path.join(current_dir, filename)

            # Use 'io.open' for better cross-platform compatibility if needed, but 'open' is fine here
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        row['class'] = int(row['class'])
                        # Ensure chapter_no is also an int for filtering
                        row['chapter_no'] = int(row['chapter_no'])
                    except (ValueError, KeyError) as e:
                        messagebox.showerror("Data Error",
                                             f"Invalid numeric data or missing column in row: {row}. Error: {e}")
                        continue
                    questions_list.append(row)
            if not questions_list:
                messagebox.showwarning("File Empty", f"The file '{filename}' appears to be empty or malformed.")
        except FileNotFoundError:
            messagebox.showerror("File Error",
                                 f"The file '{filename}' was not found. Please ensure it is in the same directory as the script.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the CSV file: {e}")
        return questions_list

    def show_frame(self, frame_to_show):
        """Hides all frames and shows the specified one."""
        self.input_frame.pack_forget()
        self.quiz_frame.pack_forget()
        self.result_frame.pack_forget()
        frame_to_show.pack(fill="both", expand=True, padx=30, pady=30)

    def create_input_frame(self):
        """Creates the initial input frame for student details."""
        self.input_frame = ttk.Frame(self.master, padding="30", style='InputFrame.TFrame')

        ttk.Label(self.input_frame, text="Welcome to the Pretest Exam!", style='Heading.TLabel').grid(row=0,
                                                                                                     columnspan=2,
                                                                                                     pady=25)
        ttk.Label(self.input_frame, text="Please enter your details to start:", style='SubHeading.TLabel').grid(row=1,
                                                                                                                columnspan=2,
                                                                                                                pady=15)

        ttk.Label(self.input_frame, text="Student Registration Number:", style='TLabel').grid(row=2, column=0, padx=5,
                                                                                              pady=10, sticky="w")
        self.regno_entry = ttk.Entry(self.input_frame, width=30, style='TEntry')
        self.regno_entry.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        ttk.Label(self.input_frame, text="Select Class:", style='TLabel').grid(row=3, column=0, padx=5, pady=10,
                                                                               sticky="w")
        self.class_var.set("8")
        self.class_dropdown = ttk.OptionMenu(self.input_frame, self.class_var, "8", "8", "9", style='TMenubutton',
                                             command=self.update_chapter_options)
        self.class_dropdown.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

        ttk.Label(self.input_frame, text="Select Subject:", style='TLabel').grid(row=4, column=0, padx=5, pady=10,
                                                                                 sticky="w")
        self.subject_var.set("Science")
        self.subject_dropdown = ttk.OptionMenu(self.input_frame, self.subject_var, "Science", "Science", "Social",
                                               "Mathematics", style='TMenubutton', command=self.update_chapter_options)
        self.subject_dropdown.grid(row=4, column=1, padx=5, pady=10, sticky="ew")

        # New chapter dropdown
        ttk.Label(self.input_frame, text="Select Chapter:", style='TLabel').grid(row=5, column=0, padx=5, pady=10,
                                                                                 sticky="w")
        self.chapter_var.set("Select Chapter...")
        self.chapter_dropdown = ttk.OptionMenu(self.input_frame, self.chapter_var, "Select Chapter...")
        self.chapter_dropdown.grid(row=5, column=1, padx=5, pady=10, sticky="ew")

        self.submit_details_button = ttk.Button(self.input_frame, text="Start Quiz", command=self.start_quiz,
                                                style='TButton')
        self.submit_details_button.grid(row=6, columnspan=2, pady=30)

        self.input_frame.columnconfigure(1, weight=1)

        # Initial call to populate the chapter dropdown
        self.update_chapter_options()

    def update_chapter_options(self, *args):
        """Updates the chapter dropdown based on selected class and subject."""
        selected_class = self.class_var.get()
        selected_subject = self.subject_var.get()

        # Filter unique chapter numbers based on the current selections
        chapters = sorted(list(set(
            q['chapter_no'] for q in self.questions
            if q.get('class') == int(selected_class) and q.get('subject') == selected_subject
        )))

        # Clear and re-populate the chapter dropdown
        menu = self.chapter_dropdown["menu"]
        menu.delete(0, "end")

        # Set a default value
        self.chapter_var.set("Select Chapter...")
        if not chapters:
            menu.add_command(label="No Chapters Available",
                             command=tk._setit(self.chapter_var, "No Chapters Available"))
        else:
            for chapter in chapters:
                menu.add_command(label=chapter, command=tk._setit(self.chapter_var, chapter))

    def create_quiz_frame(self):
        """Creates the frame to display questions."""
        self.quiz_frame = ttk.Frame(self.master, padding="20", style='QuizFrame.TFrame')

        self.quiz_canvas = tk.Canvas(self.quiz_frame, bg="#F8F8FF", highlightbackground="#D3D3D3")
        self.quiz_canvas.pack(side="left", fill="both", expand=True)

        self.quiz_scrollbar = ttk.Scrollbar(self.quiz_frame, orient="vertical", command=self.quiz_canvas.yview)
        self.quiz_scrollbar.pack(side="right", fill="y")

        self.quiz_canvas.configure(yscrollcommand=self.quiz_scrollbar.set)
        self.quiz_canvas.bind('<Configure>',
                              lambda e: self.quiz_canvas.configure(scrollregion=self.quiz_canvas.bbox("all")))

        self.questions_inner_frame = ttk.Frame(self.quiz_canvas, style='QuizFrame.TFrame')
        self.canvas_frame_id = self.quiz_canvas.create_window((0, 0), window=self.questions_inner_frame, anchor="nw")

        self.questions_inner_frame.bind("<Configure>", self.on_frame_configure)

        self.submit_answers_button = ttk.Button(self.quiz_frame, text="Submit Answers", command=self.submit_answers,
                                                style='TButton')


    def on_frame_configure(self, event):
        """Update the scrollregion of the canvas when the inner frame changes size."""
        self.quiz_canvas.configure(scrollregion=self.quiz_canvas.bbox("all"))


    def create_result_frame(self):
        """Creates the frame to display quiz results."""
        self.result_frame = ttk.Frame(self.master, padding="30", style='ResultFrame.TFrame')
        ttk.Label(self.result_frame, text="Quiz Results", style='Heading.TLabel').pack(pady=25)
        self.score_label = ttk.Label(self.result_frame, text="", font=("Arial", 20, "bold"), foreground='#1E90FF',
                                     background='#F0F8FF')
        self.score_label.pack(pady=15)
        self.regno_display_label = ttk.Label(self.result_frame, text="", font=("Arial", 14), background='#F0F8FF',
                                             foreground='#555555')
        self.regno_display_label.pack(pady=10)

        self.feedback_label = ttk.Label(self.result_frame, text="", font=("Arial", 18, "italic"), background='#F0F8FF')
        self.feedback_label.pack(pady=20)

        self.youtube_link_label = ttk.Label(self.result_frame, text="", font=("Arial", 12, "underline"),
                                            foreground="blue", cursor="hand2", background='#F0F8FF')
        self.youtube_link_label.pack(pady=10)
        self.youtube_link_label.bind("<Button-1>", self.open_youtube_link)
        self.youtube_link_url = ""

        ttk.Button(self.result_frame, text="Start New Quiz", command=self.reset_quiz, style='TButton').pack(pady=30)

    def facetracking(self):
        subprocess.run(["python", "facetracking.py"])

    def start_quiz(self):
        """Validates input and prepares questions for display."""
        self.facetracking()
        regno = self.regno_entry.get().strip()
        selected_class = self.class_var.get()
        selected_subject = self.subject_var.get()
        selected_chapter = self.chapter_var.get()


        if not regno:
            messagebox.showwarning("Input Error", "Please enter your Registration Number.")
            return
        if selected_chapter == "Select Chapter..." or selected_chapter == "No Chapters Available":
            messagebox.showwarning("Input Error", "Please select a chapter.")
            return

        if not self.questions:
            messagebox.showerror("Data Error",
                                 "No questions loaded from the CSV file. Please check the file and its content.")
            return

        # Filter questions based on selected class, subject, AND chapter
        filtered_questions = [
            q for q in self.questions
            if q.get('class') == int(selected_class) and q.get('subject') == selected_subject and q.get(
                'chapter_no') == int(selected_chapter)
        ]

        if not filtered_questions:
            messagebox.showinfo("No Questions", f"No questions found for the selected criteria.")
            return

        self.selected_questions = random.sample(filtered_questions, min(10, len(filtered_questions)))

        for widget in self.questions_inner_frame.winfo_children():
            widget.destroy()

        self.answer_vars = []

        for i, q in enumerate(self.selected_questions):
            ttk.Label(self.questions_inner_frame, text=f"Q{i + 1}: {q['question']}", wraplength=700,
                      font=("Arial", 12, "bold"), background='#F8F8FF', foreground='#333333').pack(anchor="w",
                                                                                                   pady=(10, 5))

            var = tk.StringVar(value="")
            self.answer_vars.append(var)

            choices = [q['choice1'], q['choice2'], q['choice3'], q['choice4']]
            random.shuffle(choices)

            for choice in choices:
                ttk.Radiobutton(self.questions_inner_frame, text=choice, variable=var, value=choice,
                                style='TRadiobutton').pack(anchor="w", padx=20)

            ttk.Separator(self.questions_inner_frame, orient="horizontal").pack(fill="x", pady=5)

        self.submit_answers_button.pack(pady=20)
        self.quiz_canvas.update_idletasks()
        self.quiz_canvas.config(scrollregion=self.quiz_canvas.bbox("all"))
        self.show_frame(self.quiz_frame)

    def submit_answers(self):
        """Calculates the score and displays results with feedback."""
        score = 0
        total_questions = len(self.selected_questions)

        all_answered = True
        for i, var in enumerate(self.answer_vars):
            if not var.get():
                all_answered = False
                break

        if not all_answered:
            messagebox.showwarning("Incomplete Quiz", "Please answer all questions before submitting.")
            return

        for i, q in enumerate(self.selected_questions):
            selected_answer = self.answer_vars[i].get()
            if selected_answer == q['correct_answer']:
                score += 1

        regno = self.regno_entry.get().strip()
        self.score_label.config(text=f"Your Score: {score} / {total_questions}")
        self.regno_display_label.config(text=f"Registration Number: {regno}")

        self.youtube_link_label.config(text="")
        self.youtube_link_url = ""

        if score < 5:
            classname=self.class_var.get()
            subname=self.subject_var.get()
            chapterno=self.chapter_var.get()
            self.feedback_label.config(text="Needs Improvement! Keep learning. 📚", foreground='#DC143C')
            self.youtube_link_url = "https://www.youtube.com/results?search_query="+classname+" of "+subname+" in "+ chapterno+ " chapter in karnataka state sylabus"
            self.youtube_link_label.config(text="Click here for Study Tips on YouTube 💡")
        elif 5 <= score < 8:
            self.feedback_label.config(text="Well tried! Better luck next time. ✨", foreground='#FF8C00')
        else:
            self.feedback_label.config(text="Excellent! You're doing great! 🎉", foreground='#228B22')

        self.show_frame(self.result_frame)

    def open_youtube_link(self, event):
        """Opens the stored YouTube link in a web browser."""
        if self.youtube_link_url:
            webbrowser.open_new_tab(self.youtube_link_url)

    def reset_quiz(self):
        """Resets the application to the initial input screen."""
        self.regno_entry.delete(0, tk.END)
        self.class_var.set("8")
        self.subject_var.set("Science")
        self.chapter_var.set("Select Chapter...")
        self.update_chapter_options()  # Re-populate chapters for the default selections
        self.selected_questions = []
        self.answer_vars = []
        for widget in self.questions_inner_frame.winfo_children():
            widget.destroy()
        self.submit_answers_button.pack_forget()
        self.feedback_label.config(text="")
        self.youtube_link_label.config(text="")
        self.youtube_link_url = ""
        self.show_frame(self.input_frame)


# --- Main Application Execution ---
if __name__ == "__main__":
    python_path = sys.executable
    subprocess.Popen(["python", "facetracking.py"])

    csv_filename = "pretestnew.csv"
    if not os.path.exists(csv_filename):
        dummy_csv_content = """
class,chapter_no,subject,question,choice1,choice2,choice3,choice4,correct_answer
8,1,Science,What is the chemical symbol for water?,O2,H2O,CO2,NaCl,H2O
8,2,Science,What is the powerhouse of the cell?,Nucleus,Mitochondria,Ribosome,Cytoplasm,Mitochondria
8,1,Science,Which gas do plants absorb from the atmosphere?,Oxygen,Nitrogen,Carbon Dioxide,Hydrogen,Carbon Dioxide
8,2,Science,What is the freezing point of water in Celsius?,0,10,100,-10,0
8,1,Social,What is the capital of France?,Berlin,Madrid,Paris,Rome,Paris
8,2,Social,Which planet is known as the Red Planet?,Earth,Mars,Jupiter,Venus,Mars
8,1,Social,What is the largest ocean on Earth?,Atlantic Ocean,Indian Ocean,Arctic Ocean,Pacific Ocean,Pacific Ocean
8,2,Social,Who painted the Mona Lisa?,Vincent van Gogh,Pablo Picasso,Leonardo da Vinci,Claude Monet,Leonardo da Vinci
9,1,Mathematics,What is 5 + 7?,10,11,12,13,12
9,2,Mathematics,If a square has a side length of 4 cm, what is its area?,8 sq cm,12 sq cm,16 sq cm,20 sq cm,16 sq cm
9,1,Science,What is the largest organelle in an animal cell?,Mitochondria,Ribosome,Nucleus,Endoplasmic Reticulum,Nucleus
9,2,Science,What is the chemical symbol for sodium?,So,Na,Nd,Ni,Na
9,1,Science,Which element is most abundant in Earth's crust?,Oxygen,Silicon,Aluminum,Iron,Oxygen
9,2,Science,What is the process of a solid turning directly into a gas called?,Melting,Evaporation,Sublimation,Condensation,Sublimation
9,1,Social,What is the capital of Australia?,Sydney,Melbourne,Canberra,Perth,Canberra
9,2,Social,Which gas is primarily responsible for the greenhouse effect?,Oxygen,Nitrogen,Methane,Carbon Dioxide,Carbon Dioxide
        """
        with open(csv_filename, "w", encoding="utf-8", newline="") as f:
            f.write(dummy_csv_content.strip())
        print(f"Created a dummy '{csv_filename}' for demonstration.")

    root = tk.Tk()
    app = QuizApp(root)
    #process.terminate()

    root.mainloop()