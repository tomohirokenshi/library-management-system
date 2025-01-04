# Importing all necessary modules
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
import tkinter as tk
import shutil
import pandas as pd
from tkinter import *
from mfrc522 import SimpleMFRC522
from tkinter import simpledialog, Entry, PhotoImage, ttk, filedialog
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText

# Connecting to Database
connector = sqlite3.connect('library.db')
cursor = connector.cursor()

connector.execute(
'CREATE TABLE IF NOT EXISTS Library (BK_ID TEXT PRIMARY KEY NOT NULL, BK_NAME TEXT, AUTHOR_NAME TEXT, BK_DATE INT, BK_COURSE TEXT)'
)

user_connector = sqlite3.connect('user_database.db')
user_cursor = user_connector.cursor()

user_connector.execute(
'CREATE TABLE IF NOT EXISTS users (rfid_tag INTEGER PRIMARY KEY NOT NULL, first_name TEXT, last_name TEXT, student_id TEXT, course TEXT, mobile_number TEXT, email TEXT)'
)

user_connector.execute(
'CREATE TABLE IF NOT EXISTS restricted_users (rfid_tag INTEGER PRIMARY KEY NOT NULL, reason TEXT)'
)

inventory_connector = sqlite3.connect('user_books.db')
inventory_cursor = inventory_connector.cursor()

inventory_connector.execute(
'CREATE TABLE IF NOT EXISTS User (USER_ID_VAR TEXT, STUDENT_NAME_VAR TEXT, BK_ID_VAR TEXT, BK_NAME_VAR TEXT, DATE_BORROWED TEXT, DUE_DATE_VAR TEXT, DATE_RETURNED TEXT, FEE TEXT, ID INTEGER PRIMARY KEY AUTOINCREMENT)'
)

# Read RFID
def read_rfid():
    try:
        reader = SimpleMFRC522()
        mb.showinfo('Scan RFID', 'Please scan the RFID card')
        card_uid, _ = reader.read()
        bk_id.set(str(card_uid))
    except Exception as e:
        mb.showerror('RFID Error', f'Error while reading RFID: {str(e)}')

# Display Database_1
def display_records():
    global connector, cursor
    global tree

    tree.delete(*tree.get_children())
    
    curr = connector.execute('SELECT * FROM Library')
    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)

# Display Database_2
def display_user_database():
    global user_connector, user_cursor
    global tree_user_database
    
    tree_user_database.delete(*tree_user_database.get_children())

    curr = user_cursor.execute('SELECT * FROM users')
    data = curr.fetchall()

    for records in data:
        tree_user_database.insert('', END, values=records)

# Display Database_3
def display_inventory():
    global inventory_connector, inventory_cursor
    global tree_inventory
    
    tree_inventory.delete(*tree_inventory.get_children())

    curr = inventory_cursor.execute('SELECT * FROM User')
    data = curr.fetchall()

    for records in data:
        tree_inventory.insert('', END, values=records)

# Clear Database_1
def clear_fields():
    global bk_id, bk_name, author_name, bk_date, bk_course

    bk_course.set('Select Course')
    for i in ['bk_id', 'bk_name', 'author_name', 'bk_date']:
        exec(f"{i}.set('')")
        bk_id_entry.config(state='readonly')
    try:
        tree.selection_remove(tree.selection()[0])
    except:
        pass

# Clear Database_2
def clear_fields_2():
    global rfid_tag, first_name, last_name, student_id, course, mobile_number, email

    for i in ['rfid_tag', 'first_name', 'last_name', 'student_id', 'course', 'mobile_number', 'email']:
        exec(f"{i}.set('')")
        rfid_tag_entry.config(state='disable')
        entry_1.config(state='disable')
        entry_2.config(state='disable')
        entry_3.config(state='disable')
        entry_4.config(state='disable')
        entry_5.config(state='disable')
        entry_6.config(state='disable') 
    try:
        tree.selection_remove(tree.selection()[0])
    except:
        pass
    
# Clear Database_3    
def clear_fields_3():
    global user_id_var, student_name_var, bk_id_var, bk_name_var, date_borrowed, due_date_var, date_returned, fee

    for i in ['user_id_var', 'student_name_var', 'bk_id_var', 'bk_name_var', 'date_borrowed', 'due_date_var', 'date_returned', 'fee']:
        exec(f"{i}.set('')")
        en1.config(state='disable')
        en2.config(state='disable')
        en3.config(state='disable')
        en4.config(state='disable')
        en5.config(state='disable')
        en6.config(state='disable')
        en7.config(state='disable')
        bk_id_entry1.config(state='disable')
    try:
        tree.selection_remove(tree.selection()[0])
    except:
        pass

def clear_and_display():
    clear_fields()
    display_records()

def clear_and_display_2():
    clear_fields_2()
    display_user_database()
    
def clear_and_display_3():
    clear_fields_3()
    display_inventory()
    highlight_nearing_due_dates()

# Add Database_1
def add_record():
    global connector
    global bk_name, bk_id, author_name, bk_course, bk_date
    
    read_rfid()

    surety = mb.askyesno('Are you sure?',
                'Are you sure this is the data you want to enter?\nPlease note that Book ID cannot be changed in the future')

    if surety:
        try:
            connector.execute(
            'INSERT INTO Library (BK_ID, BK_NAME, AUTHOR_NAME, BK_DATE, BK_COURSE) VALUES (?, ?, ?, ?, ?)',
                (bk_id.get(), bk_name.get(), author_name.get(), bk_date.get(), bk_course.get()))
            connector.commit()

            clear_and_display()

            mb.showinfo('Record added', 'The new record was successfully added to your database')
        except sqlite3.IntegrityError:
            mb.showerror('Book ID already in use!', 'The Book ID you are trying to enter is already in the database, please alter that book\'s record or check any discrepancies on your side')

# View Database_1
def view_record():
    global bk_id, bk_name, author_name, bk_date, bk_course
    global tree

    if not tree.focus():
        mb.showerror('Error!', 'Please select an item from the database')
        edit.place_forget()
        return

    current_item_selected = tree.focus()
    values_in_selected_item = tree.item(current_item_selected)
    selection = values_in_selected_item['values']

    bk_id.set(selection[0]) ;
    bk_name.set(selection[1]) ;
    author_name.set(selection[2]) ;
    bk_date.set(selection[3]) ;
    bk_course.set(selection[4]) ;

