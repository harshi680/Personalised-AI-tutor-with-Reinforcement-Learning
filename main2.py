import tkinter as tk
from tkinter import messagebox, ttk
import csv
import random
import os
import pdfViewer
import webbrowser
import joblib
import pandas as pd
from sessionCSV import save_session,load_session
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class QuizApp:
    def __init__(self, master):
        self.master = master
        master.title("Student Quiz System")
        master.geometry("800x650")
        master.configure(bg="#191970")  # Set the main window background to navy blue

        self.questions = self.load_questions_from_csv("pretestnew.csv")
        self.selected_questions = []
        self.answer_vars = []

        self.setup_styles()

        self.create_input_frame()
        self.create_quiz_frame()
        self.create_result_frame()

        self.show_frame(self.input_frame)

    def setup_styles(self):
        """Sets up custom ttk styles for a dark-themed GUI."""
        style = ttk.Style()
        style.theme_use('clam')

        # General Styles for a dark theme
        style.configure('TLabel', font=('Helvetica', 12), background='#191970', foreground='#FFFFFF')
        style.configure('Heading.TLabel', font=('Helvetica', 24, 'bold'), foreground='#ADD8E6',
                        background='#191970')  # Light blue for headings
        style.configure('SubHeading.TLabel', font=('Helvetica', 16, 'bold'), foreground='#D3D3D3',
                        background='#191970')  # Light gray for subheadings

        # Entry and Dropdown Styles
        style.configure('TEntry', fieldbackground='#36454F', foreground='#FFFFFF', borderwidth=1,
                        relief="solid")  # Dark gray entry background
        style.configure('TMenubutton',
                        font=('Helvetica', 12),
                        background='#4682B4',  # Steel blue for dropdowns
                        foreground='#FFFFFF',
                        padding=8,
                        borderwidth=0,
                        relief="flat")
        style.map('TMenubutton',
                  background=[('active', '#5A94C7')])

        # Button Styles
        style.configure('TButton',
                        font=('Helvetica', 13, 'bold'),
                        background='#2E8B57',  # Sea green button color
                        foreground='white',
                        padding=12,
                        borderwidth=0,
                        relief="flat")
        style.map('TButton',
                  background=[('active', '#3CB371')],
                  foreground=[('active', 'white')])

        # Radiobutton Styles
        style.configure('TRadiobutton', font=('Helvetica', 12), background='#191970', foreground='#FFFFFF')
        style.map('TRadiobutton',
                  background=[('active', '#2F4F4F')])  # Dark slate gray on hover

        # Frame Styles
        style.configure('QuizFrame.TFrame', background='#191970', borderwidth=2, relief="groove")
        style.configure('InputFrame.TFrame', background='#191970', borderwidth=2, relief="groove")
        style.configure('ResultFrame.TFrame', background='#191970', borderwidth=2, relief="groove")

        # Separator style for the quiz frame
        style.configure("TSeparator", background='#4682B4')

    def load_questions_from_csv(self, filename):
        """Loads questions from a CSV file."""
        questions_list = []
        try:
            current_dir = os.getcwd()
            filepath = os.path.join(current_dir, filename)

            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        row['class'] = int(row['class'])
                        if 'chapter_no' in row and row['chapter_no']:
                            row['chapter_no'] = int(row['chapter_no'])
                        else:
                            row['chapter_no'] = None
                    except ValueError:
                        messagebox.showerror("Data Error", f"Invalid numeric data (class or chapter_no) in row: {row}")
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
        frame_to_show.pack(fill="both", expand=True, padx=40, pady=40)

    def create_input_frame(self):
        """Creates the initial input frame for student details."""
        self.input_frame = ttk.Frame(self.master, padding="30", style='InputFrame.TFrame')

        ttk.Label(self.input_frame, text="Welcome to the Student assesment System! 📝", style='Heading.TLabel').grid(row=0,
                                                                                                        columnspan=2,
                                                                                                        pady=25)
        ttk.Label(self.input_frame, text="Please enter your details to start:", style='SubHeading.TLabel').grid(row=1,
                                                                                                                columnspan=2,
                                                                                                                pady=(
                                                                                                                15, 25))

        ttk.Label(self.input_frame, text="Student Registration Number:").grid(row=2, column=0, padx=10, pady=10,
                                                                              sticky="w")
        self.regno_entry = ttk.Entry(self.input_frame, width=30)
        self.regno_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(self.input_frame, text="Select Class:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.class_var = tk.StringVar(self.input_frame)
        self.class_var.set("8")
        classes = sorted(list(set(q['class'] for q in self.questions if 'class' in q)))
        class_options = [str(c) for c in classes] if classes else ["8", "9"]
        self.class_dropdown = ttk.OptionMenu(self.input_frame, self.class_var, self.class_var.get(), *class_options,
                                             style='TMenubutton', command=self.update_chapter_and_subject_dropdowns)
        self.class_dropdown.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(self.input_frame, text="Select Subject:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.subject_var = tk.StringVar(self.input_frame)
        self.subject_var.set("Science")
        subjects = sorted(list(set(q['subject'] for q in self.questions if 'subject' in q)))
        subject_options = [s for s in subjects] if subjects else ["Science", "Social", "Mathematics"]
        self.subject_dropdown = ttk.OptionMenu(self.input_frame, self.subject_var, self.subject_var.get(),
                                               *subject_options, style='TMenubutton',
                                               command=self.update_chapter_and_subject_dropdowns)
        self.subject_dropdown.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(self.input_frame, text="Select Chapter:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.chapter_var = tk.StringVar(self.input_frame)
        self.chapter_var.set("Any")
        self.chapter_dropdown = ttk.OptionMenu(self.input_frame, self.chapter_var, "Any", "Any", style='TMenubutton')
        self.chapter_dropdown.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        self.update_chapter_and_subject_dropdowns()

        self.submit_details_button = ttk.Button(self.input_frame, text="Start Quiz", command=self.start_quiz)
        self.submit_details_button.grid(row=6, columnspan=2, pady=10)

        self.input_frame.columnconfigure(1, weight=1)

    def update_chapter_and_subject_dropdowns(self, *args):
        """Updates the available chapters and subjects based on the currently selected class."""
        selected_class_str = self.class_var.get()
        selected_subject_str = self.subject_var.get()

        try:
            selected_class = int(selected_class_str)
        except ValueError:
            selected_class = None

        class_filtered_questions = [
            q for q in self.questions if q.get('class') == selected_class
        ]

        current_subjects = sorted(list(set(q['subject'] for q in class_filtered_questions if 'subject' in q)))
        self.subject_dropdown['menu'].delete(0, 'end')
        if not current_subjects:
            current_subjects = ["Science", "Social", "Mathematics"]
        for subject in current_subjects:
            self.subject_dropdown['menu'].add_command(label=subject, command=tk._setit(self.subject_var, subject,
                                                                                       self.update_chapter_and_subject_dropdowns))
        if selected_subject_str not in current_subjects and current_subjects:
            self.subject_var.set(current_subjects[0])
        elif not current_subjects:
            self.subject_var.set("Science")

        subject_filtered_questions = [
            q for q in class_filtered_questions if q.get('subject') == self.subject_var.get()
        ]

        current_chapters = sorted(list(set(
            q['chapter_no'] for q in subject_filtered_questions if 'chapter_no' in q and q['chapter_no'] is not None)))
        chapter_options = ["Any"] + [str(ch) for ch in current_chapters] if current_chapters else ["Any"]
        self.chapter_dropdown['menu'].delete(0, 'end')
        for chapter in chapter_options:
            self.chapter_dropdown['menu'].add_command(label=chapter, command=tk._setit(self.chapter_var, chapter))

        if self.chapter_var.get() not in chapter_options:
            self.chapter_var.set("Any")

    def create_quiz_frame(self):
        """Creates the frame to display questions."""
        self.quiz_frame = ttk.Frame(self.master, padding="20", style='QuizFrame.TFrame')

        self.quiz_canvas = tk.Canvas(self.quiz_frame, bg="#191970", highlightbackground="#36454F")
        self.quiz_canvas.pack(side="left", fill="both", expand=True)

        self.quiz_scrollbar = ttk.Scrollbar(self.quiz_frame, orient="vertical", command=self.quiz_canvas.yview)
        self.quiz_scrollbar.pack(side="right", fill="y")

        self.quiz_canvas.configure(yscrollcommand=self.quiz_scrollbar.set)
        self.quiz_canvas.bind('<Configure>',
                              lambda e: self.quiz_canvas.configure(scrollregion=self.quiz_canvas.bbox("all")))

        self.questions_inner_frame = ttk.Frame(self.quiz_canvas, style='QuizFrame.TFrame')
        self.canvas_frame_id = self.quiz_canvas.create_window((0, 0), window=self.questions_inner_frame, anchor="nw")

        self.questions_inner_frame.bind("<Configure>", self.on_frame_configure)

        self.submit_answers_button = ttk.Button(self.quiz_frame, text="Submit Answers", command=self.submit_answers)

    def on_frame_configure(self, event):
        """Update the scrollregion of the canvas when the inner frame changes size."""
        self.quiz_canvas.configure(scrollregion=self.quiz_canvas.bbox("all"))
    def chatbot(self):
        os.system("python chatbot.py")

    def read_document(self):
        os.system("python pdfnotes.py")

    def create_result_frame(self):
        """Creates the frame to display quiz results."""
        self.result_frame = ttk.Frame(self.master, padding="30", style='ResultFrame.TFrame')
        ttk.Label(self.result_frame, text="Quiz Results 🎉", style='Heading.TLabel').pack(pady=25)
        self.score_label = ttk.Label(self.result_frame, text="", font=("Helvetica", 22, "bold"), foreground='#ADD8E6',
                                     background='#191970')
        self.score_label.pack(pady=10)
        self.regno_display_label = ttk.Label(self.result_frame, text="", font=("Helvetica", 14), background='#191970',
                                             foreground='#D3D3D3')
        self.regno_display_label.pack(pady=10)

        self.feedback_label = ttk.Label(self.result_frame, text="", font=("Helvetica", 18, 'italic'),
                                        background='#191970')
        self.feedback_label.pack(pady=10)

        self.youtube_link_label = ttk.Label(self.result_frame, text="", font=("Helvetica", 12, "underline"),
                                            foreground="#ADD8E6", cursor="hand2", background='#191970')
        self.youtube_link_label.pack(pady=10)
        self.youtube_link_label.bind("<Button-1>", self.open_youtube_link)
        self.youtube_link_url = ""

        self.post_test_button = ttk.Button(self.result_frame, text="Go for post Test", command=self.GO_postTest,
                                           style='TButton')
        self.start_new_quiz_button = ttk.Button(self.result_frame, text="Start New Quiz", command=self.reset_quiz,
                                                style='TButton')

        self.start_chatbot = ttk.Button(self.result_frame, text="chat guru", command=self.chatbot,
                                                style='TButton')
        self.OpenDoc = ttk.Button(self.result_frame, text="Read Document", command=self.read_document,
                                        style='TButton')

    def GO_postTest(self):
        self.result_frame.destroy()
        self.master.destroy()
        os.system("python postTestGUI.py")

    def start_quiz(self):
        """Validates input and prepares questions for display."""
        regno = self.regno_entry.get().strip()
        selected_class_str = self.class_var.get()
        selected_subject = self.subject_var.get()
        selected_chapter_str = self.chapter_var.get()

        if not regno:
            messagebox.showwarning("Input Error", "Please enter your Registration Number.")
            return

        if not self.questions:
            messagebox.showerror("Data Error",
                                 "No questions loaded from the CSV file. Please check the file and its content.")
            return

        try:
            selected_class = int(selected_class_str)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid class selected.")
            return

        selected_chapter = None
        if selected_chapter_str != "Any":
            try:
                selected_chapter = int(selected_chapter_str)
            except ValueError:
                messagebox.showerror("Input Error", "Invalid chapter selected.")
                return

        filtered_questions = [
            q for q in self.questions
            if q.get('class') == selected_class and
               q.get('subject') == selected_subject and
               (selected_chapter is None or q.get('chapter_no') == selected_chapter)
        ]

        if not filtered_questions:
            messagebox.showinfo("No Questions",
                                f"No questions found for Class {selected_class}, Subject {selected_subject}, and Chapter {selected_chapter_str}. Please try different selections or add more questions to your CSV.")
            return

        self.selected_questions = random.sample(filtered_questions, min(10, len(filtered_questions)))

        for widget in self.questions_inner_frame.winfo_children():
            widget.destroy()

        self.answer_vars = []

        for i, q in enumerate(self.selected_questions):
            ttk.Label(self.questions_inner_frame, text=f"Q{i + 1}: {q['question']}", wraplength=700,
                      font=("Helvetica", 13, "bold"), background='#191970', foreground='#FFFFFF').pack(anchor="w",
                                                                                                       pady=(10, 5))

            var = tk.StringVar(value="")
            self.answer_vars.append(var)

            choices = [q['choice1'], q['choice2'], q['choice3'], q['choice4']]
            random.shuffle(choices)

            for choice in choices:
                ttk.Radiobutton(self.questions_inner_frame, text=choice, variable=var, value=choice,
                                style='TRadiobutton').pack(anchor="w", padx=20, pady=2)

            ttk.Separator(self.questions_inner_frame, orient="horizontal", style="TSeparator").pack(fill="x", pady=10)

        self.submit_answers_button.pack(pady=20, padx=20)
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
        #------------prediction-----------


        # Load trained model
        model = joblib.load("marks_model.pkl")

        # Function to test marks
        def sendemail(sentance,value):
            sender_email = "myprojectemails4u@gmail.com"  # Enter your email
            sender_password = "cyaoslrmrystypcm"  # Enter your email password

            # receiver_email = receiver_entry.get()
            receiver_email = value
            # subject = subject_entry.get()
            subject = "Exam Remarks"
            message = " Remarks for your improvement exam is"+ sentance

            # Constructing the email
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            try:
                # Establishing a connection to the SMTP server
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                # Logging in to the email account
                server.login(sender_email, sender_password)
                # Sending the email
                server.send_message(msg)
                # Quitting the server
                server.quit()
                # messagebox.showinfo("Success", "Email sent successfully!")
                messagebox.showinfo("alert", "Alert Send  successfully!")
            except Exception as e:
                # messagebox.showerror("Error", f"An error occurred: {str(e)}")
                print(e)



        def predict_reward(marks):
            # Pass as DataFrame with correct column name
            df = pd.DataFrame([[marks]], columns=["marks"])
            result = model.predict(df)[0]
            return "Reward" if result == 1 else "Penalty"

        # Example tests
        print("Marks: 3 ->", predict_reward(3))
        print("Marks: 8 ->", predict_reward(8))
        print("Marks: 10 ->", predict_reward(10))

        # User input
        marks = score
        print("Result:", predict_reward(marks))
        messagebox.showinfo("Reward info",predict_reward(marks))

        def get_random_sentence(label):
            # Decide which CSV to load
            if label.lower() == "reward":
                file = "rewards.csv"
            else:
                file = "remarks.csv"

            # Load CSV (assuming it has one column of sentences)
            data = pd.read_csv(file, header=None)  # no header
            sentences = data[0].tolist()  # convert first column to list

            # Pick random sentence
            return random.choice(sentences)

        # Example usage
        user_input = predict_reward(marks)
        sentence = get_random_sentence(user_input)
        print("👉", sentence)
        messagebox.showinfo("Remark infomation",sentence)
        session = load_session()
        for key, value in session.items():
            print(f"  {key}: {value}")
            sendemail(sentence,value)

        #---------------------------
        if score < 5:
            classname = self.class_var.get()
            subname = self.subject_var.get()
            chapterno = self.chapter_var.get()
            self.feedback_label.config(text="Needs Improvement! Keep learning. 📚", foreground='#FF6347')
            #self.youtube_link_url = "https://www.youtube.com/watch?v=s0n00f5k1-c"
            self.youtube_link_url = "https://www.youtube.com/results?search_query=" + classname + " of " + subname + " in " + chapterno + " chapter in karnataka state sylabus"
            self.youtube_link_label.config(text="Click here for Study Tips on YouTube 💡")
            self.post_test_button.pack_forget()
            self.start_new_quiz_button.pack(pady=10)
            self.start_chatbot.pack(pady=10)

            self.OpenDoc.pack(pady=10)


        elif score >=5  and score < 8:
            self.feedback_label.config(text="Well tried! Better luck next time. ✨", foreground='#FFD700')
            self.post_test_button.pack_forget()
            self.start_new_quiz_button.pack(pady=30)
            self.start_chatbot.pack(pady=20)
            self.OpenDoc.pack(pady=10)
        elif score >= 8:
            self.feedback_label.config(text="Excellent! You're doing great! 🎉", foreground='#32CD32')
            self.post_test_button.pack(pady=50)
            self.start_new_quiz_button.pack(pady=10)
            self.start_chatbot.pack(pady=20)
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
        self.chapter_var.set("Any")
        self.update_chapter_and_subject_dropdowns()

        self.selected_questions = []
        self.answer_vars = []
        for widget in self.questions_inner_frame.winfo_children():
            widget.destroy()
        self.submit_answers_button.pack_forget()
        self.feedback_label.config(text="")
        self.youtube_link_label.config(text="")
        self.youtube_link_url = ""
        self.post_test_button.pack_forget()
        self.start_new_quiz_button.pack_forget()
        self.show_frame(self.input_frame)


# --- Main Application Execution ---
if __name__ == "__main__":
    csv_filename = "pretestnew.csv"
    if not os.path.exists(csv_filename):
        dummy_csv_content = """
class,chapter_no,subject,question,choice1,choice2,choice3,choice4,correct_answer
8,1,Science,What is the chemical symbol for water?,O2,H2O,CO2,NaCl,H2O
8,1,Science,What is the powerhouse of the cell?,Nucleus,Mitochondria,Ribosome,Cytoplasm,Mitochondria
8,2,Science,Which gas do plants absorb from the atmosphere?,Oxygen,Nitrogen,Carbon Dioxide,Hydrogen,Carbon Dioxide
8,2,Science,What is the freezing point of water in Celsius?,0,10,100,-10,0
8,1,Social,What is the capital of France?,Berlin,Madrid,Paris,Rome,Paris
8,1,Social,Which planet is known as the Red Planet?,Earth,Mars,Jupiter,Venus,Mars
8,2,Social,What is the largest ocean on Earth?,Atlantic Ocean,Indian Ocean,Arctic Ocean,Pacific Ocean,Pacific Ocean
8,2,Social,Who painted the Mona Lisa?,Vincent van Gogh,Pablo Picasso,Leonardo da Vinci,Claude Monet,Leonardo da Vinci
9,1,Mathematics,What is 5 + 7?,10,11,12,13,12
9,1,Mathematics,If a square has a side length of 4 cm, what is its area?,8 sq cm,12 sq cm,16 sq cm,20 sq cm,16 sq cm
9,2,Mathematics,What is the value of Pi (approximately)?,3.14,3.00,3.10,3.20,3.14
9,2,Mathematics,What is the smallest prime number?,0,1,2,3,2
9,1,Science,What is the largest organelle in an animal cell?,Mitochondria,Ribosome,Nucleus,Endoplasmic Reticulum,Nucleus
9,2,Science,What is the chemical symbol for sodium?,So,Na,Nd,Ni,Na
9,2,Science,Which element is most abundant in Earth's crust?,Oxygen,Silicon,Aluminum,Iron,Oxygen
        """
        with open(csv_filename, "w", encoding="utf-8", newline="") as f:
            f.write(dummy_csv_content.strip())
        print(f"Created a dummy '{csv_filename}' for demonstration.")

    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()