# -*- coding: ISO-8859-1  -*-
License ="""LICENSE: 

BSD 3-Clause License

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

3. Neither the name of the copyright holder nor the names
   of its contributors may be used to endorse or promote
   products derived from this software without specific prior
   written permission.

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
pymsgbox.alert(License, "License Agreement")

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

        self.page = 0
        self.laptopboo = True
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure(bg="#2b2b2b")
        self.style.configure("TButton", background="#2b2b2b", foreground ="#8a8a8a", borderwidth=0)
        self.style.map('TButton', background=[('active', '#2b2b2b')])
        # self.style.map('TButton', background=[('active', '#505050')])
        self.style.configure("white.TButton", foreground="white", background="#2b2b2b")
        self.style.map('white.TButton', background=[('active', '#202020')])
        self.style.configure("green.TButton", foreground="green", background="#ffffff")
        self.style.configure("red.TButton", foreground="red", background="#2b2b2b")
        self.style.map('red.TButton', background=[('active', '#505050')])
        self.style.configure("ping.TButton", foreground = "#aaaaaa",background="#3b3b3b")
        self.style.map('ping.TButton', background=[('active', '#505050')])

        # A toggle to change database table.
        self.laptop = ttk.Button(self, style = "ping.TButton", text="Laptop", command=self.laptopbool)
        self.laptop.grid(columnspan=1, row=0, column=0)

        # Buttons with value, click to toggle between sorting in ascending/descending order.
        self.RAM = ttk.Button(self, style = "ping.TButton", text="RAM")
        self.RAM.grid(columnspan=1, row=0, column=1)
        self.CPU = ttk.Button(self, style = "ping.TButton", text="CPU")
        self.CPU.grid(row=0, column=2)
        self.misc = ttk.Button(self, style = "ping.TButton", text="Misc")
        self.misc.grid(row=0, column=3)
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
        
        # Placeholders to not make it look like ass (also useful for later).
        self.ph0 = ttk.Button(self, style = "TButton", text = "")
        self.ph0.grid(row=2, column=0)
        self.ph1 = ttk.Button(self, style = "TButton", text = "")
        self.ph1.grid(row=2, column=1)
        self.ph2 = ttk.Button(self, style = "TButton", text = "")
        self.ph2.grid(row=2, column=2)
        self.ph3 = ttk.Button(self, style = "TButton", text = "")
        self.ph3.grid(row=2, column=3)
        self.ph4 = ttk.Button(self, style = "TButton", text = "")
        self.ph4.grid(row=2, column=4)
        self.ph5 = ttk.Button(self, style = "TButton", text = "")
        self.ph5.grid(row=3, column=0)
        self.ph6 = ttk.Button(self, style = "TButton", text = "")
        self.ph6.grid(row=3, column=1)
        self.ph7 = ttk.Button(self, style = "TButton", text = "")
        self.ph7.grid(row=3, column=2)
        self.ph8 = ttk.Button(self, style = "TButton", text = "")
        self.ph8.grid(row=3, column=3)
        self.ph9 = ttk.Button(self, style = "TButton", text = "")
        self.ph9.grid(row=3, column=4)
        self.ph10 = ttk.Button(self, style = "TButton", text = "")
        self.ph10.grid(row=4, column=0)
        self.ph11 = ttk.Button(self, style = "TButton", text = "")
        self.ph11.grid(row=4, column=1)
        self.ph12 = ttk.Button(self, style = "TButton", text = "")
        self.ph12.grid(row=4, column=2)
        self.ph13 = ttk.Button(self, style = "TButton", text = "")
        self.ph13.grid(row=4, column=3)
        self.ph14 = ttk.Button(self, style = "TButton", text = "")
        self.ph14.grid(row=4, column=4)
        self.ph15 = ttk.Button(self, style = "TButton", text = "")
        self.ph15.grid(row=5, column=0)
        self.ph16 = ttk.Button(self, style = "TButton", text = "")
        self.ph16.grid(row=5, column=1)
        self.ph17 = ttk.Button(self, style = "TButton", text = "")
        self.ph17.grid(row=5, column=2)
        self.ph18 = ttk.Button(self, style = "TButton", text = "")
        self.ph18.grid(row=5, column=3)
        self.ph19 = ttk.Button(self, style = "TButton", text = "")
        self.ph19.grid(row=5, column=4)
        self.ph20 = ttk.Button(self, style = "TButton", text = "")
        self.ph20.grid(row=6, column=0)
        self.ph21 = ttk.Button(self, style = "TButton", text = "")
        self.ph21.grid(row=6, column=1)
        self.ph22 = ttk.Button(self, style = "TButton", text = "")
        self.ph22.grid(row=6, column=2)
        self.ph23 = ttk.Button(self, style = "TButton", text = "")
        self.ph23.grid(row=6, column=3)
        self.ph24 = ttk.Button(self, style = "TButton", text = "")
        self.ph24.grid(row=6, column=4)
        self.ph25 = ttk.Button(self, style = "TButton", text = "")
        self.ph25.grid(row=7, column=0)
        self.ph26 = ttk.Button(self, style = "TButton", text = "")
        self.ph26.grid(row=7, column=1)
        self.ph27 = ttk.Button(self, style = "TButton", text = "")
        self.ph27.grid(row=7, column=2)
        self.ph28 = ttk.Button(self, style = "TButton", text = "")
        self.ph28.grid(row=7, column=3)
        self.ph29 = ttk.Button(self, style = "TButton", text = "")
        self.ph29.grid(row=7, column=4)
        self.ph30 = ttk.Button(self, style = "TButton", text = "")
        self.ph30.grid(row=8, column=0)
        self.ph31 = ttk.Button(self, style = "TButton", text = "")
        self.ph31.grid(row=8, column=1)
        self.ph32 = ttk.Button(self, style = "TButton", text = "")
        self.ph32.grid(row=8, column=2)
        self.ph33 = ttk.Button(self, style = "TButton", text = "")
        self.ph33.grid(row=8, column=3)
        self.ph34 = ttk.Button(self, style = "TButton", text = "")
        self.ph34.grid(row=8, column=4)
        self.ph35 = ttk.Button(self, style = "TButton", text = "")
        self.ph35.grid(row=9, column=0)
        self.ph36 = ttk.Button(self, style = "TButton", text = "")
        self.ph36.grid(row=9, column=1)
        self.ph37 = ttk.Button(self, style = "TButton", text = "")
        self.ph37.grid(row=9, column=2)
        self.ph38 = ttk.Button(self, style = "TButton", text = "")
        self.ph38.grid(row=9, column=3)
        self.ph39 = ttk.Button(self, style = "TButton", text = "")
        self.ph39.grid(row=9, column=4)
        self.ph40 = ttk.Button(self, style = "TButton", text = "")
        self.ph40.grid(row=10, column=0)
        self.ph41 = ttk.Button(self, style = "TButton", text = "")
        self.ph41.grid(row=10, column=1)
        self.ph42 = ttk.Button(self, style = "TButton", text = "")
        self.ph42.grid(row=10, column=2)
        self.ph43 = ttk.Button(self, style = "TButton", text = "")
        self.ph43.grid(row=10, column=3)
        self.ph44 = ttk.Button(self, style = "TButton", text = "")
        self.ph44.grid(row=10, column=4)
        self.ph45 = ttk.Button(self, style = "TButton", text = "")
        self.ph45.grid(row=11, column=0)
        self.ph46 = ttk.Button(self, style = "TButton", text = "")
        self.ph46.grid(row=11, column=1)
        self.ph47 = ttk.Button(self, style = "TButton", text = "")
        self.ph47.grid(row=11, column=2)
        self.ph48 = ttk.Button(self, style = "TButton", text = "")
        self.ph48.grid(row=11, column=3)
        self.ph49 = ttk.Button(self, style = "TButton", text = "")
        self.ph49.grid(row=11, column=4)
        self.ph50 = ttk.Button(self, style = "TButton", text = "")
        self.ph50.grid(row=12, column=0)
        self.ph51 = ttk.Button(self, style = "TButton", text = "")
        self.ph51.grid(row=12, column=1)
        self.ph52 = ttk.Button(self, style = "TButton", text = "")
        self.ph52.grid(row=12, column=2)
        self.ph53 = ttk.Button(self, style = "TButton", text = "")
        self.ph53.grid(row=12, column=3)
        self.ph54 = ttk.Button(self, style = "TButton", text = "")
        self.ph54.grid(row=12, column=4)
        self.ph55 = ttk.Button(self, style = "TButton", text = "")
        self.ph55.grid(row=13, column=0)
        self.ph56 = ttk.Button(self, style = "TButton", text = "")
        self.ph56.grid(row=13, column=1)
        self.ph57 = ttk.Button(self, style = "TButton", text = "")
        self.ph57.grid(row=13, column=2)
        self.ph58 = ttk.Button(self, style = "TButton", text = "")
        self.ph58.grid(row=13, column=3)
        self.ph59 = ttk.Button(self, style = "TButton", text = "")
        self.ph59.grid(row=13, column=4)
        self.ph60 = ttk.Button(self, style = "TButton", text = "")
        self.ph60.grid(row=14, column=0)
        self.ph61 = ttk.Button(self, style = "TButton", text = "")
        self.ph61.grid(row=14, column=1)
        self.ph62 = ttk.Button(self, style = "TButton", text = "")
        self.ph62.grid(row=14, column=2)
        self.ph63 = ttk.Button(self, style = "TButton", text = "")
        self.ph63.grid(row=14, column=3)
        self.ph64 = ttk.Button(self, style = "TButton", text = "")
        self.ph64.grid(row=14, column=4)
        self.ph65 = ttk.Button(self, style = "TButton", text = "")
        self.ph65.grid(row=15, column=0)
        self.ph66 = ttk.Button(self, style = "TButton", text = "")
        self.ph66.grid(row=15, column=1)
        self.ph67 = ttk.Button(self, style = "TButton", text = "")
        self.ph67.grid(row=15, column=2)
        self.ph68 = ttk.Button(self, style = "TButton", text = "")
        self.ph68.grid(row=15, column=3)
        self.ph69 = ttk.Button(self, style = "TButton", text = "")
        self.ph69.grid(row=15, column=4)
        self.ph70 = ttk.Button(self, style = "TButton", text = "")
        self.ph70.grid(row=16, column=0)
        self.ph71 = ttk.Button(self, style = "TButton", text = "")
        self.ph71.grid(row=16, column=1)
        self.ph72 = ttk.Button(self, style = "TButton", text = "")
        self.ph72.grid(row=16, column=2)
        self.ph73 = ttk.Button(self, style = "TButton", text = "")
        self.ph73.grid(row=16, column=3)
        self.ph74 = ttk.Button(self, style = "TButton", text = "")
        self.ph74.grid(row=16, column=4)
        self.ph75 = ttk.Button(self, style = "TButton", text = "")
        self.ph75.grid(row=17, column=0)
        self.ph76 = ttk.Button(self, style = "TButton", text = "")
        self.ph76.grid(row=17, column=1)
        self.ph77 = ttk.Button(self, style = "TButton", text = "")
        self.ph77.grid(row=17, column=2)
        self.ph78 = ttk.Button(self, style = "TButton", text = "")
        self.ph78.grid(row=17, column=3)
        self.ph79 = ttk.Button(self, style = "TButton", text = "")
        self.ph79.grid(row=17, column=4)

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
       
        # List of all placeholders.
        self.allphs = [self.ph0, self.ph1, self.ph2, self.ph3, self.ph4, self.ph5, self.ph6, \
                       self.ph7, self.ph8, self.ph9, self.ph10, self.ph11, self.ph12, self.ph13, \
                       self.ph14, self.ph15, self.ph16, self.ph17, self.ph18, self.ph19, self.ph20, \
                       self.ph21, self.ph22, self.ph23, self.ph24, self.ph25, self.ph26, self.ph27, \
                       self.ph28, self.ph29, self.ph30, self.ph31, self.ph32, self.ph33, self.ph34, \
                       self.ph35, self.ph36, self.ph37, self.ph38, self.ph39, self.ph40, self.ph41, \
                       self.ph42, self.ph43, self.ph44, self.ph45, self.ph46, self.ph47, self.ph48, \
                       self.ph49, self.ph50, self.ph51, self.ph52, self.ph53, self.ph54, self.ph55, \
                       self.ph56, self.ph57, self.ph58, self.ph59, self.ph60, self.ph61, self.ph62, \
                       self.ph63, self.ph64, self.ph65, self.ph66, self.ph67, self.ph68, self.ph69, \
                       self.ph70, self.ph71, self.ph72, self.ph73, self.ph74, self.ph75, self.ph76, \
                       self.ph77, self.ph78, self.ph79]

        # Make list of all entry values.
        self.allvalues = [self.value0, self.value1, self.value2, self.value3, self.value4]

    def previousp(self):
        if self.page == 0:
            "Easter egg"
        else:
            self.page -= 1
            self.searchsql()

    def nextp(self):
        self.page += 1
        self.searchsql()

    def searchsq(self):
        self.page = 0
        self.searchsql()

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
        self.searchsql()

    # Search SQLite3 database. 
    def searchsql(self):
        columns = ["SELECT * FROM LAPTOPS WHERE MODEL LIKE", "RAM LIKE", "CPU LIKE", "MISC LIKE", "NUMBER = "]
        values = []
        q = 0
        for sq in self.allvalues:
            if q == 4:
                values.append(f"{columns[q]} {sq.get()} ")
            else:
                values.append(f"{columns[q]} '%{sq.get()}%'")
            q += 1
        if self.value4.get() == "":
            del values[-1]
        query=" AND ".join(values) + f"LIMIT {self.page * 16}, 16"

        connection = sqlite3.connect("inventering.db")
        cursor = connection.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()
        valuesp = []
        for row in rows:
            # lis = row.split(",")
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
                self.searchsql()

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
