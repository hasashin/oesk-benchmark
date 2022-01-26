from curses import window
import tkinter as tk
import tkinter.ttk as ttk
import threading
from turtle import left
import matplotlib.pyplot as plt

class Plotter:

    def __init__(self, table):
        self.data = table

    def plot_results(self, type):
        x = [int(x_val) for x_val in list(self.data)]
        y = [self.data['{}'.format(i)].total_seconds() for i in list(self.data)]
        plt.scatter(x, y, marker='.')
        plt.xlabel('Liczba rekordów w każdej z tabel')
        plt.ylabel('Czas wykonania zapytania [s]')
        plt.title('Wykres wydajności bazy {}'.format(type))
        plt.grid(True)
        plt.show()

class DbGui:
    db_type = {"MySQL":1, "PostgreSQL":2, "SQLite":3}

    def __init__(self, db_connector):
        self.db_connector = db_connector

    results = None
    window = None
    vars={'selected_db':None, 'server_address':None, 'progress':None}
    times={}

    def show_results(self):
        pltr = Plotter(self.times)
        pltr.plot_results([k for k,v in self.db_type.items() if v == self.db_connector.type][0])

    def start_benchmark(self):
        self.vars['progress']['value'] = 0
        try:
            self.db_connector.start(0)
        except AttributeError:
            try:
                self.db_connector.connect_to_database(self.vars['server_address'])
            except:
                tk.Message(window, text='Failed to connect to database. Please check your address and try again.').pack()
                return
        threading.Thread(target=self.start_benchmark_thread).start()

    def start_benchmark_thread(self):
        try:
            self.vars['progress_label'].set('Running test 1 of 10')
            self.times['100'] = self.db_connector.start(100)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 2 of 10')
            self.times['200'] = self.db_connector.start(200)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 3 of 10')
            self.times['300'] = self.db_connector.start(300)
            self.vars['progress']['value'] += 10
            
            self.vars['progress_label'].set('Running test 4 of 10')
            self.times['400'] = self.db_connector.start(400)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 5 of 10')
            self.times['500'] = self.db_connector.start(500)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 6 of 10')
            self.times['600'] = self.db_connector.start(600)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 7 of 10')
            self.times['700'] = self.db_connector.start(700)
            self.vars['progress']['value'] += 10
            
            self.vars['progress_label'].set('Running test 8 of 10')
            self.times['800'] = self.db_connector.start(800)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 9 of 10')
            self.times['900'] = self.db_connector.start(900)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 10 of 10')
            self.times['1000'] = self.db_connector.start(1000)
            self.vars['progress']['value'] += 10
            self.vars['progress']['value'] = 100

            self.vars['progress_label'].set('Tests completed!')
        except Exception as e:
            tk.Message(self.window, text="Failed to make tests").pack()
            self.vars['progress_label'].set('Tests failed!')
            self.vars['progress']['value'] = 0
            print(e)

    def set_grid_responsive(self, root:tk.Tk):
        n_rows = 5
        n_columns = 3
        for i in range(n_rows):
            root.grid_rowconfigure(i,  weight =1)
        for i in range(n_columns):
            root.grid_columnconfigure(i,  weight =1)

    def update_db(self, event):
        self.db_connector.type = self.db_type[self.vars['selected_db'].get()]
        self.db_connector.connect_to_database(self.vars['server_address'])

    def prepare_widgets(self, root:tk.Tk):
        title = tk.Label(\
            root, \
            text='This app is benchmarking database engine of your choice'\
        )
        title.pack()

        frame = tk.Frame(root, borderwidth=2)
        frame.pack(side='top', pady=20)

        step_1 = tk.Label(\
            frame, \
            text='1. Select database engine'\
        )
        step_1.pack()
        
        self.vars['selected_db'] = tk.StringVar()
        combo_engine = ttk.Combobox(\
            frame, \
            values=list(self.db_type), \
            textvariable=self.vars['selected_db'] \
        )
        combo_engine.current(0)
        combo_engine.pack( \
            anchor='w', \
            padx=20, \
            pady=10 \
        )
        combo_engine.bind('<<ComboboxSelected>>', self.update_db)

        step_2 = tk.Label(\
            frame, \
            text='2. Type server url'\
        )
        step_2.pack()

        self.vars['server_address'] = tk.StringVar()
        entry_server = tk.Entry( \
            frame, \
            width=20, \
            textvariable=self.vars['server_address'] \
        )
        entry_server.pack( \
            pady=10 \
        )

        bottom_frame = tk.Frame(root)
        bottom_frame.pack(side='left', anchor='sw')

        self.vars['progress'] = ttk.Progressbar(bottom_frame, length = 280)
        self.vars['progress'].pack( \
            side='left', \
            anchor='sw', \
            padx=10, \
            pady=10 \
        )

        self.vars['progress_label'] = tk.StringVar()
        prog_label = tk.Label(\
            bottom_frame,\
            textvariable=self.vars['progress_label']
        )
        prog_label.pack(\
            before=self.vars['progress'], \
            anchor='s' \
        )

        btn = tk.Button(\
            root, \
            text="Start", \
            command=self.start_benchmark \
        )
        btn.pack( \
            side='right', \
            anchor='se', \
            padx=5, \
            pady=5 \
        )

        btn2 = tk.Button( \
            root, \
            text="Show results", \
            command=self.show_results \
        )
        btn2.pack( \
            before=btn, \
            side='right', \
            anchor='se', \
            padx=5, \
            pady=5 \
        )

    def prepare_window(self):
        root = tk.Tk()
        root.title('DataBase benchmark')
        root.geometry("500x400")
        root.minsize(width=500, height=400)
        return root
    
    def prepare(self):
        self.window = self.prepare_window()
        self.prepare_widgets(self.window)

    def update_gui(self):
        self.window.update()
        self.window.after(3000, self.update_gui)

    def start(self):
        self.window.mainloop()
        self.update_gui()

if __name__== '__main__':
    print('This script is not meant to be run')
    exit(1)