# Update Database_1
def update_record():
    def update():
        global bk_id, bk_name, author_name, bk_date, bk_course
        global connector, tree

        cursor.execute('UPDATE Library SET BK_NAME=?, AUTHOR_NAME=?, BK_DATE=?, BK_COURSE=? WHERE BK_ID=?',
                       (bk_name.get(), author_name.get(), bk_date.get(), bk_course.get(), bk_id.get()))
        connector.commit()
        
        clear_and_display()

        bk_id_entry.config(state='readonly')
        submit.place(x=50, y=700)
        clear.place(x=50, y=650)
        edit.place_forget()
        
    view_record()

    bk_id_entry.config(state='readonly')
    submit.place_forget()
    clear.place_forget()

    edit = Button(left_frame_b, text='Update Record', font=btn_font, bg=btn_hlb_bg, width=19, command=update)
    edit.place(x=50, y=700)

# Remove a Record Database_1
def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
        return

    confirm = mb.askyesno('Confirmation', 'Are you sure you want to delete this record?')

    if not confirm:
        return

    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]

    cursor.execute('DELETE FROM Library WHERE BK_ID=?', (selection[0],))
    connector.commit()

    tree.delete(current_item)

    mb.showinfo('Done', 'Record Deleted Successfully')

    clear_and_display()

# Remove All of Database_1
def delete_inventory():
    if mb.askyesno('Are you sure?', 'Are you sure you want to delete the entire inventory?\n\nThis command is irreversible'):
        tree.delete(*tree.get_children())
        mb.showinfo('Done', 'Whole Record Deleted Successfully')
        cursor.execute('DELETE FROM Library')
        connector.commit()
    else:
        return

# View Database_2
def view_users():
    global rfid_tag, first_name, last_name, student_id, course, mobile_number, email
    global tree_user_database

    if not tree_user_database.focus():
        mb.showerror('Error!', 'Please select an item from the database')
        edit1.place_forget()
        return

    current_item_selected = tree_user_database.focus()
    values_in_selected_item = tree_user_database.item(current_item_selected)
    selection = values_in_selected_item['values']

    rfid_tag.set(selection[0]) ;
    first_name.set(selection[1]) ;
    last_name.set(selection[2]) ;
    student_id.set(selection[3]) ;
    course.set(selection[4]) ;
    mobile_number.set(selection[5]) ;
    email.set(selection[6]) ;

# Update Database_2
def update_user_info():
    def update_user():
        global rfid_tag, first_name, last_name, student_id, course, mobile_number, email
        global user_connector, tree_user_database

        user_cursor.execute('UPDATE users SET first_name=?, last_name=?, student_id=?, course=?, mobile_number=?, email=? WHERE rfid_tag=?',
                       (first_name.get(), last_name.get(), student_id.get(), course.get(), mobile_number.get(), email.get(), rfid_tag.get()))
        user_connector.commit()
        
        clear_and_display_2()
    
        rfid_tag_entry.config(state='disable')
        edit1.place_forget()
        
    view_users()
    
    entry_1.config(state='normal')
    entry_2.config(state='normal')
    entry_3.config(state='normal')
    entry_4.config(state='normal')
    entry_5.config(state='normal')
    entry_6.config(state='normal') 
    rfid_tag_entry.config(state='disable')
    
    edit1 = Button(left_frame_u, text='Update Profile', font=btn_font, bg=btn_hlb_bg, width=19, command=update_user)
    edit1.place(x=50, y=700)

# Remove a User Database_2
def remove_user():
    if not tree_user_database.selection():
        mb.showerror('Error!', 'Please select an item from the database')
        return

    confirm = mb.askyesno('Confirmation', 'Are you sure you want to delete this record?')

    if not confirm:
        return

    current_item = tree_user_database.focus()
    values = tree_user_database.item(current_item)
    selection = values["values"]

    user_cursor.execute('DELETE FROM users WHERE rfid_tag=?', (selection[0],))
    user_cursor.execute('DELETE FROM restricted_users WHERE rfid_tag=?', (selection[0],))
    user_connector.commit()

    tree_user_database.delete(current_item)

    mb.showinfo('Done', 'Record Deleted Successfully')

    clear_and_display()

# Remove All of Database_2
def remove_inventory():
    if not tree_inventory.selection():
        mb.showerror('Error!', 'Please select an item from the database')
        return

    confirm = mb.askyesno('Confirmation', 'Are you sure you want to delete this record?')

    if not confirm:
        return

    current_item = tree_inventory.focus()
    values = tree_inventory.item(current_item)
    selection = values["values"]
    
    record_id = selection[8]

    inventory_cursor.execute('DELETE FROM User WHERE id=?',
                             (record_id,))
    inventory_connector.commit()

    tree_inventory.delete(current_item)

    mb.showinfo('Done', 'Record Deleted Successfully')

    clear_and_display_3()

# Remove a Record Database_3
def delete_borrower():
    if mb.askyesno('Are you sure?', 'Are you sure you want to delete the entire inventory?\n\nThis command is irreversible'):
        tree_inventory.delete(*tree_inventory.get_children())
        mb.showinfo('Done', 'Whole Record Deleted Successfully')
        inventory_cursor.execute('DELETE FROM User')
        inventory_connector.commit()
    else:
        return

# Filter Database_1
def filter_book_inventory(search_query):
    global connector, cursor
    global tree

    tree.delete(*tree.get_children())

    sorting_option = sorting_var.get()
    
    if sorting_option == "Book ID":
        query = "SELECT * FROM Library ORDER BY BK_ID"
    elif sorting_option == "Title":
        query = "SELECT * FROM Library ORDER BY BK_NAME"
    elif sorting_option == "Author":
        query = "SELECT * FROM Library ORDER BY AUTHOR_NAME"
    elif sorting_option == "Date":
        query = "SELECT * FROM Library ORDER BY BK_DATE"
    elif sorting_option == "Course":
        query = "SELECT * FROM Library ORDER BY BK_COURSE"
    else:
        query = "SELECT * FROM Library"

    curr = cursor.execute(query)
    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)

# Search Database_1
def search_book_inventory():
    global connector, cursor
    global tree

    tree.delete(*tree.get_children())

    search_query = search_book_entry.get().strip().lower()

    if not search_query:
        curr = cursor.execute("SELECT * FROM Library")
    else:
        curr = cursor.execute("""
            SELECT * FROM Library 
            WHERE LOWER(BK_ID) LIKE ? OR LOWER(BK_NAME) LIKE ? OR LOWER(AUTHOR_NAME) LIKE ?
            OR CAST(BK_DATE AS TEXT) LIKE ? OR LOWER(BK_COURSE) LIKE ?
        """,
            ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%',
             '%' + search_query + '%', '%' + search_query + '%'))

    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)

