import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3
import pyqrcode
from PIL import ImageTk, Image


class Main(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def started_create(self):
        self.top_level = Top()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file='add.gif')
        btn_open_dialog = tk.Button(toolbar, text='Додавання даних', command=self.open_dialog,
                                    bg='#d7d8e0', bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редагувати дані', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete.gif')
        btn_delete = tk.Button(toolbar, text='Видалити дані', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.get_qr_img = tk.PhotoImage(file='qr.gif')
        btn_get_qr = tk.Button(toolbar, text='Згенерувати QR-код', bg='#d7d8e0', bd=0, image=self.get_qr_img,
                               compound=tk.TOP, command=self.get_qr)
        btn_get_qr.pack(side=tk.LEFT)

        self.get_qr_img1 = tk.PhotoImage(file='getqr.gif')
        btn_get_qr1 = tk.Button(toolbar, text='Отримати QR-код', bg='#d7d8e0', bd=0, image=self.get_qr_img1,
                                compound=tk.TOP, command=self.started_create)
        btn_get_qr1.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, column=('ID', 'Name', 'Surname', 'Flight To', 'Flight Time', 'Vaccine',
                                               'Number Of Vaccine'), height=15, show='headings')

        self.tree.column('ID', width=25, anchor=tk.CENTER)
        self.tree.column('Name', width=75, anchor=tk.CENTER)
        self.tree.column('Surname', width=95, anchor=tk.CENTER)
        self.tree.column('Flight To', width=120, anchor=tk.CENTER)
        self.tree.column('Flight Time', width=95, anchor=tk.CENTER)
        self.tree.column('Vaccine', width=105, anchor=tk.CENTER)
        self.tree.column('Number Of Vaccine', width=115, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Ім\'я')
        self.tree.heading('Surname', text='Прізвище')
        self.tree.heading('Flight To', text='Місце призначення')
        self.tree.heading('Flight Time', text='Час відправки')
        self.tree.heading('Vaccine', text='Назва вакцини')
        self.tree.heading('Number Of Vaccine', text='К-ть доз вакцини')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, name, surname, flight_to, flight_time, vaccine, number_of_vaccine):
        self.db.insert_data(name, surname, flight_to, flight_time, vaccine, number_of_vaccine)
        self.view_records()

    def update_records(self, name, surname, flight_to, flight_time, vaccine, number_of_vaccine):
        self.db.cur.execute('UPDATE passenger_traffic SET name=?, surname=?, flight_decision=?,'
                            'flight_time=?, vaccine=?, number_of_vaccine=? WHERE ID=?',
                            (name, surname, flight_to, flight_time, vaccine, number_of_vaccine,
                             self.tree.set(self.tree.selection()[0], '#1'),))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.cur.execute('SELECT * FROM passenger_traffic')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', '0', values=row) for row in self.db.cur.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cur.execute('DELETE FROM passenger_traffic WHERE id=?', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def get_qr(self):
        with sqlite3.connect("PassengersTraffic.db") as connect:
            items = connect.execute("SELECT name, surname, flight_decision, flight_time,"
                                    "vaccine, number_of_vaccine FROM passenger_traffic").fetchone()
            print(items)

        text = "\n".join(items)
        qr_code = pyqrcode.create(text)
        qr_code.png('qrcode1.png', scale=8)

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()


class Child(Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Додавання даних')
        self.geometry('400x300+400+300')
        self.resizable(False, False)

        lable_enterence = tk.Label(self, text='Поля для заповнення. Важливо заповнити всі поля,\n'
                                              'аби допомогти нам прискорити перевірку важливих документів.')
        lable_enterence.place(x=10, y=0)

        lable_name = tk.Label(self, text='Ім\'я')
        lable_name.place(x=40, y=60)
        lable_surname = tk.Label(self, text='Прізвище')
        lable_surname.place(x=40, y=90)
        lable_flight_to = tk.Label(self, text='Місце призначення')
        lable_flight_to.place(x=40, y=120)
        lable_flight_time = tk.Label(self, text='Час відправки')
        lable_flight_time.place(x=40, y=150)
        lable_vaccine = tk.Label(self, text='Назва вакцини')
        lable_vaccine.place(x=40, y=180)
        lable_nuber_of_vaccine = tk.Label(self, text='К-ть доз вакцини')
        lable_nuber_of_vaccine.place(x=40, y=210)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=60)

        self.entry_surname = ttk.Entry(self)
        self.entry_surname.place(x=200, y=90)

        self.entry_flight_to = ttk.Entry(self)
        self.entry_flight_to.place(x=200, y=120)

        self.entry_flight_time = ttk.Entry(self)
        self.entry_flight_time.place(x=200, y=150)

        self.combobox1 = ttk.Combobox(self, values=[u'Pfizer/BioNTech', u'Moderna', u'AstraZeneca', u'Johnson&Johnson'])
        self.combobox1.current(0)
        self.combobox1.place(x=200, y=180)

        self.combobox2 = ttk.Combobox(self, values=[u'One', u'Two'])
        self.combobox2.current(0)
        self.combobox2.place(x=200, y=210)

        bnt_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        bnt_cancel.place(x=300, y=260)

        self.btn_add = ttk.Button(self, text='Додати')
        self.btn_add.place(x=170, y=260)
        self.btn_add.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(), self.entry_surname.get(),
                                                                        self.entry_flight_to.get(),
                                                                        self.entry_flight_time.get(),
                                                                        self.combobox1.get(), self.combobox2.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('Редактування позиції')
        btn_edit = ttk.Button(self, text='Редактувати')
        btn_edit.place(x=100, y=260)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_records(self.entry_name.get(),
                                                                           self.entry_surname.get(),
                                                                           self.entry_flight_to.get(),
                                                                           self.entry_flight_time.get(),
                                                                           self.combobox1.get(), self.combobox2.get()))
        self.btn_add.destroy()

    def init_qr(self):
        self.title('Отримати QR-код')
        btn_qr = ttk.Button(self, text='Отримати')
        btn_qr.place(x=100, y=260)


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('PassengersTraffic.db')
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS passenger_traffic (ID TEXT PRIMARY KEY, name TEXT,'
                         'surname TEXT, flight_decision TEXT, flight_time TEXT, vaccine TEXT, number_of_vaccine TEXT)')
        self.conn.commit()

    def insert_data(self, name, surname, flight_to, flight_time, vaccine, number_of_vaccine):
        self.cur.execute('INSERT INTO passenger_traffic (name, surname, flight_decision, '
                         'flight_time, vaccine, number_of_vaccine) VALUES (?, ?, ?, ?, ?, ?)',
                         (name, surname, flight_to, flight_time, vaccine, number_of_vaccine))
        self.conn.commit()


class Top(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('QR-code')
        self.geometry('400x400')
        self.img = ImageTk.PhotoImage(Image.open("qrcode1.png"))
        self.panel = Label(self, image=self.img)
        self.panel.pack(side="bottom", fill="both", expand="no")


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Passengers traffic")
    root.geometry('650x450+300+200')
    root.resizable(False, False)
    root.mainloop()
