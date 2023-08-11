import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import pickle
from threading import Thread
from queue import Queue
import threading
import glob
from mainnoconversion import process_folder, process_video, download_and_process

pickle_path = 'folder_paths.pkl'
MODEL_FILE = 'bdetectionmodel_05_01_23.onnx'

class Job:
    def __init__(self, func, args, description):
        self.func = func
        self.args = args
        self.description = description

# Job Queue
job_queue = Queue()
current_job_queue = Queue()

def worker():
    while True:
        job = job_queue.get()
        if job is None:
            break
        current_job_queue.put(job)
        job.func(*job.args)
        job_queue.task_done()
        current_job_queue.get()
        app.update_queue()



worker_thread = Thread(target=worker, daemon=True)
worker_thread.start()





def process_folder(folder_path, model_file, output_directory=None):
    # Get all video files in the folder with supported extensions
    video_files = glob.glob(os.path.join(folder_path, '*.mp4'))
    video_files += glob.glob(os.path.join(folder_path, '*.ts'))
    video_files += glob.glob(os.path.join(folder_path, '*.mkv'))
    video_files += glob.glob(os.path.join(folder_path, '*.avi'))

    return video_files


class ProcessFolderFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.pickle_path = 'folder_paths.pkl'  # Unique pickle path
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text='Folder:').grid(row=0)
        self.dir_entry = tk.Entry(self, width=50)
        self.dir_entry.grid(row=0, column=1)
        tk.Button(self, text='Select Folder', command=self.select_directory).grid(row=0, column=2)

        tk.Label(self, text='Output Dir:').grid(row=1)
        self.output_dir_entry = tk.Entry(self, width=50)
        self.output_dir_entry.grid(row=1, column=1)
        tk.Button(self, text='Select Output Folder', command=self.select_output_directory).grid(row=1, column=2)

        tk.Button(self, text='Process Folder', command=self.process_folder_gui).grid(row=2, column=0)


        # Add buffer input for before the timestamp
        tk.Label(self, text='Buffer Before (in seconds):').grid(row=3)
        self.buffer_before_entry = tk.Entry(self, width=50)
        self.buffer_before_entry.grid(row=3, column=1)

        # Add buffer input for after the timestamp
        tk.Label(self, text='Buffer After (in seconds):').grid(row=4)
        self.buffer_after_entry = tk.Entry(self, width=50)
        self.buffer_after_entry.grid(row=4, column=1)

        self.load_folder_paths()

    def select_directory(self):
        directory = filedialog.askdirectory()
        self.dir_entry.delete(0, tk.END)
        self.dir_entry.insert(0, directory)
        self.save_folder_paths()

    def select_output_directory(self):
        directory = filedialog.askdirectory()
        self.output_dir_entry.delete(0, tk.END)
        self.output_dir_entry.insert(0, directory)
        self.save_folder_paths()

    def process_folder_gui(self):
        directory = self.dir_entry.get()
        output_dir = self.output_dir_entry.get()
        buffer_before_seconds = int(self.buffer_before_entry.get())
        buffer_after_seconds = int(self.buffer_after_entry.get())

        if not directory or not output_dir:
            messagebox.showerror('Error', 'Please fill all the fields')
        else:
            video_files = process_folder(directory, MODEL_FILE, output_dir) 
            for video_file in video_files:
                description = f"{video_file}"
                job = Job(process_video, (video_file, MODEL_FILE, output_dir, buffer_before_seconds, buffer_after_seconds), description)
                job_queue.put(job)
            self.master.master.update_queue()

    def save_folder_paths(self):
        folder_paths = {
            'input_folder': self.dir_entry.get(),
            'output_folder': self.output_dir_entry.get(),
            'buffer_before': self.buffer_before_entry.get(),
            'buffer_after': self.buffer_after_entry.get()
        }
        with open(self.pickle_path, 'wb') as f:
            pickle.dump(folder_paths, f)

    def load_folder_paths(self):
        if os.path.exists(self.pickle_path):
            with open(self.pickle_path, 'rb') as f:
                folder_paths = pickle.load(f)
                self.dir_entry.insert(0, folder_paths.get('input_folder', ''))
                self.output_dir_entry.insert(0, folder_paths.get('output_folder', ''))
                self.buffer_before_entry.insert(0, folder_paths.get('buffer_before', '0'))
                self.buffer_after_entry.insert(0, folder_paths.get('buffer_after', '0'))

















class ProcessFileFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.pickle_path = 'file_paths.pkl'  # Unique pickle path
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text='File:').grid(row=0)
        self.file_entry = tk.Entry(self, width=50)
        self.file_entry.grid(row=0, column=1)
        tk.Button(self, text='Select File', command=self.select_file).grid(row=0, column=2)

        tk.Label(self, text='Output Dir:').grid(row=1)
        self.output_dir_entry = tk.Entry(self, width=50)
        self.output_dir_entry.grid(row=1, column=1)
        tk.Button(self, text='Select Output Folder', command=self.select_output_directory).grid(row=1, column=2)

        tk.Button(self, text='Process File', command=self.process_file_gui).grid(row=2, column=0)

        # Add buffer input for before the timestamp
        tk.Label(self, text='Buffer Before (in seconds):').grid(row=3)
        self.buffer_before_entry = tk.Entry(self, width=50)
        self.buffer_before_entry.grid(row=3, column=1)

        # Add buffer input for after the timestamp
        tk.Label(self, text='Buffer After (in seconds):').grid(row=4)
        self.buffer_after_entry = tk.Entry(self, width=50)
        self.buffer_after_entry.grid(row=4, column=1)

        self.load_folder_paths()

    def select_file(self):
        file = filedialog.askopenfilename()
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file)
        self.save_folder_paths()

    def select_output_directory(self):
        directory = filedialog.askdirectory()
        self.output_dir_entry.delete(0, tk.END)
        self.output_dir_entry.insert(0, directory)
        self.save_folder_paths()

    def process_file_gui(self):
        file = self.file_entry.get()
        output_dir = self.output_dir_entry.get()
        buffer_before_seconds = int(self.buffer_before_entry.get())
        buffer_after_seconds = int(self.buffer_after_entry.get())

        if not file or not output_dir:
            messagebox.showerror('Error', 'Please fill all the fields')
        else:
            description = f"Processing file: {file}"
            job = Job(process_video, (file, MODEL_FILE, output_dir, buffer_before_seconds, buffer_after_seconds), description)
            job_queue.put(job)
            self.master.master.update_queue()


    def process_file_thread(self, file, output_dir):
        process_video(file, MODEL_FILE, output_dir)
        self.master.master.update_queue()


    def save_folder_paths(self):
        folder_paths = {
            'input_file': self.file_entry.get(),
            'output_folder': self.output_dir_entry.get(),
            'buffer_before': self.buffer_before_entry.get(),
            'buffer_after': self.buffer_after_entry.get()
        }
        with open(self.pickle_path, 'wb') as f:
            pickle.dump(folder_paths, f)


    def load_folder_paths(self):
        if os.path.exists(self.pickle_path):
            with open(self.pickle_path, 'rb') as f:
                folder_paths = pickle.load(f)
                self.file_entry.insert(0, folder_paths.get('input_file', ''))
                self.output_dir_entry.insert(0, folder_paths.get('output_folder', ''))
                self.buffer_before_entry.insert(0, folder_paths.get('buffer_before', '0'))
                self.buffer_after_entry.insert(0, folder_paths.get('buffer_after', '0'))























class DownloadAndProcessFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.pickle_path = 'download_paths.pkl'  # Unique pickle path
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text='URL:').grid(row=0)
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.grid(row=0, column=1)

        tk.Label(self, text='Output Dir:').grid(row=1)
        self.output_dir_entry = tk.Entry(self, width=50)
        self.output_dir_entry.grid(row=1, column=1)
        tk.Button(self, text='Select Output Folder', command=self.select_output_directory).grid(row=1, column=2)

        tk.Button(self, text='Download & Process', command=self.download_and_process_gui).grid(row=3, column=0)

        # Add buffer input for before the timestamp
        tk.Label(self, text='Buffer Before (in seconds):').grid(row=4)
        self.buffer_before_entry = tk.Entry(self, width=50)
        self.buffer_before_entry.grid(row=4, column=1)

        # Add buffer input for after the timestamp
        tk.Label(self, text='Buffer After (in seconds):').grid(row=5)
        self.buffer_after_entry = tk.Entry(self, width=50)
        self.buffer_after_entry.grid(row=5, column=1)

        # Temp Folder Selection
        self.temp_folder_label = tk.Label(self, text="Temp Folder:")
        self.temp_folder_label.grid(row = 6, column = 0)

        self.temp_folder_entry = tk.Entry(self, width=50)
        self.temp_folder_entry.grid(row = 6, column = 1)

        self.temp_folder_button = tk.Button(self, text="Select Temp Folder", command=self.select_temp_folder)
        self.temp_folder_button.grid(row = 6, column = 2)

        self.load_temp_folder_path()
        self.load_folder_paths()


    def select_output_directory(self):
        directory = filedialog.askdirectory()
        self.output_dir_entry.delete(0, tk.END)
        self.output_dir_entry.insert(0, directory)
        self.save_folder_paths()

    def download_and_process_gui(self):
        self.save_folder_paths()
        url = self.url_entry.get()
        output_dir = self.output_dir_entry.get()
        buffer_before_seconds = int(self.buffer_before_entry.get())
        buffer_after_seconds = int(self.buffer_after_entry.get())
        temp_folder = self.temp_folder_entry.get()

        if not url or not output_dir:
            messagebox.showerror('Error', 'Please fill all the fields')
        else:
            description = f"{url}"
            job = Job(download_and_process, (url, MODEL_FILE, output_dir, temp_folder, buffer_before_seconds, buffer_after_seconds), description)
            job_queue.put(job)
            self.master.master.update_queue()

    def save_folder_paths(self):
        folder_paths = {
            'output_folder': self.output_dir_entry.get(),
            'buffer_before': self.buffer_before_entry.get(),
            'buffer_after': self.buffer_after_entry.get()
        }
        with open(self.pickle_path, 'wb') as f:
            pickle.dump(folder_paths, f)


    def load_folder_paths(self):
        if os.path.exists(self.pickle_path):
            with open(self.pickle_path, 'rb') as f:
                folder_paths = pickle.load(f)
                self.output_dir_entry.insert(0, folder_paths.get('output_folder', ''))
                self.buffer_before_entry.insert(0, folder_paths.get('buffer_before', '0'))
                self.buffer_after_entry.insert(0, folder_paths.get('buffer_after', '0'))


    def select_temp_folder(self):
        directory = filedialog.askdirectory()
        self.temp_folder_entry.delete(0, tk.END)
        self.temp_folder_entry.insert(0, directory)
        self.save_temp_folder_path()

    def save_temp_folder_path(self):
        with open('temp_folder_path.pkl', 'wb') as f:
            pickle.dump(self.temp_folder_entry.get(), f)

    def load_temp_folder_path(self):
        if os.path.exists('temp_folder_path.pkl'):
            with open('temp_folder_path.pkl', 'rb') as f:
                temp_folder_path = pickle.load(f)
                self.temp_folder_entry.insert(0, temp_folder_path)





























class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self)

        tab1 = ProcessFolderFrame(tab_control)
        tab_control.add(tab1, text='Process Folder')

        tab2 = DownloadAndProcessFrame(tab_control)
        tab_control.add(tab2, text='Download & Process')

        # Add the new tab
        tab3 = ProcessFileFrame(tab_control)
        tab_control.add(tab3, text='Process File')

        tab_control.pack(expand=1, fill='both')

        # Frame for queue
        self.queue_frame = tk.Frame(self)
        self.queue_frame.pack(fill='both', expand=True)

        self.queue_label = tk.Label(self.queue_frame, text="Queue:")
        self.queue_label.pack()

        # Create the listbox and make its width 100 characters
        self.queue_listbox = tk.Listbox(self.queue_frame, width=100)
        self.queue_listbox.pack(fill='both', expand=True)

        self.pause_button = tk.Button(self.queue_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.pack()

        self.is_paused = False

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Resume" if self.is_paused else "Pause")

    def update_queue(self):
        self.queue_listbox.delete(0, tk.END)

        if not current_job_queue.empty():
            current_job = current_job_queue.queue[0]
            self.queue_listbox.insert(tk.END, f"Processing: {current_job.description}")
            self.queue_listbox.itemconfig(0, {'bg':'green'})
        else:
            current_job = None

        for job in list(job_queue.queue): 
            if job != current_job:
                self.queue_listbox.insert(tk.END, job.description)




if __name__ == '__main__':
    app = App()
    app.mainloop()