# Filter Database_2
def filter_user_database(event=None):
    global user_connector, user_cursor
    global tree_user_database

    tree_user_database.delete(*tree_user_database.get_children())

    user_sorting_option = user_sorting_var.get()

    if user_sorting_option == "RFID Tag":
        query = "SELECT * FROM users ORDER BY rfid_tag"
    elif user_sorting_option == "First Name":
        query = "SELECT * FROM users ORDER BY first_name"
    elif user_sorting_option == "Last Name":
        query = "SELECT * FROM users ORDER BY last_name"
    elif user_sorting_option == "Student ID":
        query = "SELECT * FROM users ORDER BY student_id"
    elif user_sorting_option == "Course":
        query = "SELECT * FROM users ORDER BY course"
    elif user_sorting_option == "Mobile Number":
        query = "SELECT * FROM users ORDER BY mobile_number"
    elif user_sorting_option == "Email":
        query = "SELECT * FROM users ORDER BY email"
    else:
        query = "SELECT * FROM users"

    curr = user_cursor.execute(query)
    data = curr.fetchall()

    for records in data:
        tree_user_database.insert('', END, values=records)

# Search Database_2
def search_user(event=None):
    global user_connector, user_cursor
    global tree_user_database

    tree_user_database.delete(*tree_user_database.get_children())

    search_query = search_user_entry.get().strip().lower()

    if not search_query:
        curr = user_cursor.execute("SELECT * FROM users")
    else:
        curr = user_cursor.execute("""
            SELECT * FROM users 
            WHERE LOWER(rfid_tag) LIKE ? OR LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?
            OR LOWER(student_id) LIKE ? OR LOWER(course) LIKE ? OR LOWER(mobile_number) LIKE ?
            OR LOWER(email) LIKE ?
        """,
            ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%',
             '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%',
             '%' + search_query + '%'))

    data = curr.fetchall()

    for records in data:
        tree_user_database.insert('', END, values=records)

# Filter Database_3
def filter_inventory(event=None):
    global inventory_connector, inventory_cursor
    global tree_inventory

    tree_inventory.delete(*tree_inventory.get_children())

    inventory_sorting_option = inventory_sorting_var.get()

    if inventory_sorting_option == "Student's ID":
        query = "SELECT * FROM User ORDER BY user_id_var"
    elif inventory_sorting_option == "Student's Name":
        query = "SELECT * FROM User ORDER BY student_name_var"
    elif inventory_sorting_option == "Book ID":
        query = "SELECT * FROM User ORDER BY bk_id_var"
    elif inventory_sorting_option == "Book Title":
        query = "SELECT * FROM User ORDER BY bk_name_var"
    elif inventory_sorting_option == "Date Borrowed":
        query = "SELECT * FROM User ORDER BY date_borrowed"
    elif inventory_sorting_option == "Due Date":
        query = "SELECT * FROM User ORDER BY due_date_var"
    elif inventory_sorting_option == "Date Returned":
        query = "SELECT * FROM User ORDER BY date_returned"
    elif inventory_sorting_option == "Fee":
        query = "SELECT * FROM User ORDER BY fee"
    else:
        query = "SELECT * FROM User"

    curr = inventory_cursor.execute(query)
    data = curr.fetchall()

    for records in data:
        tree_inventory.insert('', END, values=records)

# Search Database_3
def search_inventory(event=None):
    global inventory_connector, inventory_cursor
    global tree_inventory

    tree_inventory.delete(*tree_inventory.get_children())

    search_query = search_inventory_entry.get().strip().lower()

    if not search_query:
        curr = inventory_cursor.execute("SELECT * FROM User")
    else:
        curr = inventory_cursor.execute("""
            SELECT * FROM User 
            WHERE LOWER(user_id_var) LIKE ? OR LOWER(student_name_var) LIKE ? OR LOWER(bk_id_var) LIKE ?
            OR LOWER(bk_name_var) LIKE ? OR LOWER(date_borrowed) LIKE ? OR LOWER(due_date_var) LIKE ?
            OR LOWER(date_returned) LIKE ? OR LOWER(fee) LIKE ?
        """,
            ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%',
             '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%',
             '%' + search_query + '%', '%' + search_query + '%'))

    data = curr.fetchall()

    for records in data:
        tree_inventory.insert('', END, values=records)

#email notif
def remind_borrower():
    global user_connector, user_cursor
    global inventory_connector, inventory_cursor
    global tree_user_database

    if not tree_user_database.focus():
        mb.showerror('Error!', 'Please select an item from the database')
        return
    
    current_selected_item = tree_user_database.focus()
    values_in_selected_item = tree_user_database.item(current_selected_item)
    selection = values_in_selected_item['values']
    
    email = selection[6]
    first_name = selection[1]
    last_name = selection[2]
    course_section = selection[4]
    rfid_tag = selection[0]

    # Get borrowed book details with date_returned = "None"
    inventory_cursor.execute("SELECT BK_NAME_VAR, DATE_BORROWED, DUE_DATE_VAR FROM User WHERE USER_ID_VAR = ? AND DATE_RETURNED IS NULL", (rfid_tag,))
    borrowed_books = inventory_cursor.fetchall()
    
    if not borrowed_books:
        mb.showinfo("No Borrowed Books", "No books are currently borrowed by the selected user.")
        return

    reminder_message = f"Reminder from COE Library Management System,\n\n{first_name} {last_name} - {course_section},\n"
    reminder_message += f"You have books nearing their due date.\n\nBorrowed Book Details:\n"

    for book in borrowed_books:
        book_name, date_borrowed, due_date = book
        reminder_message += f"Book Name: {book_name}\n"
        reminder_message += f"Date Borrowed: {date_borrowed}\n"
        reminder_message += f"Due Date: {due_date}\n\n"

    reminder_message += f"Please return them on or before the due date.\n\nBest regards,\nThe COE Library Management"

    # Send an email
    try:
        sender_email = "raffy.hular@gmail.com"
        sender_password = "ktla egso fwit blzc"

        msg = MIMEText(reminder_message)
        msg["Subject"] = "Book Due Date Reminder"
        msg["From"] = sender_email
        msg["To"] = email

        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        server.login(sender_email, sender_password)

        server.sendmail(sender_email, [email], msg.as_string())
        server.quit()
        mb.showinfo("Email Sent", "Reminder email sent successfully!")

    except Exception as e:
        mb.showerror("Error", f"Error sending email: {e}")

