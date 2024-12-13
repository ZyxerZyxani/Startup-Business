#!/usr/bin/python3

License ="""LICENSE: 

BSD 2-Clause License

Copyright (c) 2024, Emilio Anastasio Müller

Redistribution and use in source and binary forms, with or
without modification, are permitted provided that the
following conditions are met:

1. Redistributions of source code must retain the above 
   copyright notice, this list of conditions and the following
   disclaimer.

2. Redistributions in binary form must reproduce the above
   copyright notice, this list of conditions and the following
   disclaimer in the documentation and/or other materials
   provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS
AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND 
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE.
"""
import math
import asyncio
import os
from tkinter import *
from tkinter import ttk
from itertools import chain
import pymsgbox
import platform
import sys
import traceback
import sqlite3
import datetime
from sqlite3 import Error
# Shows license. Removing this could break license. 
pymsgbox.alert(License, "License Agreement")

# Checks if database exists in working directory. If not, generate the table. 
if not os.path.exists('inventering.db'):
    query = "CREATE TABLE IF NOT EXISTS LAPTOPS (MODEL TEXT, RAM TEXT, CPU TEXT, MISC TEXT, NUMBER PRIMARY KEY);"
    try:
        connection = sqlite3.connect("inventering.db")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()
    except Error as err:
        pymsgbox.alert(f"Couldn't create database.\n\nError message from database:\n{err}", "Exception Error")
        connection.close()
        exit()
