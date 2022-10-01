import os
from tkinter import *
from sqlite3 import *
from tkinter import ttk
from tkinter import messagebox
from random import *
import pandas as pd
from pygame import mixer
import matplotlib.pyplot as plt

# Background music
mixer.init()
mixer.music.load("s.mp3")
mixer.music.play(-1)

# Connecting to the database
db = connect('schooloffline.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS`students_record` (
  userid CHAR(50),
  name CHAR(50),
  contact_number CHAR(50),
  email CHAR(50),
  gender CHAR(50),
  dob CHAR(50),
  class CHAR(50)
)''')

db.commit()

# initializing the windows
windows = Tk()
windows.title("STUDENT'S MANAGEMENT")
windows.maxsize(width=1330, height=650)
windows.resizable(False, False)
windows.iconbitmap('s.ico')

# The body color
bg_color = 'dimgrey'


# add record
def add():
    if name_entry.get() == '':
        messagebox.showwarning(title="EMPTY INPUT", message="name is missing")
    elif contact_entry.get() == '':
        messagebox.showwarning(title='MISSING INPUT', message="contact is missing")
    elif email_entry.get() == '':
        messagebox.showwarning(title="MISSING INPUT", message="email is missing")
    elif '@' not in email_entry.get():
        messagebox.showwarning(title='Invalid Email', message="Invalid email")
    elif gender.get() == '':
        messagebox.showwarning(title="MISSING INPUT", message="gender is missing")
    elif class_entry.get() == '':
        messagebox.showwarning(title="MISSING INPUT", message="Class is missing")
    elif birth_entry.get() == '':
        messagebox.showwarning(title="MISSING INPUT", message="D.O.B is missing")
    else:
        mix = "12345678900987654321ABZY"
        ran_num = "".join(choice(mix) for _ in range(randint(5, 6)))
        curso = db.cursor()
        curso.execute(f"INSERT INTO students_record (userid, name, contact_number, email, gender, dob, class) "
                      f"VALUES(?,?,?,?,?,?,?)", ('student' + ran_num, name_entry.get().upper(),
                                                 contact_entry.get().upper(), email_entry.get().upper(),
                                                 gender.get().upper(), birth_entry.get().upper(),
                                                 class_entry.get().upper()))
        db.commit()
        messagebox.showinfo(title="ADDED", message=f"{name_entry.get()} has been added and also moved to excelsheet")
        ide = f"student{ran_num}"
        datas = [ide, name_entry.get().upper(), contact_entry.get().upper(), email_entry.get().upper(),
                 gender.get().upper(), birth_entry.get().upper(), class_entry.get().upper()]
        re = pd.DataFrame(data=[datas], columns=['userid', 'name', 'contact_number', 'email_entry', 'gender', 'D.O.B',
                                                 'class'])
        if class_entry.get().upper() + '_RECORD.csv' not in os.listdir():
            re.to_csv(class_entry.get().upper() + '_RECORD.csv', mode="a", header=['userid', 'name',
                                                                                   'contact_number', 'email_entry',
                                                                                   'gender', 'D.O.B',
                                                                                   'class'], index=False)
        else:
            re.to_csv(class_entry.get().upper() + '_RECORD.csv', mode="a", header=False, index=False)
        tree.insert('', i, text="", values=(f"student{ran_num}", name_entry.get().upper(),
                                            contact_entry.get().upper(), email_entry.get().upper(),
                                            gender.get().upper(), birth_entry.get().upper(), class_entry.get().upper()))
        name_entry.delete(0, END)
        contact_entry.delete(0, END)
        email_entry.delete(0, END)
        birth_entry.delete(0, END)
        class_entry.delete(0, END)
        curso.execute("SELECT count(*) FROM students_record")
        tot = curso.fetchall()[0][0]
        messagebox.showinfo(title="student's total".upper(), message=f"The total number of students is {tot}")

    return


def view():
    if not tree.selection():
        messagebox.showerror(title='Error', message='No student selected')
    else:
        selected_user = tree.focus()
        selected = tree.item(selected_user)
        selectee = selected["values"]
        messagebox.showinfo(title="User's Record", message=f'''
        Users Info:\n
    user's id: {selectee[0]}\n
    Name: {selectee[1]}\n
    Contact_Number: {selectee[2]}\n
    Email: {selectee[3]}\n
    Gender: {selectee[4]}\n
    D.O.B: {selectee[5]}\n
    Class: {selectee[6]}\n
        ''')
        # cusor = db.cursor()
        # cusor.execute("SELECT count(*) FROM students_record")
        # tot = cusor.fetchall()[0][0]
        # messagebox.showinfo(title="student's total".upper(), message=f"The total number of students is {tot}")
    return


# update user record to entry
def update():
    if not tree.selection():
        messagebox.showerror(title='Error', message='No student selected')
    else:
        selected_user = tree.focus()
        selected = tree.item(selected_user)
        selectee = selected["values"]
        name_entry.delete(0, END)
        contact_entry.delete(0, END)
        email_entry.delete(0, END)
        birth_entry.delete(0, END)
        class_entry.delete(0, END)
        name_entry.insert(0, selectee[1])
        contact_entry.insert(0, selectee[2])
        email_entry.insert(0, selectee[3])
        birth_entry.insert(0, selectee[5])
        class_entry.insert(0, selectee[6])
    return


# Update user record
def update_record():
    if not tree.selection():
        messagebox.showerror(title='Error', message='No student selected')
    elif name_entry.get() == '':
        messagebox.showwarning(title="EMPTY INPUT", message="name is missing. Click the update user to auto fill the "
                                                            "update form")
    elif contact_entry.get() == '':
        messagebox.showwarning(title='MISSING INPUT', message="contact is missing. Click the update user to auto fill "
                                                              "the update form")
    elif email_entry.get() == '':
        messagebox.showwarning(title="MISSING INPUT", message="email is missing. Click the update user to auto fill "
                                                              "the update form")
    elif gender.get() == '':
        messagebox.showwarning(title="MISSING INPUT", message="gender is missing.")
    elif class_entry.get() == '':
        messagebox.showwarning(title="MISSING INPUT", message="Class is missing. Click the update user to auto fill "
                                                              "the update form")
    elif birth_entry.get() == '':
        messagebox.showwarning(title="MISSING INPUT", message="D.O.B is missing. Click the update user to auto fill "
                                                              "the update form")
    else:
        selected_user = tree.focus()
        selected = tree.item(selected_user)
        selectee = selected["values"]
        curso = db.cursor()
        curso.execute(f'''UPDATE students_record SET name = ?, contact_number = ?, email = ?, gender = ?, dob =?,
          class = ?  WHERE userid ='{selectee[0]}';''', (name_entry.get().upper(), contact_entry.get().upper(),
                                                         email_entry.get().upper(), gender.get().upper(),
                                                         birth_entry.get().upper(), class_entry.get().upper()))
        db.commit()
        tree.delete(selected_user)
        messagebox.showinfo(title='successful', message=f"{name_entry.get()}, Successfully updated")
        tree.insert('', i, text="", values=(selectee[0], name_entry.get().upper(),
                                            contact_entry.get().upper(), email_entry.get().upper(),
                                            gender.get().upper(), birth_entry.get().upper(), class_entry.get().upper()))
    return


# Delete a particular student
def delete_user():
    if not tree.selection():
        messagebox.showerror(title='Error', message='No student selected')
    selected_user = tree.focus()
    selected = tree.item(selected_user)
    selectee = selected["values"]
    tree.delete(selected_user)
    cursor.execute('DELETE FROM students_record WHERE userid = ?', (selectee[0],))
    db.commit()
    cos = db.cursor()
    messagebox.showinfo(title="record deleted", message=f"Student successfully deleted")
    cos.execute("SELECT count(*) FROM students_record")
    tot = cos.fetchall()[0][0]
    messagebox.showinfo(title="student's total".upper(), message=f"The total number of students is {tot}")
    return


# Database function to truncate all the record in the database
def delete_database():
    cursor.execute("SELECT count(*) FROM (select 1 from students_record limit 1);")
    check = cursor.fetchall()[0][0]
    if check == 1:
        answer = messagebox.askyesno(title='DELETE ALL', message="Are you sure you want to"
                                                                 " delete all the student's record?")
        if answer:
            tree.destroy()
            reset_table = db.cursor()
            sql = "DELETE FROM students_record"
            reset_table.execute(sql)
            db.commit()
            messagebox.showinfo(title="DELETED", message="All student's records have been deleted")
        else:
            pass
    else:
        messagebox.showerror(title='EMPTY', message="There is no student registered")
    return


def stop():
    mixer.music.pause()
    return


def play():
    mixer.music.unpause()
    return


def record():
    js1 = cursor.execute('SELECT count(*) FROM students_record WHERE class = "JS1"')
    js1p = js1.fetchall()[0][0]

    js2 = cursor.execute('SELECT count(*) FROM students_record WHERE class = "JS2"')
    js2p = js2.fetchall()[0][0]

    js3 = cursor.execute('SELECT count(*) FROM students_record WHERE class = "JS3"')
    js3p = js3.fetchall()[0][0]

    ss1 = cursor.execute('SELECT count(*) FROM students_record WHERE class = "SS1"')
    ss1p = ss1.fetchall()[0][0]

    ss2 = cursor.execute('SELECT count(*) FROM students_record WHERE class = "SS2"')
    ss2p = ss2.fetchall()[0][0]

    ss3 = cursor.execute('SELECT count(*) FROM students_record WHERE class = "SS3"')
    ss3p = ss3.fetchall()[0][0]

    tto = cursor.execute("SELECT count(*) FROM students_record")
    t = tto.fetchall()[0][0]

    if (js1p or js2p or js3p or ss1p or ss2p or ss3p) == 0:
        messagebox.showinfo(title="No Record", message="There is no student in the record")
    else:
        messagebox.showinfo("Class record", message=f'''
        The total number of student's are:
        
            JS1 - {js1p}
            JS2 - {js2p}
            JS3 - {js3p}
            SS1 - {ss1p}
            SS2 - {ss2p}
            SS3 - {ss3p}
            The total of {t} students
        ''')

    return


def plo():
    js1 = cursor.execute('SELECT count(*) FROM students_record WHERE class = "JS1"')
    js1p = js1.fetchall()[0][0]

    js2 = cursor.execute('SELECT count(*) FROM students_record WHERE class = "JS2"')
    js2p = js2.fetchall()[0][0]

    js3 = cursor.execute('SELECT count(*) FROM students_record WHERE class = "JS3"')
    js3p = js3.fetchall()[0][0]

    ss1 = cursor.execute('SELECT count(*) FROM students_record WHERE class = "SS1"')
    ss1p = ss1.fetchall()[0][0]

    ss2 = cursor.execute('SELECT count(*) FROM students_record WHERE class = "SS2"')
    ss2p = ss2.fetchall()[0][0]

    ss3 = cursor.execute('SELECT count(*) FROM students_record WHERE class = "SS3"')
    ss3p = ss3.fetchall()[0][0]

    dat = [js1p, js2p, js3p, ss1p, ss2p, ss3p]
    ru = pd.DataFrame(data=[dat], columns=['JS1', 'JS2', 'JS3', 'SS1', 'SS2', 'SS3'])
    if 'students_record.csv' in os.listdir():
        os.remove('students_record.csv')
        ru.to_csv('students_record.csv', index=False)
    else:
        ru.to_csv('students_record.csv', index=False)

    cla = pd.read_csv('students_record.csv')
    plt.title("Student's record")
    label = ['JS1', 'JS2', 'JS3', 'SS1', 'SS2', 'SS3']
    values = [int(cla.JS1), int(cla.JS2), int(cla.JS3), int(cla.SS1), int(cla.SS2), int(cla.SS3)]
    plt.ylabel("Student's record")
    plt.xlabel("Classes in School")
    plt.yticks([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11])
    plt.bar(label, values)
    plt.show()
    return

# Selecting gender and plotting them as graph


def gen():
    maler = cursor.execute('SELECT count(*) FROM students_record WHERE gender = "MALE"')
    malers = maler.fetchall()[0][0]

    femaler = cursor.execute('SELECT count(*) FROM students_record WHERE gender = "FEMALE"')
    femalers = femaler.fetchall()[0][0]

    otherser = cursor.execute('SELECT count(*) FROM students_record WHERE class = "OTHERS"')
    otherses = otherser.fetchall()[0][0]

    dat = [malers, femalers, otherses]
    ru = pd.DataFrame(data=[dat], columns=['MALE', 'FEMALE', 'OTHERS'])
    if 'gender.csv' in os.listdir():
        os.remove('gender.csv')
        ru.to_csv('gender.csv', index=False)
    else:
        ru.to_csv('gender.csv', index=False)

    cla = pd.read_csv('gender.csv')
    plt.title("Student's record by Gender")
    label = ['MALE', 'FEMALE', 'OTHERS']
    values = [int(cla.MALE), int(cla.FEMALE), int(cla.OTHERS)]
    plt.ylabel("Student's record")
    plt.xlabel("gender")
    plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    plt.bar(label, values)
    plt.show()
    return

# Window for chat


def charts():
    win = Tk()
    win.title('charts')
    win.geometry('500x500')
    win.iconbitmap('s.ico')
    win.resizable(False, False)
    chart_frame = Frame(win, bg='teal', width=500, height=500)
    chart_frame.pack()
    chart_frame.pack_propagate(False)
    chart_label = Label(chart_frame, text="SELECT HOW TO VIEW CHART BASED ON YOUR SELECTION",
                        bg='teal', fg='white', width=80)
    chart_label.pack()
    class_btn = Button(chart_frame, text="View record by class".upper(), width=40, command=plo)
    class_btn.place(x=90, y=70)
    gender_btn = Button(chart_frame, text="View record by gender".upper(), width=40, command=gen)
    gender_btn.place(x=90, y=150)
    win.mainloop()
    return


# The main frame that holds all other frames
page_frame = Frame(windows, width=1330, height=650, bg=bg_color)
page_frame.grid()
page_frame.pack_propagate(False)
fonnt = ("Comic Sans MS", 13, "bold")
page_label = Label(page_frame, width=200, height=2, bg='darkslategrey', text='STUDENT MANAGEMENT', fg='white',
                   font=fonnt)
page_label.pack()
page_pause_btn = Button(page_frame, command=stop, text='stop song')
page_pause_btn.place(x=1180, y=5)
page_play_btn = Button(page_frame, command=play, text='play song')
page_play_btn.place(x=1250, y=5)

# The display frame for displaying all the student's record from the database

display_frame = Frame(page_frame, width=653, height=614, bg='white')
display_frame.place(x=677, y=35)
display_frame.pack_propagate(False)
display_label = Label(display_frame, width=110, height=2, bg='lightslategrey', text='STUDENT\'S RECORD', fg='white',
                      font=50)
display_label.pack()

# This is to create a mini frame for the tree's text
tree = ttk.Treeview(display_frame, height=27)

# This is to show the header and remove the icon space that is set default by tree
tree["show"] = 'headings'

# Styling the heading
st = ttk.Style(display_frame)
st.theme_use("default")

scr = ttk.Scrollbar(display_frame, orient="horizontal")
scr.config(command=tree.xview)
tree.configure(xscrollcommand=scr.set)
scr.pack(fill=X, side=BOTTOM)

scrv = ttk.Scrollbar(display_frame, orient="vertical")
scrv.config(command=tree.yview)
tree.configure(yscrollcommand=scrv.set)
scrv.pack(fill=Y, side=LEFT)

# Define the columns for entering the header
tree["columns"] = ("id", "name", "contact_number", "email", "gender", "D.O.B", "class")
tree.column("id", anchor=W, width=100)
tree.column("name", anchor=W, width=200)
tree.column("contact_number", anchor=W, width=100)
tree.column("email", anchor=W, width=200)
tree.column("gender", anchor=W, width=50)
tree.column("D.O.B", anchor=W, width=150)
tree.column("class", anchor=W, width=50)

tree.heading("id", text="id", anchor=W)
tree.heading("name", text="name", anchor=W)
tree.heading("contact_number", text="contact_number", anchor=W)
tree.heading("email", text="email", anchor=W)
tree.heading("gender", text="gender", anchor=W)
tree.heading("D.O.B", text="D.O.B", anchor=W)
tree.heading("class", text="class", anchor=W)

# Database function starts here...
my = db.cursor()
my.execute("SELECT * FROM students_record")

result = my.fetchall()

i = 0
for students in result:
    tree.insert('', i, text="",
                values=(students[0], students[1], students[2], students[3], students[4], students[5], students[6]))
    i += 1
tree.pack()

# The second frame for buttons
second_frame = Frame(page_frame, width=400, height=650, bg='slategrey')
second_frame.place(x=276, y=35)
second_frame.pack_propagate(False)

load_image = PhotoImage(file='s.png')
logo = Label(second_frame, image=load_image, bg='slategrey')
logo.image = load_image
logo.pack()

# The delete button
delete_btn = Button(second_frame, width=30, text='DELETE RECORD', command=delete_user)
delete_btn.place(x=90, y=175)

# The view record button
view_btn = Button(second_frame, width=30, text='VIEW RECORD', command=view)
view_btn.place(x=90, y=255)

# The reset button. It will delete the students record
update_btn = Button(second_frame, width=30, text='UPDATE USER', command=update)
update_btn.place(x=90, y=335)

# The delete_ database button will empty the database
delete_database_btn = Button(second_frame, width=30, text='DELETE ALL USERS', command=delete_database)
delete_database_btn.place(x=90, y=415)

# Get total number of students
record = Button(second_frame, width=30, text='VIEW ALL CLASS RECORD', command=record)
record.place(x=90, y=495)

records = Button(second_frame, width=30, text='VIEW CLASS RECORD IN CHARTS', command=charts)
records.place(x=90, y=575)

# The third frame for adding students record
third_frame = Frame(page_frame, width=277, height=650, bg='teal')
third_frame.place(x=0, y=35)
third_frame.pack_propagate(False)

# name label and entry for the third frame(add record)
name_label = Label(third_frame, text='NAME', fg='white', bg='teal', font=40)
name_label.place(x=100, y=45)
name_entry = Entry(third_frame, width=30)
name_entry.place(x=35, y=75)

# contact label and entry for the third frame(add record)
contact_label = Label(third_frame, text='CONTACT NUMBER', fg='white', bg='teal', font=40)
contact_label.place(x=50, y=125)
contact_entry = Entry(third_frame, width=30)
contact_entry.place(x=35, y=155)

# email label and entry for the third frame(add record)
email_label = Label(third_frame, text='EMAIL ADDRESS', fg='white', bg='teal', font=40)
email_label.place(x=60, y=205)
email_entry = Entry(third_frame, width=30)
email_entry.place(x=35, y=235)

# gender label and option-menu. you can select from it and the gender variable holds it
gender_label = Label(third_frame, text='GENDER', fg='white', bg='teal', font=40)
gender_label.place(x=90, y=275)
options = [
    'male', 'female', 'others'
]
gender = StringVar()
gender_entry = OptionMenu(third_frame, gender, *options)
gender_entry.place(x=105, y=310)

# birth label and entry for the third frame add record
birth_label = Label(third_frame, text='D.O.B', fg='white', bg='teal', font=40)
birth_label.place(x=100, y=355)
birth_entry = Entry(third_frame, width=30)
birth_entry.place(x=35, y=385)

# Class label for the third frame
class_label = Label(third_frame, text='CLASS', fg='white', bg='teal', font=40)
class_label.place(x=90, y=420)
class_entry = Entry(third_frame, width=30)
class_entry.place(x=35, y=450)

# Button for the third frame to add student's record
btn_add_entry = Button(third_frame, width=20, text='ADD RECORD', command=add)
btn_add_entry.place(x=45, y=510)

# Update button
update_add_entry = Button(third_frame, width=20, text='UPDATE RECORD', command=update_record)
update_add_entry.place(x=45, y=565)

# Display the window
windows.mainloop()