# Restrict/Unrestrict Function
def restrict_unrestrict_user():
    global rfid_tag, user_connector, user_cursor
    global tree_user_database

    if not tree_user_database.focus():
        mb.showerror('Error!', 'Please select an item from the database')
        return

    current_item_selected = tree_user_database.focus()
    values_in_selected_item = tree_user_database.item(current_item_selected)
    selection = values_in_selected_item['values']

    rfid_tag_to_restrict = selection[0]

    user_cursor.execute('SELECT * FROM restricted_users WHERE rfid_tag=?', (rfid_tag_to_restrict,))
    already_restricted = user_cursor.fetchone()

    confirm = mb.askyesno('Confirmation', f'Are you sure you want to restrict/unrestrict user with RFID tag: {rfid_tag_to_restrict}?')

    if not confirm:
        return

    try:
        if already_restricted:
            user_cursor.execute('DELETE FROM restricted_users WHERE rfid_tag=?', (rfid_tag_to_restrict,))
            message = f'The user with RFID tag {rfid_tag_to_restrict} has been unrestricted successfully.'
        else:
            reason = sd.askstring('Reason for Restriction', 'Enter the reason for restriction:')
            if reason is None:
                return

            user_cursor.execute('INSERT INTO restricted_users (rfid_tag, reason) VALUES (?, ?)', (rfid_tag_to_restrict, reason))
            message = f'The user with RFID tag {rfid_tag_to_restrict} has been restricted successfully.\nReason: {reason}'

        user_connector.commit()

        clear_and_display_2()

        mb.showinfo('Success', message)
    except Exception as e:
        mb.showerror('Error', f'Error updating user restriction status: {str(e)}')

# Show Restricted Users
def show_restricted_users():
    user_cursor.execute('SELECT rfid_tag, reason FROM restricted_users')
    restricted_data = user_cursor.fetchall()

    if restricted_data:
        window = tk.Toplevel()
        window.title('Restricted Users')

        tree = ttk.Treeview(window)
        tree['columns'] = ('RFID Tag', 'User', 'Violation')
        tree.column('#0', width=0, stretch=NO)
        tree.heading('RFID Tag', text='RFID Tag')
        tree.heading('User', text='User')
        tree.heading('Violation', text='Violation')

        for row in restricted_data:
            rfid_tag = row[0]
            reason = row[1]

            user_cursor.execute('SELECT first_name, last_name FROM users WHERE rfid_tag=?', (rfid_tag,))
            user_info = user_cursor.fetchone()

            if user_info:
                first_name, last_name = user_info
                user_details = f"{first_name} {last_name}"
            else:
                user_details = "Unknown User"

            tree.insert('', 'end', values=(rfid_tag, user_details, reason))

        tree.pack(expand=True, fill='both')
    else:
        mb.showinfo('Restricted Users', 'No users are currently restricted.')

# Export Function
def export_database(selected_database):
    filename_db = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database Files", "*.db")])
    filename_excel = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

    if filename_db:
        if selected_database == "Book Inventory":
            shutil.copyfile('library.db', filename_db)
            print("Library database exported to", filename_db)
        elif selected_database == "User Management":
            shutil.copyfile('user_database.db', filename_db)
            print("User Database exported to", filename_db)
        elif selected_database == "Borrower's Inventory":
            shutil.copyfile('user_books.db', filename_db)
            print("User Database exported to", filename_db) 

    if filename_excel:
        if selected_database == "Book Inventory":
            with sqlite3.connect('library.db') as conn:
                query = "SELECT * FROM Library"
                df = pd.read_sql_query(query, conn)
                df.to_excel(filename_excel, index=False)
                print("Library database exported to", filename_excel)
        elif selected_database == "User Management":
            with sqlite3.connect('user_database.db') as conn:
                query_1 = "SELECT * FROM users"
                query_2 = "SELECT * FROM restricted_users"
                df_1 = pd.read_sql_query(query_1, conn)
                df_2 = pd.read_sql_query(query_2, conn)
                with pd.ExcelWriter(filename_excel, engine='xlsxwriter') as writer:
                    df_1.to_excel(writer, sheet_name='Users', index=False)
                    df_2.to_excel(writer, sheet_name='Restricted Users', index=False)
                print("User Database exported to", filename_excel)
        elif selected_database == "Borrower's Inventory":
            with sqlite3.connect('user_books.db') as conn:
                query = "SELECT * FROM User"
                df = pd.read_sql_query(query, conn)
                df.to_excel(filename_excel, index=False)
                print("User Database exported to", filename_excel)

