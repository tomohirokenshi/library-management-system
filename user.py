# Importing all necessary modules
import sqlite3
import sys
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
from tkinter import *
from mfrc522 import SimpleMFRC522
from tkinter import Tk, Label, Entry, StringVar, Button
from datetime import datetime, timedelta

# Connecting to Database
connector = sqlite3.connect('user_books.db')
cursor = connector.cursor()

connector.execute(
'CREATE TABLE IF NOT EXISTS User (USER_ID_VAR TEXT, STUDENT_NAME_VAR TEXT, BK_ID_VAR TEXT, BK_NAME_VAR TEXT, DATE_BORROWED TEXT, DUE_DATE_VAR TEXT, DATE_RETURNED TEXT, FEE TEXT, ID INTEGER PRIMARY KEY AUTOINCREMENT)'
)

# Inclusivity Function
if __name__ == "__main__":
    if len(sys.argv) == 4:
        user_id = sys.argv[1]
        first_name = sys.argv[2]
        last_name = sys.argv[3]

        print(f"User ID: {user_id}")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")

    else:
        print("Usage: python user.py <user_id> <first_name> <last_name>")
        
# Read RFID
def read_rfid():
    try: 
        book_connector = sqlite3.connect('library.db')
        book_cursor = book_connector.cursor()

        reader = SimpleMFRC522()

        # Use askquestion instead of showinfo
        user_response = mb.askquestion('Confirm Book RFID', 'Please scan the Book`s RFID card')

        if user_response == 'yes':
            bk_id, _ = reader.read()
            book_cursor.execute('SELECT BK_ID, BK_NAME FROM Library WHERE BK_ID = ?', (bk_id,))
            book_data = book_cursor.fetchone()
            if book_data:
                bk_id_var.set(book_data[0])
                bk_name_var.set(book_data[1])
            else:
                mb.showinfo('Book not found', 'The scanned RFID tag does not correspond to any book in the library.')
        else:
            pass

        book_connector.close()
    except Exception as e:
        mb.showerror('RFID Error', f'Error while reading RFID: {str(e)}')

# Display User Records
def display_records():
    global connector, cursor
    global tree

    tree.delete(*tree.get_children())

    try:
        cursor.execute('SELECT * FROM User WHERE USER_ID_VAR = ?', (user_id_var.get(),))
        data = cursor.fetchall()

        for record in data:
            tree.insert('', END, values=record)

    except Exception as e:
        print(f"Error displaying records: {str(e)}")

# Clear Fields
def clear_fields():
	global user_id_var, student_name_var, bk_id_var, bk_name_var, date_borrowed, due_date_var

	for i in ['bk_id_var', 'bk_name_var', 'date_borrowed', 'due_date_var', 'date_returned']:
		exec(f"{i}.set('')")
	try:
		tree.selection_remove(tree.selection()[0])
	except:
		pass

def clear_and_display():
    clear_fields()
    display_records()

# Function to highlight nearing due dates
def highlight_nearing_due_dates():
    today = datetime.today()
    overdue_threshold = today
    nearing_due_date_threshold = today + timedelta(days=2)

    for child in tree.get_children():
        due_date_str = tree.item(child, 'values')[5]  
        date_returned_str = tree.item(child, 'values')[6]

        due_date = datetime.strptime(due_date_str, "%m/%d/%Y") if due_date_str != "N/A" else None        

        if date_returned_str != 'None':
            tree.tag_configure('returned', background='#aaffaa')  
            tree.item(child, tags='returned')
        elif due_date and due_date < overdue_threshold:
            tree.tag_configure('nearing_due', background='#ffaaaa')  
            tree.item(child, tags='nearing_due')
        elif due_date and today < due_date <= nearing_due_date_threshold:
            tree.tag_configure('nearing_due', background='#ffcc99')  
            tree.item(child, tags='nearing_due')
        else:
            tree.tag_configure('nearing_due', background='white')

def check_due_dates_periodically():
    highlight_nearing_due_dates()
    root.after(1000, check_due_dates_periodically)

# Borrow Book Function
def borrow_book():
    global connector
    global user_id_var, student_name_var, bk_id_var, bk_name_var, date_borrowed, due_date_var
    
    current_date_time = datetime.now()
    date_format = "%m/%d/%Y"
    date_borrowed_str = current_date_time.strftime(date_format)
    date_borrowed.set(date_borrowed_str)

    try:
        borrowed_date = current_date_time
        due_date = borrowed_date + timedelta(days=5)
        due_date_str = due_date.strftime(date_format)
        due_date_var.set(due_date_str)

        read_rfid()
        surety = mb.askyesno('Are you sure?',
                            'Are you sure this is the data you want to enter?\nPlease note that the Book cannot be changed in the future')

        if surety:
            try:
                connector.execute(
                    'INSERT INTO User (USER_ID_VAR, STUDENT_NAME_VAR, BK_ID_VAR, BK_NAME_VAR, DATE_BORROWED, DUE_DATE_VAR) VALUES (?, ?, ?, ?, ?, ?)',
                    (user_id_var.get(), student_name_var.get(), bk_id_var.get(), bk_name_var.get(), date_borrowed.get(), due_date_var.get()))
                connector.commit()

                clear_and_display()

                mb.showinfo('Record added', 'The new record was successfully added to your database for book borrowing')
            except sqlite3.IntegrityError:
                mb.showerror('Book ID already in use!',
                            'The Book ID you are trying to enter is already in the database. Please choose another book.')
            except Exception as e:
                mb.showerror('Error adding record', f'Error: {str(e)}')
    except ValueError:
        due_date_var.set("Invalid Date")
        return
    
  # Repeat every 60 seconds (adjust as needed)

