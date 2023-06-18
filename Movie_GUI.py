from tkinter import *
from sql_config import dbconfig
import pypyodbc as pyo
import tkinter.messagebox

con = pyo.connect(**dbconfig)
# print(con)

cursor = con.cursor()


class Moviedb:
    def __init__(self):
        self.con = pyo.connect(**dbconfig)
        self.cursor = con.cursor()
        print("You have connected to the database")

    def __del__(self):
        self.con.close()

    def view(self):
        self.cursor.execute("Select original_title,year(convert(date,release_date)),convert(int,id) from movies_metadata")
        rows = self.cursor.fetchall()
        return rows


    def insert(self,Movie_title, realease_yr,movie_id):
        sql = "insert into movies_metadata(Movie_title,realease_yr,movie_id) values(?,?,?)"
        values = [Movie_title,realease_yr,movie_id]
        self.cursor.execute(sql,values)
        self.con.commit()
        tkinter.messagebox.showinfo(title="Movie Database",message = "New Movie added to the database")

    def update(self,Movie_title, realease_yr,movie_id):
        tsql = "update  movies_metadata set original_title = ?,release_date=?,where id=?"
        self.cursor.execute(tsql,[Movie_title,realease_yr,movie_id])
        self.con.commit()
        tkinter.messagebox.showinfo(title="Movie Database",message = "Movie Updated")

    def delete(self,id):
        delsql = "delete from movies_metadata where id=?"
        self.cursor.execute(delsql,[id])
        self.con.commit()
        tkinter.messagebox.showinfo(title="Movie Database",message = "Movie Deleted")


cls_db = Moviedb()


def selected_row(event):
    global selected_tuple
    index = list_bx.curselection()[0]
    selected_tuple = list_bx.get(index)
    title_entry.delete(0,'end')
    title_entry.insert('end',selected_tuple[0])
    release_yr_entry.delete(0,'end')
    release_yr_entry.insert('end',selected_tuple[1])
    movie_id_entry.delete(0,'end')
    movie_id_entry.insert('end',selected_tuple[2])


def view_records():
    list_bx.delete(0,'end')
    for row in cls_db.view():
        list_bx.insert('end', row)


def add_movie():
    cls_db.insert(title_text.get(),release_yr_text.get(),movie_id_text.get())
    list_bx.delete(0,'end')
    list_bx.insert('end',(title_text.get(),release_yr_text.get(),movie_id_text.get()))
    title_entry.delete(0,'end')
    release_yr_entry.delete(0,'end')
    movie_id_entry.delete(0,'end')
    con.commit()

def delete_records():

    Moviedb.delete((selected_tuple[2])
    con.commit()

def cls():
    list_bx.delete(0,'end')
    title_entry.delete(0,'end')
    release_yr_entry.delete(0,'end')
    movie_id_entry.delete(0,'end')

def update_records():
    Moviedb.update(selected_tuple[0],title_text.get(),release_yr_text.get(),movie_id_text.get())
    title_entry.delete(0,'end')
    release_yr_entry.delete(0,'end')
    movie_id_entry.delete(0,'end')
    con.commit()


def close():
    movie = Moviedb
    if tkinter.messagebox.askokcancel("Quit","Do you want to quit?"):
        root.destroy()
        del movie


root = Tk()

root.title("Movies Database Application")
root.geometry("850x500")
root.resizable(width=False,height=False)
root.configure(background="light green")

title_label = Label(root,text="Title",background="light green",font=("TKDefaultFont",16))
title_label.grid(row=0,column=0,sticky=W,padx=5)
title_text = StringVar()
title_entry = Entry(root,width=24,textvariable=title_text)
title_entry.grid(row=0,column=1,sticky=W,padx=10)

release_yr = Label(root,text="Release Year",background="light green",font=("TKDefaultFont",16))
release_yr.grid(row=0,column=2,sticky=W,padx=10)
release_yr_text = StringVar()
release_yr_entry = Entry(root,width=16,textvariable=release_yr_text)
release_yr_entry.grid(row=0,column=3,sticky=W)

movie_id = Label(root,text="Movie id",background="light green",font=("TKDefaultFont",16))
movie_id.grid(row=0,column=4,sticky=W,padx=10)
movie_id_text = StringVar()
movie_id_entry = Entry(root,width=16,textvariable=movie_id_text)
movie_id_entry.grid(row=0,column=5,sticky=W)

add_btn = Button(root,text="Add Movie", bg="blue", fg='white',font='helvetica 10 bold',command=add_movie)
add_btn.grid(row=0, column=6, sticky=W,padx=5)

list_bx = Listbox(root,height=16,width=30,font='helvetica 13',bg='light blue')
list_bx.grid(row=3,column=1,columnspan=5, sticky=W+E,padx=10,pady=40)
list_bx.bind('<<ListboxSelect>>',selected_row)


scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1, column=6,rowspan=14, sticky=W,padx=(0,15))

list_bx.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_bx.yview)

modify_btn = Button(root, text='Modify Record', bg='purple', fg='white',font='helvetica 10 bold',command=update_records)
modify_btn.grid(row=15,column=4)

delete_btn = Button(root, text='Delete Record', bg='red', fg='white',font='helvetica 10 bold',command=delete_records)
delete_btn.grid(row=15,column=5)

view_btn = Button(root, text='View All Records', bg='black', fg='white',font='helvetica 10 bold',command=view_records)
view_btn.grid(row=15,column=1)

clear_btn = Button(root, text='Clear Screen', bg='maroon', fg='white',font='helvetica 10 bold',command=cls)
clear_btn.grid(row=15,column=2, padx=(0,40))

exit_btn = Button(root, text='Exit Application', bg='blue', fg='white',font='helvetica 10 bold',command=root.destroy)
exit_btn.grid(row=15,column=3)

root.mainloop()

#print(title_text)