# Import Function
def import_database(selected_database):
    filename = filedialog.askopenfilename(defaultextension=".db", filetypes=[("SQLite Database Files", "*.db")])
    if filename:
        if selected_database == "Book Inventory":
            with sqlite3.connect(filename) as import_conn:
                import_cursor = import_conn.cursor()
                import_cursor.execute("SELECT * FROM Library")
                data_to_import = import_cursor.fetchall()
                with sqlite3.connect('library.db') as export_conn:
                    export_cursor = export_conn.cursor()
                    export_cursor.executemany("INSERT INTO Library VALUES (?, ?, ?, ?, ?)", data_to_import)
                print("Library database imported successfully.")
        elif selected_database == "User Management":
            with sqlite3.connect(filename) as import_conn:
                import_cursor = import_conn.cursor()
                import_cursor.execute("SELECT * FROM users")
                data_to_import = import_cursor.fetchall()
                with sqlite3.connect('user_database.db') as export_conn:
                    export_cursor = export_conn.cursor()
                    export_cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", data_to_import)
                print("User Database imported successfully.")
        elif selected_database == "Borrower's Inventory":
            with sqlite3.connect(filename) as import_conn:
                import_cursor = import_conn.cursor()
                import_cursor.execute("SELECT * FROM User")
                data_to_import = import_cursor.fetchall()
                with sqlite3.connect('user_books.db') as export_conn:
                    export_cursor = export_conn.cursor()
                    export_cursor.executemany("INSERT INTO User VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data_to_import)
                print("User Database imported successfully.")

# Import/Export Buttons
def on_combobox_selected(event):
    selected_database = combobox.get()
    export_button.configure(state="normal", command=lambda: export_database(selected_database))
    import_button.configure(state="normal", command=lambda: import_database(selected_database))

# View Database_3
def view_borrow():
    global user_id_var, student_name_var, bk_id_var, bk_name_var, date_borrowed, due_date_var, date_returned, fee
    global tree_inventory

    if not tree_inventory.focus():
        mb.showerror('Error!', 'Please select an item from the database')
        edit3.place_forget()
        return
    

    current_item_selected = tree_inventory.focus()
    values_in_selected_item = tree_inventory.item(current_item_selected)
    selection = values_in_selected_item['values']

    user_id_var.set(selection[0]) ;
    student_name_var.set(selection[1]) ;
    bk_id_var.set(selection[2]) ;
    bk_name_var.set(selection[3]) ;
    date_borrowed.set(selection[4]) ;
    due_date_var.set(selection[5]) ;
    date_returned.set(selection[6]) ;
    fee.set(selection[7]) ;

# Function to highlight nearing due dates
def highlight_nearing_due_dates():
    today = datetime.today()
    overdue_threshold = today
    nearing_due_date_threshold = today + timedelta(days=2)  

    for child in tree_inventory.get_children():
        due_date_str = tree_inventory.item(child, 'values')[5]  
        date_returned_str = tree_inventory.item(child, 'values')[6]

        due_date = datetime.strptime(due_date_str, "%m/%d/%Y")	 if due_date_str != "N/A" else None        

        if date_returned_str != 'None':
            tree_inventory.tag_configure('returned', background='#aaffaa')  
            tree_inventory.item(child, tags='returned')
        elif due_date and due_date < overdue_threshold:
            tree_inventory.tag_configure('nearing_due', background='#ffaaaa')  
            tree_inventory.item(child, tags='nearing_due')
        elif due_date and today < due_date <= nearing_due_date_threshold:
            tree_inventory.tag_configure('nearing_due', background='#ffcc99')  
            tree_inventory.item(child, tags='nearing_due')
        else:
            tree_inventory.tag_configure('nearing_due', background='white')

def check_due_dates_periodically():
    highlight_nearing_due_dates()
    root.after(1000, check_due_dates_periodically) # set to 86400 second to check everyday 

# Return Book Function
def return_book():
    def return_b():
        global user_id_var, student_name_var, bk_id_var, bk_name_var, date_borrowed, due_date_var, date_returned, fee, id
        global inventory_connector, tree_inventory
        
        current_item = tree_inventory.focus()
        values = tree_inventory.item(current_item)
        selection = values["values"]
        record_id = selection[8]
        
        current_date_time = datetime.now()
        date_format = "%m/%d/%Y"
        date_returned_str = current_date_time.strftime(date_format)
        date_returned.set(date_returned_str)
        due_date_str = due_date_var.get()
        due_date = datetime.strptime(due_date_str, date_format)
        
        try:
            days_overdue = max(0, (current_date_time - due_date).days)
            fee_value = days_overdue * 2
            days_overdue_var.set(days_overdue)
            fee.set(fee_value)

            inventory_cursor.execute('UPDATE User SET user_id_var=?, student_name_var=?, bk_id_var=?, bk_name_var=?, date_borrowed=?, due_date_var=?, date_returned=?, fee=? WHERE ID=?',
                                     (user_id_var.get(), student_name_var.get(), bk_id_var.get(), bk_name_var.get(), date_borrowed.get(), due_date_var.get(), date_returned.get(), fee_value, record_id))
            inventory_connector.commit()
            mb.showinfo('Returning Book', "This will be returned and user's book status will change")

            clear_and_display_3()
        except ValueError:
            days_overdue_var.set("Invalid Date")
            fee.set("Invalid Date")
    
    view_borrow()
    confirm = mb.askyesno('Confirmation', 'Are you sure you want to return this book?')

    if not confirm:
        return
    returned_date = date_returned.get()
    if returned_date is not None and returned_date != 'None':
        mb.showerror('Error!', 'This Book is already returned!')
        return
    else:
        return_b()

    en1.config(state='readonly')
    en2.config(state='readonly')
    en3.config(state='readonly')
    en4.config(state='readonly')
    en5.config(state='readonly')
    en6.config(state='readonly')
    en7.config(state='readonly')
    bk_id_entry1.config(state='readonly')

# Switch to Database_1
def switch_to_user_database():
    RB_frame_inventory.pack_forget()
    RB_frame_borrower.pack_forget()
    RB_frame_user_database.pack(side=RIGHT, fill=BOTH, expand=YES)
    display_user_database()
    
    for widget in RT_frame.winfo_children():
        if widget['text'] in ['Delete Book Record', 'Delete Full Inventory', 'Delete Borrowing Record', 'Update Book Details', 'Return Book', 'Delete All Record']:
            widget.place_forget()
            
    for widget in RT_frame.winfo_children():
        if widget['text'] in ['User Management']:
            widget.config(state='disable')
            
    for widget in RT_frame.winfo_children():
        if widget['text'] in ['Book Inventory', "Borrower's Inventory"]:
            widget.config(state='normal')
            
    Button(RT_frame, text='Update User Information', font=btn_font, bg=btn_hlb_bg, width=20, command=update_user_info, padx=5).place(x=94, y=15)
    Button(RT_frame, text='Remove User', font=btn_font, bg=btn_hlb_bg, width=11, command=remove_user, padx=5).place(x=320, y=15)
    Button(RT_frame, text='Restrict/Unrestrict User', font=btn_font, bg=btn_hlb_bg, width=17, command=restrict_unrestrict_user).place(x=465, y=15)
    Button(RT_frame, text='Show Restricted Users', font=btn_font, bg=btn_hlb_bg, width=16, command=show_restricted_users).place(x=675	, y=15)
    Button(RT_frame, text='Due Date Reminders', font=btn_font, bg=btn_hlb_bg, width=15, command=remind_borrower).place(x=880, y=15)
    
    left_frame_u.place(x=0, y=30, relwidth=0.3, relheight=0.96)
    left_frame_b.place_forget()
    left_frame_i.place_forget()
    clear_and_display_2()

# Switch to Database_2
def switch_to_book_inventory():
    RB_frame_user_database.pack_forget()
    RB_frame_borrower.pack_forget()
    RB_frame_inventory.pack(side=RIGHT, fill=BOTH, expand=YES)
    display_records()
    
    for widget in RT_frame.winfo_children():
        if widget['text'] in ['Due Date Reminders','Show Restricted Users', 'Restrict/Unrestrict User', 'Delete Borrowing Record', 'Update User Information', 'Remove User', 'Return Book', 'Delete All Record']:
            widget.place_forget()
            
    for widget in RT_frame.winfo_children():
        if widget['text'] in ['Book Inventory']:
            widget.config(state='disable')
            
    for widget in RT_frame.winfo_children():
        if widget['text'] in ['User Management', "Borrower's Inventory"]:
            widget.config(state='normal')
            
    Button(RT_frame, text='Update Book Details', font=btn_font, bg=btn_hlb_bg, width=17, command=update_record, padx=5).place(x=286, y=15)
    Button(RT_frame, text='Delete Book Record', font=btn_font, bg=btn_hlb_bg, width=16, command=remove_record, padx=5).place(x=485, y=15)
    Button(RT_frame, text='Delete Full Inventory', font=btn_font, bg=btn_hlb_bg, width=17, command=delete_inventory, padx=5).place(x=677, y=15)
    
    left_frame_u.place_forget()
    left_frame_b.place(x=0, y=30, relwidth=0.3, relheight=0.96)
    left_frame_i.place_forget()
    clear_and_display()

# Switch to Database_3
def switch_to_borrower_inventory():
    RB_frame_user_database.pack_forget()
    RB_frame_borrower.pack(side=RIGHT, fill=BOTH, expand=YES)
    RB_frame_inventory.pack_forget()
    display_inventory()
    
    for widget in RT_frame.winfo_children():
        if widget['text'] in ['Due Date Reminders','Show Restricted Users', 'Restrict/Unrestrict User', 'Update User Information', 'Remove User', 'Delete Book Record', 'Delete Full Inventory', 'Update Book Details']:
            widget.place_forget()
            
    for widget in RT_frame.winfo_children():
        if widget['text'] in ["Borrower's Inventory"]:
            widget.config(state='disable')
            
    for widget in RT_frame.winfo_children():
        if widget['text'] in ['User Management', "Book Inventory"]:
            widget.config(state='normal')
    
    Button(RT_frame, text='Return Book', font=btn_font, bg=btn_hlb_bg, width=11, command=return_book, padx=5).place(x=306, y=15)
    Button(RT_frame, text='Delete Borrowing Record', font=btn_font, bg=btn_hlb_bg, width=20, command=remove_inventory, padx=5).place(x=454, y=15)
    Button(RT_frame, text='Delete All Record', font=btn_font, bg=btn_hlb_bg, width=14, command=delete_borrower, padx=5).place(x=683, y=15)
    
    left_frame_u.place_forget()
    left_frame_b.place_forget()
    left_frame_i.place(x=0, y=30, relwidth=0.3, relheight=0.96)
    clear_and_display_3()
    
# Variables
lf_bg = 'LightSkyBlue'
rtf_bg = 'DodgerBlue'
rbf_bg = 'DeepSkyBlue'
btn_hlb_bg = 'SteelBlue'
#DodgerBlue
lbl_font = ('Poppins', 13)
entry_font = ('Lato', 10)
btn_font = ('Poppins', 10)

# Initializing the Main GUI Window
root = Tk()
root.title('CoE Library Management System (Admin)')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(0, 0)

Label(root, text='LIBRARY MANAGEMENT SYSTEM', font=("Noto Sans CJK TC", 15, 'bold'), bg='#c45103', fg='White').pack(side=TOP, fill=X)

# StringVars for Book Inventory
bk_name = StringVar()
bk_id = StringVar()
author_name = StringVar()
bk_course = StringVar()
bk_date = StringVar()

#StringVars for User Management
rfid_tag = StringVar()
first_name = StringVar()
last_name = StringVar()
student_id = StringVar()
course = StringVar()
mobile_number = StringVar()
email = StringVar()

#StringVars for Borrower's Inventory
user_id_var = StringVar()
student_name_var = StringVar()
bk_name_var = StringVar()
bk_id_var = StringVar()
date_borrowed = StringVar()
due_date_var = StringVar()
date_returned = StringVar()
days_overdue_var = StringVar()
fee = StringVar()

# Frames
left_frame_def = Frame(root, bg=lf_bg)
left_frame_def.place(x=0, y=30, relwidth=0.3, relheight=0.96)

left_frame_b = Frame(root, bg=lf_bg)

left_frame_u = Frame(root, bg=lf_bg)

left_frame_i = Frame(root, bg=lf_bg)

RT_frame = Frame(root, bg=rtf_bg)
RT_frame.place(relx=0.19, y=30, relheight=0.15, relwidth=0.81)

RB_frame = Frame(root, bd=1, relief="flat", borderwidth=1)
RB_frame.place(relx=0.19, y=125, relheight=0.84, relwidth=0.81)

# Left Frame (Default)
image = Image.open("COE.png")
resized_image = image.resize((310, 800))
image1 = ImageTk.PhotoImage(resized_image)
img = tk.Label(left_frame_def, bg=lf_bg, image=image1, anchor='center', )
img.place(x=0, y=0)

# Left Frame for Book Inventory
Label(left_frame_b, text='Book Details', bg=lf_bg, font=('Poppins',15,'bold')).place(x=78, y=25)

Label(left_frame_b, text='Book ID', bg=lf_bg, font=lbl_font).place(x=110, y=65)
bk_id_entry = Entry(left_frame_b, width=25, font=entry_font, text=bk_id, state='readonly')
bk_id_entry.place(x=45, y=95)

Label(left_frame_b, text='Title', bg=lf_bg, font=lbl_font).place(x=125, y=135)
Entry(left_frame_b, width=25, font=entry_font, text=bk_name).place(x=45, y=165)

Label(left_frame_b, text='Author', bg=lf_bg, font=lbl_font).place(x=115, y=205)
Entry(left_frame_b, width=25, font=entry_font, text=author_name).place(x=45, y=235)

Label(left_frame_b, text='Date', bg=lf_bg, font=lbl_font).place(x=124, y=275)
Entry(left_frame_b, width=25, font=entry_font, text=bk_date).place(x=45, y=305)

Label(left_frame_b, text='Course', bg=lf_bg, font=lbl_font).place(x=115, y=345)
dd1 = OptionMenu(left_frame_b, bk_course, *['Civil Engineering', 'Computer Engineering', 'Electrical Engineering', 'Electronics Engineering', 'Mechanical Engineering'])
dd1.configure(font=entry_font, width=20)
dd1.place(x=45, y=375)

submit = Button(left_frame_b, text='Add New Record', font=btn_font, bg=btn_hlb_bg, width=19, command=add_record)
submit.place(x=50, y=700)

clear = Button(left_frame_b, text='Clear Fields', font=btn_font, bg=btn_hlb_bg, width=19, command=clear_fields)
clear.place(x=50, y=650)

# Left Frame for User Management
Label(left_frame_u, text='User Information', bg=lf_bg, font=('Poppins',15,'bold')).place(x=59, y=25)

Label(left_frame_u, text='RFID Tag', bg=lf_bg, font=lbl_font).place(x=106, y=65)
rfid_tag_entry = Entry(left_frame_u, width=25, font=entry_font, text=rfid_tag)
rfid_tag_entry.place(x=45, y=95)

Label(left_frame_u, text='First Name', bg=lf_bg, font=lbl_font).place(x=98, y=135)
entry_1 = Entry(left_frame_u, width=25, font=entry_font, text=first_name)
entry_1.place(x=45, y=165)

Label(left_frame_u, text='Last Name', bg=lf_bg, font=lbl_font).place(x=101, y=205)
entry_2 = Entry(left_frame_u, width=25, font=entry_font, text=last_name)
entry_2.place(x=45, y=235)

Label(left_frame_u, text='Student ID', bg=lf_bg, font=lbl_font).place(x=98, y=275)
entry_3 = Entry(left_frame_u, width=25, font=entry_font, text=student_id)
entry_3.place(x=45, y=305)

Label(left_frame_u, text='Course and Section', bg=lf_bg, font=lbl_font).place(x=61, y=345)
entry_4 = Entry(left_frame_u, width=25, font=entry_font, text=course)
entry_4.place(x=45, y=375)

Label(left_frame_u, text='Mobile Number', bg=lf_bg, font=lbl_font).place(x=78, y=415)
entry_5 = Entry(left_frame_u, width=25, font=entry_font, text=mobile_number)
entry_5.place(x=45, y=445)

Label(left_frame_u, text='Email', bg=lf_bg, font=lbl_font).place(x=120, y=485)
entry_6 = Entry(left_frame_u, width=25, font=entry_font, text=email)
entry_6.place(x=45, y=515)

# Left Frame for Borrower's Inventory
Label(left_frame_i, text="Borrowing Record", bg=lf_bg, font=('Poppins',15,'bold')).place(x=51, y=25)

Label(left_frame_i, text="User's ID", bg=lf_bg, font=lbl_font).place(x=105, y=65)
en1 = Entry(left_frame_i, width=25, font=entry_font, text=user_id_var)
en1.place(x=45, y=95)

Label(left_frame_i, text="Student's Name", bg=lf_bg, font=lbl_font).place(x=75, y=135)
en2 = Entry(left_frame_i, width=25, font=entry_font, text=student_name_var)
en2.place(x=45, y=165)

Label(left_frame_i, text='Book ID', bg=lf_bg, font=lbl_font).place(x=110, y=205)
bk_id_entry1 = Entry(left_frame_i, width=25, font=entry_font, text=bk_id_var)
bk_id_entry1.place(x=45, y=235)

Label(left_frame_i, text='Book Title', bg=lf_bg, font=lbl_font).place(x=100, y=275)
en3 = Entry(left_frame_i, width=25, font=entry_font, text=bk_name_var)
en3.place(x=45, y=305)

Label(left_frame_i, text='Date Borrowed', bg=lf_bg, font=lbl_font).place(x=80, y=345)
en4 = Entry(left_frame_i, width=25, font=entry_font, text=date_borrowed)
en4.insert(0, "mm/dd/yyyy")
en4.place(x=45, y=375)

Label(left_frame_i, text='Due Date', bg=lf_bg, font=lbl_font).place(x=104, y=415)
en5 = Entry(left_frame_i, width=25, font=entry_font, text=due_date_var)
en5.insert(0, "mm/dd/yyyy")
en5.place(x=45, y=445)

Label(left_frame_i, text='Date Returned', bg=lf_bg, font=lbl_font).place(x=80, y=485)
en6 = Entry(left_frame_i, width=25, font=entry_font, text=date_returned)
en6.insert(0, "mm/dd/yyyy")
en6.place(x=45, y=515)

Label(left_frame_i, text='Fee', bg=lf_bg, font=lbl_font).place(x=128, y=555)
en7 = Entry(left_frame_i, width=25, font=entry_font, text=fee)
en7.place(x=45, y=585)

# Right Top Frame
Button(RT_frame, text='User Management', relief='flat', borderwidth=0, font=btn_font, bg=rbf_bg, width=16, command=switch_to_user_database, padx=5).place(x=28, y=65)
Button(RT_frame, text='Book Inventory', relief='flat', borderwidth=0, font=btn_font, bg=rbf_bg, width=13, command=switch_to_book_inventory, padx=5).place(x=185, y=65)
Button(RT_frame, text="Borrower's Inventory", relief='flat', borderwidth=0, font=btn_font, bg=rbf_bg, width=17, command=switch_to_borrower_inventory, padx=5).place(x=315, y=65)

Label(RT_frame, text='Import/Export Data', bg=rtf_bg, font=('Poppins', 11)).place(x=1138, y=5)

database_options = ["User Management", "Book Inventory", "Borrower's Inventory"]
combobox = ttk.Combobox(RT_frame, values=database_options, state="readonly", font=('Poppins', 10))
combobox.set("Select Database")
combobox.pack(pady=10)
combobox.place(x=1138, y=30, height=25, width=150)

# Create an Export Button
export_button = tk.Button(RT_frame, text="Export", font=btn_font, bg=btn_hlb_bg, state="disabled")
export_button.pack(pady=5)
export_button.place(x=1218, y=61, height=25)

# Create an Import Button
import_button = tk.Button(RT_frame, text="Import", font=btn_font, bg=btn_hlb_bg, state="disabled")
import_button.pack(pady=5)
import_button.place(x=1138, y=61, height=25)

combobox.bind("<<ComboboxSelected>>", on_combobox_selected)

# Right Bottom Frame for Book Inventory
RB_frame_inventory = Frame(RB_frame)
RB_frame_inventory.pack(side=RIGHT, fill=BOTH, expand=YES)
Label(RB_frame_inventory, text='BOOK INVENTORY', bg=rbf_bg, font=("Noto Sans CJK TC", 15, 'bold')).pack(side=TOP, fill=X)

search_book_entry = Entry(RB_frame_inventory, width=15, font=('Poppins', 10))
search_book_entry.pack(side=TOP, padx=10, pady=10)
search_book_entry.place(x=1150, y=3, height=21)
search_book_entry.insert(0, "Search...")

sorting_options = ["Default", "Book ID", "Title", "Author", "Date", "Course"]
sorting_var = StringVar()
sorting_var.set(sorting_options[0])
sorting_dropdown = ttk.Combobox(RB_frame_inventory, textvariable=sorting_var, values=sorting_options, font=('Poppins', 10))
sorting_dropdown.pack(side=TOP, pady=5)
sorting_dropdown.place(x=1035, y=3, width=110, height=21)
sorting_dropdown.bind("<<ComboboxSelected>>", filter_book_inventory)

search_book_entry.bind("<Return>", lambda event: search_book_inventory())

tree = ttk.Treeview(RB_frame_inventory, selectmode=BROWSE, columns=('Book ID', 'Book Name', 'Book Author', 'Book Date', 'Book Course'))

XScrollbar = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
YScrollbar = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
XScrollbar.pack(side=BOTTOM, fill=X)
YScrollbar.pack(side=RIGHT, fill=Y)
tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)