class Root(Tk):

    def __init__(self):
        super(Root, self).__init__()

        # Initialise variables that are needed to be initialized for proper function. 
        self.page = 0
        self.laptopboo = True
        self.values = []

        # Make it look slick.
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure(bg="#2b2b2b")
        self.style.configure("TButton", background="#2b2b2b", foreground ="#8a8a8a", borderwidth=0)
        self.style.map('TButton', background=[('active', '#2b2b2b')])
        self.style.configure("white.TButton", foreground="white", background="#2b2b2b")
        self.style.map('white.TButton', background=[('active', '#202020')])
        self.style.configure("green.TButton", foreground="green", background="#ffffff")
        self.style.configure("red.TButton", foreground="red", background="#2b2b2b")
        self.style.map('red.TButton', background=[('active', '#505050')])
        self.style.configure("ping.TButton", foreground = "#aaaaaa",background="#3b3b3b")
        self.style.map('ping.TButton', background=[('active', '#505050')])

        # A toggle to change first row of buttons.
        self.laptop = ttk.Button(self, style = "ping.TButton", text="Laptop", command=self.laptopbool)
        self.laptop.grid(columnspan=1, row=0, column=0)

        # Buttons with value, click to toggle between sorting in ascending/descending order (feature not yet implemented).
        self.RAM = ttk.Button(self, style = "ping.TButton", text="RAM")
        self.RAM.grid(columnspan=1, row=0, column=1)
        self.CPU = ttk.Button(self, style = "ping.TButton", text="CPU")
        self.CPU.grid(row=0, column=2)
        self.misc = ttk.Button(self, style = "ping.TButton", text="Misc")
        self.misc.grid(row=0, column=3)
        # Command on this button is supposed to be on the alternative toggled version. TL;DR button needs fixing.
        self.nummer = ttk.Button(self, style="ping.TButton", text="Number", command = self.editsq)
        self.nummer.grid(row=0, column=4)

        # Entry fields, meant to correspond to sqlite3 database query values.
        self.value0 = ttk.Entry(self, width = 10)
        self.value0.grid(row=1, column=0)
        self.value1 = ttk.Entry(self, width= 10)
        self.value1.grid(row=1, column=1)
        self.value2 = ttk.Entry(self, width = 10)
        self.value2.grid(row=1, column=2)
        self.value3 = ttk.Entry(self, width= 10)
        self.value3.grid(row=1, column=3)
        self.value4 = ttk.Entry(self, width= 10)
        self.value4.grid(row=1, column=4)
                
        # Placeholders to not make it look like ass (also useful for later). Also put them in list
        self.allphs = []
        for i in range(80):
            ph = ttk.Button(self, style = "TButton", text = "")
            ph.grid(row=(math.floor(i/5) + 2), column=(i%5))
            self.allphs.append(ph)

        # self.laptop = ttk.Button(self, style = "ping.TButton", text="Laptop", command=self.laptopbool)
        # Buttons to search, add, and delete entry from database
        self.addin = ttk.Button(self, style = "green.TButton", text="Add", command=self.addtosql)
        self.addin.grid(row=18, column=0)
        self.previous = ttk.Button(self, style = "green.TButton", text="<--", command=self.previousp)
        self.previous.grid(row=18, column=1)
        self.search = ttk.Button(self, style = "green.TButton", text="Search", command=self.searchsq)
        self.search.grid(row=18, column=2)
        self.next = ttk.Button(self, style = "green.TButton", text="-->", command=self.nextp)
        self.next.grid(row=18, column=3)
        self.tabort = ttk.Button(self, style = "red.TButton", text="Remove", command=self.delfromsql)
        self.tabort.grid(row=18, column=4)
       
        # Make list of all entry values.
        self.allvalues = [self.value0, self.value1, self.value2, self.value3, self.value4]
        self.searchsq()

    # Search button function. Needed to be able to reset page and also to be able to show different pages (16 results per page). 
    def searchsq(self):
        self.page = 0
        self.searchsql()

    # shows prior 16 results unles 0 in which case nothing happens.
    def previousp(self):
        if self.page == 0:
            "Easter egg"
        else:
            self.page -= 1
            self.searchsql()

    # Shows next page. Need to implement function to not do that if last result is shown.
    # At the moment you can keep clicking it to show the non existent 2 billionth to 2 billion and 16th result. Do not recomend.
    def nextp(self):
        self.page += 1
        self.searchsql()

    # Edits database entry. Takes the values and edits the entry with the matching number (unique identifier).
    def editsq(self):
        if self.laptopboo:
            return
        if self.value4.get() != "":
            values = []
            colum = ["MODEL","RAM","CPU","MISC", "NUMBER"]
            q = 0
            for sq in self.allvalues:
                if sq.get() != "":
                    if q == 4:
                        values.append(f"WHERE {colum[4]} = {sq.get()}")
                    else:
                        values.append(f"{colum[q]} = '{sq.get()}', ")
                q += 1
            las = values[-1]
            del values [-1]
            values[-1] = f"{values[-1][:-2]} "
            updatetasks = "UPDATE LAPTOPS SET "
            query = f"{updatetasks}{''.join(values)}{las}"
            try:
                connection = sqlite3.connect("inventering.db")
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
                connection.close()
            except Error as err:
                pymsgbox.alert(f"Couldn't change values in the database.\nCheck if the number exists and is correct.\n\nError message from the database:\n{err}", "Exception Error")
                connection.close()
        else:
            pymsgbox.alert("Number wasn't given. Can't change values without specifying unique number. The unique numbers columns are the values that change.", "No unique number given")
        self.searchsql("more")

    # Search SQLite3 database. 
    def searchsql(self, igor = "lmao"):
        columns = ["SELECT * FROM LAPTOPS WHERE MODEL LIKE", "RAM LIKE", "CPU LIKE", "MISC LIKE", "NUMBER = "]
        q = 0
        # igor != more skips reassigning values to the search query. Compensates the unnecessary CPU cycle needed for previousp(). 
        # Saves maybe 1 nano second and improves user experience when deleting entries or reassigning values.
        if igor != "more":
            self.values = []
            for sq in self.allvalues:
                if q == 4:
                    self.values.append(f"{columns[q]} {sq.get()} ")
                else:
                    self.values.append(f"{columns[q]} '%{sq.get()}%'")
                q += 1
        if self.value4.get() == "" or igor == "last":
            del self.values[-1]
        query=" AND ".join(self.values) + f"ORDER BY NUMBER ASC LIMIT {self.page * 16}, 16"

        connection = sqlite3.connect("inventering.db")
        cursor = connection.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()
        valuesp = []
        for row in rows:
            for y in row:
                valuesp.append(y)
        for x in range(len(valuesp)):
            self.allphs[x].configure(style="white.TButton", text=valuesp[x])
        for x in range(len(self.allphs))[len(valuesp):]:
            self.allphs[x].configure(style="TButton", text="")


    # Add inputs to SQL database
    def addtosql(self):
        values = []
        for sq in self.allvalues:
            values.append(sq.get())
        connection = sqlite3.connect("inventering.db")
        cursor = connection.cursor()
        try:
            cursor.execute(f"INSERT INTO LAPTOPS VALUES ('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}', {values[4]} )")
            connection.commit()
            connection.close()
        except Error as err:
            pymsgbox.alert(f"Couldn't add values to the database.\nIs the number unique?\n\nError message from the database:\n{err}", "Exception Error")
            connection.close()
        self.searchsql("more")

    # Function to delete row from database. It takes the last value, nummer, and deletes row with it. 
    def delfromsql(self):
        values = []
        for sq in self.allvalues:
            values.append(sq.get())
        try:
            nummer = int(values[-1])

        except Exception:
            pymsgbox.alert("Note that the number must be a whole number. The program deletes the row which has the given number, no commas or punctiations.", "Not INT error")

        else:
            connection = sqlite3.connect("inventering.db")
            cursor = connection.cursor()
            try:
                cursor.execute(f"DELETE FROM LAPTOPS WHERE NUMBER IS {nummer}")
                connection.commit()
                connection.close()
            except Error as err:
                pymsgbox.alert(f"Couldn't delete from the database.\nDoes the number exist in the database?\n\nError message from the database:\n{err}", "Exception error")
                connection.close()
            else:
            # Redo searchquery without the unique identifier
                self.searchsql("more")

    # A toggle to change database table as well as matching labels. For future use of course, no usage atm.
    def laptopbool(self):
        if self.laptopboo:
            self.laptop.configure(text="Value 0")
            self.RAM.configure(text="Value 1")
            self.CPU.configure(text="Value 2")
            self.misc.configure(text="Value 3")
            self.nummer.configure(text="Change")
            self.laptopboo = False
        else:
            self.laptop.configure(text="Laptop")
            self.RAM.configure(text="RAM")
            self.CPU.configure(text="CPU")
            self.misc.configure(text="Misc")
            self.nummer.configure(text="Number")
            self.laptopboo = True


if __name__ == "__main__":
    root = Root()
    root.title("Inventering")
    root.mainloop()
