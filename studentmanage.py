import datetime
from tkinter import *  # for creating the GUI
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3  # to connect the program to database

headlabel = ("Calibri", 15, 'bold')
labelfont = ('Calibri', 14)
entryfont = ('Calibri', 14)

connector = sqlite3.connect('Studentmanagement.db')
cursor = connector.cursor()
connector.execute("CREATE TABLE IF NOT EXISTS STUDENT_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, STREAM TEXT)")


def add_record():
    global name_stringvar, phone_stringvar, email_stringvar, gender_stringvar, stream_stringvar, dob
    name = name_stringvar.get()
    phone = phone_stringvar.get()
    email = email_stringvar.get()
    gender = gender_stringvar.get()
    DOB = dob.get_date()
    stream = stream_stringvar.get()

    if not name or not phone or not email or not gender or not DOB or not stream:
        mb.showerror('Error', "Please enter all Fields")
    else:
        try:
            connector.execute(
                'INSERT INTO STUDENT_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES(?, ?, ?, ?, ?, ?)', (
                    name, email, phone, gender, DOB, stream)
            )
            connector.commit()
            mb.showinfo('Record Inserted', f'Record of {name} is added.')
            clear_command()
            display_records()
            print("Yess")
        except:
            mb.showerror(
                'Internal Error', 'We are having some difficulty inserting your details. Try after sometime.')


def delete_command():
    if not tree.selection():
        mb.showerror('Error', 'Please select an item from the databse.')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values['values']
        tree.delete(current_item)
        connector.execute(
            'DELETE FROM STUDENT_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
        connector.commit()
        mb.showinfo('Deleted', 'The record has been Deleted Successfully.')
        display_records()


def view_command():
    pass


def clear_command():
    global name_stringvar, phone_stringvar, email_stringvar, gender_stringvar, dob, stream_stringvar
    for i in ['name_stringvar', 'phone_stringvar', 'email_stringvar', 'gender_stringvar', 'stream_stringvar']:
        exec(f"{i}.set('')")
    dob.set_date(datetime.datetime.now().date())


def remove_command():
    global tree
    tree.delete(*tree.get_children())
    clear_command()


def display_records():
    tree.delete(*tree.get_children())
    c = connector.execute('SELECT * FROM STUDENT_MANAGEMENT')
    data = c.fetchall()
    for records in data:
        tree.insert('', END, values=records)


# GUI Window Initialize
main = Tk()
main.title('Student Management System')
main.geometry('1000x1000')
main.resizable(0, 0)

lf_bg = 'Steelblue'

name_stringvar = StringVar()
email_stringvar = StringVar()
phone_stringvar = StringVar()
gender_stringvar = StringVar()
stream_stringvar = StringVar()

Label(main, text="STUDENT MANAGEMENT SYSTEM",
      font='Arial', bg='SkyBlue').pack(side=TOP, fill=X)
left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, height=1000, width=400)
right_frame = Frame(main, bg="gray")
right_frame.place(x=400, y=30, height=1000, width=600)

Label(left_frame, text="Name", font=labelfont, bg=lf_bg).place(x=30, y=50)
Label(left_frame, text="Contact Number",
      font=labelfont, bg=lf_bg).place(x=30, y=100)
Label(left_frame, text="Email Address",
      font=labelfont, bg=lf_bg).place(x=30, y=150)
Label(left_frame, text="Gender", font=labelfont, bg=lf_bg).place(x=30, y=200)
Label(left_frame, text="Date of Birth (DOB)",
      font=labelfont, bg=lf_bg).place(x=30, y=250)
Label(left_frame, text="Stream", font=labelfont, bg=lf_bg).place(x=30, y=300)
Entry(left_frame, width="20", textvariable=name_stringvar,
      font=entryfont).place(x=170, y=50)
Entry(left_frame, width="20", textvariable=phone_stringvar,
      font=entryfont).place(x=170, y=100)
Entry(left_frame, textvariable=email_stringvar,
      width="20", font=entryfont).place(x=170, y=150)
OptionMenu(left_frame, gender_stringvar, 'Male',
           'Female').place(x=170, y=200, width=70)
Entry(left_frame, width="20", textvariable=stream_stringvar,
      font=entryfont).place(x=170, y=300)
dob = DateEntry(left_frame, font=("Arial", 12), width=15)
dob.place(x=180, y=250)

Button(left_frame, text="Submit and Add Record", font=labelfont,
       command=add_record, width=18).place(x=80, y=380)
Button(left_frame, text="Delete Record", font=labelfont,
       command=delete_command, width=15).place(x=30, y=450)
Button(left_frame, text="View Record", font=labelfont,
       command=view_command, width=15).place(x=200, y=450)
Button(left_frame, text="Clear Fields", font=labelfont,
       command=clear_command, width=15).place(x=30, y=520)
Button(left_frame, text="Remove Database", font=labelfont,
       command=remove_command, width=15).place(x=200, y=520)


Label(right_frame, text="Student Records", width=400, font="Arial",
      bg="DarkBlue", fg="LightCyan").pack(side=TOP, fill=X)
tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('Stud ID', "Name", "Email Addr", "Contact No", "Gender", "Date of Birth", "Stream"))
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('Stud ID', text='ID', anchor=CENTER)
tree.heading('Name', text="Name", anchor=CENTER)
tree.heading("Email Addr", text="Email ID", anchor=CENTER)
tree.heading("Contact No", text="Phone No.", anchor=CENTER)
tree.heading("Gender", text="Gender", anchor=CENTER)
tree.heading("Date of Birth", text="DOB", anchor=CENTER)
tree.heading("Stream", text="Stream", anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=120, stretch=NO)
tree.column('#3', width=180, stretch=NO)
tree.column('#4', width=60, stretch=NO)
tree.column('#5', width=60, stretch=NO)
tree.column('#6', width=70, stretch=NO)
tree.column('#7', width=120, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)
display_records()

main.mainloop()