tree.heading('Book ID', text='Book ID', anchor=CENTER)
tree.heading('Book Name', text='Title', anchor=CENTER)
tree.heading('Book Author', text='Author', anchor=CENTER)
tree.heading('Book Date', text='Date', anchor=CENTER)
tree.heading('Book Course', text='Course', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=150, stretch=NO)
tree.column('#2', width=700, stretch=NO)
tree.column('#3', width=300, stretch=NO)
tree.column('#4', width=100, stretch=NO)
tree.column('#5', width=175, stretch=NO)

tree.place(y=30, x=0, relheight=0.9, relwidth=1)

clear_and_display()

# Right Bottom Frame for User Database
RB_frame_user_database = Frame(RB_frame)
RB_frame_user_database.pack(side=RIGHT, fill=BOTH, expand=YES)
Label(RB_frame_user_database, text='USER MANAGEMENT', bg=rbf_bg, font=("Noto Sans CJK TC", 15, 'bold')).pack(side=TOP, fill=X)

search_user_entry = Entry(RB_frame_user_database, width=15, font=('Poppins', 10))
search_user_entry.pack(side=TOP, padx=10, pady=10)
search_user_entry.place(x=1150, y=3, height=21)
search_user_entry.insert(0, "Search...")

user_sorting_options = ["Default", "RFID Tag", "First Name", "Last Name", "Student ID", "Course", "Mobile Number", "Email"]
user_sorting_var = StringVar()
user_sorting_var.set(user_sorting_options[0])
user_sorting_dropdown = ttk.Combobox(RB_frame_user_database, textvariable=user_sorting_var, values=user_sorting_options, font=('Poppins', 10))
user_sorting_dropdown.pack(side=TOP, pady=5)
user_sorting_dropdown.place(x=1035, y=3, width=110, height=21)
user_sorting_dropdown.bind("<<ComboboxSelected>>", filter_user_database)

