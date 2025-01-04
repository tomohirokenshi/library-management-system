import tkinter as tk
from tkinter import messagebox
import sqlite3
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import subprocess
from PIL import Image, ImageTk

GPIO.setwarnings(False)

class RFIDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CoE Library Management System (Home Page)")
        self.root.resizable(0, 0)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}")
        root.resizable(0, 0)

        self.reader = SimpleMFRC522()
        self.conn = sqlite3.connect("user_database.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                rfid_tag INTEGER PRIMARY KEY NOT NULL,
                first_name TEXT,
                last_name TEXT,
                student_id TEXT,
                course TEXT,
                mobile_number TEXT,
                email TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS restricted_users (
                rfid_tag INTEGER PRIMARY KEY NOT NULL,
                reason TEXT
            )
        ''')
        
        self.conn.commit()
        
        image = Image.open("bg.png")
        resized_image = image.resize((screen_width, screen_height))
        self.image = ImageTk.PhotoImage(resized_image)
        self.img = tk.Label(root, bg='#DAE3F3', image=self.image, anchor='center', )
        self.img.place(x=(screen_width - self.img.winfo_reqwidth()) / 2)
        
        self.id_var = tk.StringVar()
        self.id_entry = tk.Entry(root, textvariable=self.id_var, state="readonly", font=("Poppins", 14))
        self.id_entry.place(x=1233, y=675)
        
        self.signup_window_delay = 2000
        self.root.after(100, self.continuous_scan)
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    # Scan RFID
    def scan_rfid(self):
        id, _ = self.reader.read()
        self.id_var.set(str(id))
        self.check_user_in_database(str(id))
    
    # Open to Admin Page
    def open_lms_rfid(self):
        try:
            subprocess.run(["python", "lms_rfid.py"])
        except Exception as e:
            print(f"Error opening lms_rfid.py: {e}")
    
    # Open to User Page
    def open_user(self, user_data):
        try:
            subprocess.run(["python", "user.py", str(user_data[0]), user_data[1], user_data[2]])
        except Exception as e:
            print(f"Error opening user.py: {e}")
    
    # Continuous Scanning
    def continuous_scan(self):
        self.scan_rfid()
        self.root.after(100, self.continuous_scan)
    
    # Closing Window Form
    def on_closing(self):
        self.conn.close()
        self.root.destroy()
    
    # Check User if in Database (updated)
    def check_user_in_database(self, rfid_tag):   
        self.cursor.execute('SELECT * FROM restricted_users WHERE rfid_tag=?', (rfid_tag,))
        restricted_user_data = self.cursor.fetchone()
        
        self.cursor.execute('SELECT * FROM users WHERE rfid_tag=?', (rfid_tag,))
        user_data = self.cursor.fetchone()

        admin_rfid_tags = ["211051685533", "210749630126"] #Add RFID Tags for Admin Access

        if restricted_user_data:
            reason = restricted_user_data[1]
            messagebox.showinfo("Restricted User", f"You are restricted from using the app. User {user_data[0]}\n{user_data[1]} {user_data[2]}\n\nViolation: {reason}")
        else:
            if str(rfid_tag) in admin_rfid_tags:
                messagebox.showinfo("Admin", "Welcome, Admin!")
                self.open_lms_rfid()
            elif user_data:
                messagebox.showinfo("User Found", f"Welcome, {user_data[1]} {user_data[2]}!")
                self.open_user(user_data)
            else:
                signup_window_result = self.signup_window(rfid_tag)
                self.root.wait_window(signup_window_result)
    
    # SignUp Window
    def signup_window(self, rfid_tag):
        id, _ = self.reader.read()
        self.id_var.set(str(id))
        messagebox.showinfo("RFID Scanned", f"RFID Tag Scanned: {id} \n\nUSER NOT YET REGISTERED")
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Create Account")
        signup_window.configure(bg='#DAE3F3')

        # StringVar
        first_name_var = tk.StringVar()
        last_name_var = tk.StringVar()
        student_id_var = tk.StringVar()
        course_var = tk.StringVar()
        mobile_number_var = tk.StringVar()
        email_var = tk.StringVar()

        # SignUp Window UI
        tk.Label(signup_window, text="Create New Account", font=("Poppins", 12), bg='#DAE3F3').grid(row=5, column=1, columnspan=4, padx=15, pady=15)
        
        entry1 = tk.Entry(signup_window, textvariable=first_name_var, font=("Poppins", 14), relief="ridge")
        entry1.grid(row=6, column=1, padx=10, pady=10)
        label1 = tk.Label(signup_window, text="First Name", font=("Poppins", 10), justify="left", bg="white", fg="#767171")
        label1.grid(row=6, column=1, padx=15, pady=10, sticky="w")
        entry1.bind("<FocusIn>", lambda event: label1.place_forget() if entry1.get() else label1.place(x=1000, y=1000))

        entry2 = tk.Entry(signup_window, textvariable=last_name_var, font=("Poppins", 14), relief="ridge")
        entry2.grid(row=6, column=2, padx=10, pady=10)
        label2 = tk.Label(signup_window, text="Last Name", font=("Poppins", 10), justify="left", bg="white", fg="#767171")
        label2.grid(row=6, column=2, padx=15, pady=10, sticky="w")
        entry2.bind("<FocusIn>", lambda event: label2.place_forget() if entry2.get() else label2.place(x=1000, y=1000))
        
        entry3 = tk.Entry(signup_window, textvariable=student_id_var, font=("Poppins", 14), width=42, relief="ridge")
        entry3.grid(row=8, column=1, columnspan=2, padx=10, pady=10)
        label3 = tk.Label(signup_window, text="Student ID e.g. 0120-2XXX", font=("Poppins", 10), justify="left", bg="white", fg="#767171")
        label3.grid(row=8, column=1, padx=15, pady=10, sticky="w")
        entry3.bind("<FocusIn>", lambda event: label3.place_forget() if entry3.get() else label3.place(x=1000, y=1000))

        entry4 = tk.Entry(signup_window, textvariable=course_var, font=("Poppins", 14), width=42, relief="ridge")
        entry4.grid(row=9, column=1, columnspan=2, padx=10, pady=10)
        label4 = tk.Label(signup_window, text="Course and Section e.g. CpE 4C", font=("Poppins", 10), justify="left", bg="white", fg="#767171")
        label4.grid(row=9, column=1, padx=15, pady=10, sticky="w")
        entry4.bind("<FocusIn>", lambda event: label4.place_forget() if entry4.get() else label4.place(x=1000, y=1000))

        entry5 = tk.Entry(signup_window, textvariable=mobile_number_var, font=("Poppins", 14), width=42, relief="ridge")
        entry5.grid(row=10, column=1, columnspan=2, padx=10, pady=10)
        label5 = tk.Label(signup_window, text="Mobile Number", font=("Poppins", 10), justify="left", bg="white", fg="#767171")
        label5.grid(row=10, column=1, padx=15, pady=10, sticky="w")
        entry5.bind("<FocusIn>", lambda event: label5.place_forget() if entry5.get() else label5.place(x=1000, y=1000))
        
        entry6 = tk.Entry(signup_window, textvariable=email_var, font=("Poppins", 14), width=42, relief="ridge")
        entry6.grid(row=11, column=1, columnspan=2, padx=10, pady=10)
        label6 = tk.Label(signup_window, text="Email", font=("Poppins", 10), justify="left", bg="white", fg="#767171")
        label6.grid(row=11, column=1, padx=15, pady=10, sticky="w")
        entry6.bind("<FocusIn>", lambda event: label6.place_forget() if entry6.get() else label6.place(x=1000, y=1000))
        
        tk.Button(signup_window, text="Sign Up", command=lambda: self.save_user_info(rfid_tag, first_name_var.get(), last_name_var.get(),
                                                                                 student_id_var.get(), course_var.get(),
                                                                                 mobile_number_var.get(), email_var.get(),
                                                                                 signup_window),
                  font=("Poppins", 11)).grid(row=12, column=0, columnspan=4, pady=20)
        
        return signup_window
    
    # Save User Info to Database after SignUp Process
    def save_user_info(self, rfid_tag, first_name, last_name, student_id, course, mobile_number, email, signup_window):
        self.cursor.execute('''
            INSERT INTO users (rfid_tag, first_name, last_name, student_id, course, mobile_number, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (str(rfid_tag), first_name, last_name, student_id, course, mobile_number, email))
        self.conn.commit()
        signup_window.destroy()
        messagebox.showinfo("User Information Saved", "User information has been saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RFIDApp(root)
    root.configure(bg='#DAE3F3')    
    root.mainloop()