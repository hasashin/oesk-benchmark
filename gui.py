import tkinter as tk
import tkinter.ttk as ttk
import threading
from turtle import left
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

class Plotter:

    def __init__(self, table):
        self.data = table

    def plot_results(self):
        for datarow in self.data:
            x = [int(x_val) for x_val in list(datarow['values'])]
            y = [datarow['values']['{}'.format(i)].total_seconds() for i in list(datarow['values'])]
            plt.scatter(x, y, marker='.', label='{} {}'.format(datarow['engine'],datarow['timestamp'].strftime("%Y-%m-%d %H:%M:%S")))
        plt.xlabel('Liczba rekordów w każdej z tabel')
        plt.ylabel('Czas wykonania zapytania [s]')
        plt.title('Wykres wydajności bazy')
        plt.legend()
        plt.grid(True)
        plt.show()

class DbGui:
    db_type = {"MySQL":1, "PostgreSQL":2, "SQLite":3}

    def __init__(self, db_connector):
        self.db_connector = db_connector

    table = None
    results = None
    window = None
    vars={'selected_db':None, 'server_address':None, 'progress':None}
    bench_id=0
    times=[]

    def show_results(self):
        newtimes = []
        for item in self.table.selection():
            newtimes.append(self.times[int(item)])
        pltr = Plotter(newtimes)
        pltr.plot_results()

    def start_benchmark(self):
        self.vars['progress']['value'] = 0
        try:
            self.db_connector.start(0)
        except AttributeError:
            try:
                self.db_connector.connect_to_database(self.vars['server_address'])
            except:
                tk.Message(self.window, text='Failed to connect to database. Please check your address and try again.').pack()
                return
        threading.Thread(target=self.start_benchmark_thread).start()

    def start_benchmark_thread(self):
        try:
            self.times.append({})
            self.times[self.bench_id]['timestamp'] = datetime.now()
            self.times[self.bench_id]['engine'] = [k for k,v in self.db_type.items() if v == self.db_connector.type][0]
            self.times[self.bench_id]['values'] = {}

            self.vars['progress_label'].set('Running test 1 of 10')
            self.times[self.bench_id]['values']['10'] = self.db_connector.start(10)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 2 of 10')
            self.times[self.bench_id]['values']['20'] = self.db_connector.start(20)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 3 of 10')
            self.times[self.bench_id]['values']['30'] = self.db_connector.start(30)
            self.vars['progress']['value'] += 10
            
            self.vars['progress_label'].set('Running test 4 of 10')
            self.times[self.bench_id]['values']['40'] = self.db_connector.start(40)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 5 of 10')
            self.times[self.bench_id]['values']['50'] = self.db_connector.start(50)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 6 of 10')
            self.times[self.bench_id]['values']['60'] = self.db_connector.start(60)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 7 of 10')
            self.times[self.bench_id]['values']['70'] = self.db_connector.start(70)
            self.vars['progress']['value'] += 10
            
            self.vars['progress_label'].set('Running test 8 of 10')
            self.times[self.bench_id]['values']['80'] = self.db_connector.start(80)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 9 of 10')
            self.times[self.bench_id]['values']['90'] = self.db_connector.start(90)
            self.vars['progress']['value'] += 10

            self.vars['progress_label'].set('Running test 10 of 10')
            self.times[self.bench_id]['values']['100'] = self.db_connector.start(100)
            self.vars['progress']['value'] += 10
            self.vars['progress']['value'] = 100

            self.vars['progress_label'].set('Tests completed!')
        except Exception as e:
            tk.Message(self.window, text="Failed to make tests").pack()
            self.vars['progress_label'].set('Tests failed!')
            self.vars['progress']['value'] = 0
            print(e)
        finally:
            self.add_items()
            self.bench_id += 1

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

    def save_results(self):
        for item in self.table.selection():
            datarow = self.times[int(item)]
            new_times = {}
            for k in datarow['values']:
                new_times[k] = datarow['values'][k].total_seconds()
            df = pd.DataFrame.from_dict(new_times, orient='index')
            df.to_csv('output-{}-{}.csv'.format(datarow['engine'],int(datarow['timestamp'].timestamp())))

    def prepare_widgets(self, root:tk.Tk):
        title = tk.Label(\
            root, \
            text='This app is benchmarking database engine of your choice'\
        )
        title.pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(side='left', anchor='n')

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

        self.vars['progress_label'] = tk.StringVar()
        prog_label = tk.Label(\
            frame,\
            textvariable=self.vars['progress_label']
        )
        prog_label.pack(\
            before=self.vars['progress'], \
            side='bottom', \
            anchor='s' \
        )
        
        self.vars['progress'] = ttk.Progressbar(frame, length = 280)
        self.vars['progress'].pack( \
            side='bottom', \
            anchor='sw', \
            padx=10, \
            pady=10 \
        )

        btn = tk.Button(\
            frame, \
            text="Start", \
            command=self.start_benchmark \
        )
        btn.pack( \
            side='bottom', \
            anchor='s', \
            padx=5, \
            pady=5 \
        )


        frame2 = tk.Frame(root, borderwidth=2)
        frame2.pack(side='right', anchor='n')

        self.table = ttk.Treeview(frame2)

        self.table['columns'] = ('bench_id', 'timestamp', 'engine')


        self.table.column("#0", width=0,  stretch=tk.NO)
        self.table.column("bench_id",anchor=tk.CENTER, width=40)
        self.table.column("timestamp",anchor=tk.CENTER, width=160)
        self.table.column("engine",anchor=tk.CENTER, width=100)

        self.table.heading("#0",text="",anchor=tk.CENTER)
        self.table.heading("bench_id",text="Id",anchor=tk.CENTER)
        self.table.heading("timestamp",text="Timestamp",anchor=tk.CENTER)
        self.table.heading("engine",text="Database type",anchor=tk.CENTER)

        self.table.pack(side='top', anchor='ne', padx=20)

        frame3 = tk.Frame(frame2, borderwidth=2)
        frame3.pack(side='bottom', anchor='n')

        btn2 = tk.Button( \
            frame3, \
            text="Show results", \
            command=self.show_results \
        )
        btn2.pack( \
            side='right', \
            anchor='se', \
            padx=5, \
            pady=5 \
        )

        btn3 = tk.Button( \
            frame3, \
            text="Save results", \
            command=self.save_results \
        )
        btn3.pack( \
            before=btn2, \
            side='right', \
            anchor='se', \
            padx=5, \
            pady=5 \
        )

    def prepare_window(self):
        root = tk.Tk()
        root.title('DataBase benchmark')
        root.geometry("700x300")
        root.minsize(width=700, height=300)
        root.maxsize(width=700, height=300)
        return root
    
    def add_items(self):
        self.table.insert(
            parent='', 
            index='end', 
            iid=self.bench_id, 
            text='', 
            values=(
                self.bench_id+1,
                self.times[self.bench_id]['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
                self.times[self.bench_id]['engine']
            )
        )

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