search_user_entry.bind("<Return>", lambda event: search_user())

tree_user_database = ttk.Treeview(RB_frame_user_database, selectmode=BROWSE, columns=('RFID Tag', 'First Name', 'Last Name', 'Student ID', 'Course', 'Mobile Number', 'Email'))

XScrollbar = Scrollbar(tree_user_database, orient=HORIZONTAL, command=tree_user_database.xview)
YScrollbar = Scrollbar(tree_user_database, orient=VERTICAL, command=tree_user_database.yview)
XScrollbar.pack(side=BOTTOM, fill=X)
YScrollbar.pack(side=RIGHT, fill=Y)
tree_user_database.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)

tree_user_database.heading('RFID Tag', text='RFID Tag', anchor=CENTER)
tree_user_database.heading('First Name', text='First Name', anchor=CENTER)
tree_user_database.heading('Last Name', text='Last Name', anchor=CENTER)
tree_user_database.heading('Student ID', text='Student ID', anchor=CENTER)
tree_user_database.heading('Course', text='Course and Section', anchor=CENTER)
tree_user_database.heading('Mobile Number', text='Mobile Number', anchor=CENTER)
tree_user_database.heading('Email', text='Email', anchor=CENTER)

tree_user_database.column('#0', width=0, stretch=NO)
tree_user_database.column('#1', width=175, stretch=NO)
tree_user_database.column('#2', width=175, stretch=NO)
tree_user_database.column('#3', width=175, stretch=NO)
tree_user_database.column('#4', width=175, stretch=NO)
tree_user_database.column('#5', width=175, stretch=NO)
tree_user_database.column('#6', width=175, stretch=NO)
tree_user_database.column('#7', width=175, stretch=NO)