# Variables
lf_bg = 'LightSkyBlue'
rtf_bg = 'DeepSkyBlue'
rbf_bg = 'DodgerBlue'
btn_hlb_bg = 'SteelBlue'

lbl_font = ('Poppins', 13)
entry_font = ('Lato', 10)
btn_font = ('Poppins', 10)

# Initializing the Main GUI Window
root = Tk()
root.title('CoE Library Management System (User)')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(1, 1)

Label(root, text='LIBRARY MANAGEMENT SYSTEM', font=("Noto Sans CJK TC", 15, 'bold'), bg=btn_hlb_bg, fg='White').pack(side=TOP, fill=X)

# StringVars
user_id_var = StringVar()
student_name_var = StringVar()
user_id_var.set(sys.argv[1])
student_name_var.set(sys.argv[2] + " " + sys.argv[3])
bk_name_var = StringVar()
bk_id_var = StringVar()
date_borrowed = StringVar()
due_date_var = StringVar()
date_returned = StringVar()
fee = StringVar()

# Frames
left_frame = Frame(root, bg=lf_bg)
left_frame.place(x=0, y=30, relwidth=0.3, relheight=0.99)

RB_frame = Frame(root, bg=rtf_bg)
RB_frame.place(relx=0.19, y=30, relwidth=0.81, relheight=1.031)

# Left Frame
Label(left_frame, text="Borrowing Record", bg=lf_bg, font=('Poppins',15,'bold')).place(x=52, y=25)

Label(left_frame, text="User's ID", bg=lf_bg, font=lbl_font).place(x=105, y=65)
en1 = Entry(left_frame, width=25, font=entry_font, text=user_id_var, state='readonly')
en1.place(x=45, y=95)

Label(left_frame, text="Student's Name", bg=lf_bg, font=lbl_font).place(x=75, y=135)
en2 = Entry(left_frame, width=25, font=entry_font, text=student_name_var, state='readonly')
en2.place(x=45, y=165)

Label(left_frame, text='Book ID', bg=lf_bg, font=lbl_font).place(x=110, y=205)
bk_id_entry1 = Entry(left_frame, width=25, font=entry_font, text=bk_id_var, state='readonly')
bk_id_entry1.place(x=45, y=235)

Label(left_frame, text='Book Title', bg=lf_bg, font=lbl_font).place(x=100, y=275)
en3 = Entry(left_frame, width=25, font=entry_font, text=bk_name_var, state='readonly')
en3.place(x=45, y=305)

Label(left_frame, text='Date Borrowed', bg=lf_bg, font=lbl_font).place(x=80, y=345)
en4 = Entry(left_frame, width=25, font=entry_font, text=date_borrowed, state='readonly')
en4.place(x=45, y=375)

Label(left_frame, text='Due Date', bg=lf_bg, font=lbl_font).place(x=104, y=415)
en5 = Entry(left_frame, width=25, font=entry_font, text=due_date_var, state='readonly')
en5.place(x=45, y=445)

borrow = Button(left_frame, text='Borrow Book', font=btn_font, bg=btn_hlb_bg, width=19, command=borrow_book)
borrow.place(x=50, y=700)

# Right Bottom Frame
Label(RB_frame, text="BORROWER'S INVENTORY", bg=rbf_bg, font=("Noto Sans CJK TC", 15, 'bold')).pack(side=TOP, fill=X)

tree = ttk.Treeview(RB_frame, selectmode=BROWSE, columns=("User's ID", "Student's Name", 'Book ID', 'Book Title', 'Date Borrowed', 'Due Date', 'Date Returned', 'Fee'))

XScrollbar = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
YScrollbar = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
XScrollbar.pack(side=BOTTOM, fill=X)
YScrollbar.pack(side=RIGHT, fill=Y)

tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)

tree.heading("User's ID", text="User's ID", anchor=CENTER)
tree.heading("Student's Name", text="Student's Name", anchor=CENTER)
tree.heading('Book ID', text='Book ID', anchor=CENTER)
tree.heading('Book Title', text='Book Title', anchor=CENTER)
tree.heading('Date Borrowed', text='Date Borrowed', anchor=CENTER)
tree.heading('Due Date', text='Due Date', anchor=CENTER)
tree.heading('Date Returned', text='Date Returned', anchor=CENTER)
tree.heading('Fee', text='Fee', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=120, stretch=NO)
tree.column('#2', width=170, stretch=NO)
tree.column('#3', width=120, stretch=NO)
tree.column('#4', width=700, stretch=NO)
tree.column('#5', width=120, stretch=NO)
tree.column('#6', width=120, stretch=NO)
tree.column('#7', width=120, stretch=NO)
tree.column('#8', width=100, stretch=NO)

tree.place(y=30, x=0, relheight=0.9, relwidth=1)

display_records()
highlight_nearing_due_dates()
check_due_dates_periodically()
# Finalizing the Window
root.update()
root.mainloop()