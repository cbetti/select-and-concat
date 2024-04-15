import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os


class SelectAndConcatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Select and Concat")

        # Configure the grid layout
        self.root.grid_columnconfigure(1, weight=1)  # Makes the second column (index 1) expandable
        self.root.grid_rowconfigure(0, weight=1)  # Makes the row expandable

        # Frame for Listbox and Scrollbar on the left
        left_frame = tk.Frame(self.root)
        left_frame.grid(row=0, column=0, sticky='ns')

        # Scrollable Listbox
        self.listbox = tk.Listbox(left_frame, selectmode='multiple', width=70, height=30,
                                  # exportselection=False preserves the selected files after the
                                  # text_area obtains a selection.
                                  exportselection=False)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(left_frame, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=scrollbar.set)

        # Buttons below the listbox
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=1, column=0, sticky='ew')
        load_button = tk.Button(button_frame, text="Load Files", command=self.load_files)
        load_button.pack(side=tk.LEFT, expand=True, fill=tk.X)
        concat_button = tk.Button(button_frame, text="Concatenate Files", command=self.concatenate_files)
        concat_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Scrolled Text to display file contents on the right
        self.text_area = scrolledtext.ScrolledText(self.root, width=60, height=15)
        self.text_area.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

    def load_files(self):
        self.listbox.delete(0, tk.END)
        directory = filedialog.askdirectory()
        if directory:
            self.base_directory = directory
            for root, dirs, files in os.walk(directory):
                for file in files:
                    relative_path = os.path.relpath(os.path.join(root, file), directory)
                    self.listbox.insert(tk.END, relative_path)

    def concatenate_files(self):
        indices = self.listbox.curselection()
        if not hasattr(self, 'base_directory') or self.base_directory is None:
            messagebox.showerror("Error", "Please load files before concatenating.")
            return

        content = ""
        for index in indices:
            file_path = os.path.join(self.base_directory, self.listbox.get(index))
            with open(file_path, 'r') as file:
                content += file.read() + '\n\n'

        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, content)


if __name__ == "__main__":
    root = tk.Tk()
    app = SelectAndConcatApp(root)
    root.mainloop()