tree_user_database.place(y=30, x=0, relheight=0.9, relwidth=1)

clear_and_display_2()

# Right Bottom Frame for Borrower's Inventory
RB_frame_borrower = Frame(RB_frame)
RB_frame_borrower.pack(side=RIGHT, fill=BOTH, expand=YES)
Label(RB_frame_borrower, text="BORROWER'S INVENTORY", bg=rbf_bg, font=("Noto Sans CJK TC", 15, 'bold')).pack(side=TOP, fill=X)

search_inventory_entry = Entry(RB_frame_borrower, width=15, font=('Poppins', 10))
search_inventory_entry.pack(side=TOP, padx=10, pady=10)
search_inventory_entry.place(x=1150, y=3, height=21)
search_inventory_entry.insert(0, "Search...")

inventory_sorting_options = ["Default", "Student's ID", "Student's Name", "Book ID", "Book Title", "Date Borrowed", "Due Date", "Date Returned", "Fee"]
inventory_sorting_var = StringVar()
inventory_sorting_var.set(inventory_sorting_options[0])
inventory_sorting_dropdown = ttk.Combobox(RB_frame_borrower, textvariable=inventory_sorting_var, values=inventory_sorting_options, font=('Poppins', 10))
inventory_sorting_dropdown.pack(side=TOP, pady=5)
inventory_sorting_dropdown.place(x=1035, y=3, width=110, height=21)
inventory_sorting_dropdown.bind("<<ComboboxSelected>>", filter_inventory)

search_inventory_entry.bind("<Return>", lambda event: search_inventory())

tree_inventory = ttk.Treeview(RB_frame_borrower, selectmode=BROWSE, columns=("User's ID", "Student's Name", 'Book ID', 'Book Title', 'Date Borrowed', 'Due Date', 'Date Returned', 'Fee'))

XScrollbar = Scrollbar(tree_inventory, orient=HORIZONTAL, command=tree_inventory.xview)
YScrollbar = Scrollbar(tree_inventory, orient=VERTICAL, command=tree_inventory.yview)
XScrollbar.pack(side=BOTTOM, fill=X)
YScrollbar.pack(side=RIGHT, fill=Y)
tree_inventory.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)

tree_inventory.heading("User's ID", text="User's ID", anchor=CENTER)
tree_inventory.heading("Student's Name", text="Student's Name", anchor=CENTER)
tree_inventory.heading('Book ID', text='Book ID', anchor=CENTER)
tree_inventory.heading('Book Title', text='Book Title', anchor=CENTER)
tree_inventory.heading('Date Borrowed', text='Date Borrowed', anchor=CENTER)
tree_inventory.heading('Due Date', text='Due Date', anchor=CENTER)
tree_inventory.heading('Date Returned', text='Date Returned', anchor=CENTER)
tree_inventory.heading('Fee', text='Fee', anchor=CENTER)

tree_inventory.column('#0', width=0, stretch=NO)
tree_inventory.column('#1', width=120, stretch=NO)
tree_inventory.column('#2', width=170, stretch=NO)
tree_inventory.column('#3', width=120, stretch=NO)
tree_inventory.column('#4', width=700, stretch=NO)
tree_inventory.column('#5', width=120, stretch=NO)
tree_inventory.column('#6', width=120, stretch=NO)
tree_inventory.column('#7', width=120, stretch=NO)
tree_inventory.column('#8', width=100, stretch=NO)

tree_inventory.place(y=30, x=0, relheight=0.9, relwidth=1)

clear_and_display_3()
highlight_nearing_due_dates()
check_due_dates_periodically()

# Finalizing the Window
root.update()
root.mainloop()