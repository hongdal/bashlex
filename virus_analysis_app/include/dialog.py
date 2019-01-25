from tkinter import *
import tkinter as tk
import os

SMALLFONT = ('Arial', 8)
MIDFONT = ('Arial', 10)
LARGEFONT = ('Arial', 12)
WIDTH = 50
HEIGHT = 10

class Dialog(Toplevel):
  """Tk Dialog for class view to use

    Longer class information....
    Longer class information....

    Attributes:
        result: A data which need to use by other funtions
  """

  def __init__(self, parent, title=None, argv=None, argv2=None):
    """Inits Dialog Class."""
    Toplevel.__init__(self, parent)
    self.transient(parent)
    if title:
      self.title(title)
    self.parent = parent
    self.result = None
    self.res_nums = 0
    self.argv = argv
    self.argv2 = argv2
    body = Frame(self)
    self.initial_focus = self.body(body)
    body.pack(padx=5, pady=5)
    self.buttonbox()
    # self.grab_set()
    if not self.initial_focus:
      self.initial_focus = self
    self.protocol("WM_DELETE_WINDOW", self.cancel)
    self.geometry(
        "+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
    self.initial_focus.focus_set()
    self.wait_window(self)

  def body(self, master):
    """create dialog body.  return widget that should have
    initial focus.  this method should be overridden
    """
    pass

  def buttonbox(self):
    """add standard button box. override if you don't want the
    standard buttons
    """
    box = Frame(self)
    w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
    w.pack(side=LEFT, padx=5, pady=5)
    w = Button(box, text="Cancel", width=10, command=self.cancel)
    w.pack(side=LEFT, padx=5, pady=5)

    self.bind("<Return>", self.ok)
    self.bind("<Escape>", self.cancel)
    box.pack()

  # standard button semantics
  def ok(self, event=None):
    if not self.validate():
      self.initial_focus.focus_set()  # put focus back
      return
    self.withdraw()
    self.update_idletasks()
    self.apply()
    self.cancel()

  def cancel(self, event=None):
    # put focus back to the parent window
    self.parent.focus_set()
    self.destroy()

  # command hooks
  def validate(self):
    return 1  # override

  def apply(self):
    pass  # override


class RespInfoDialog(Dialog):
  def body(self, master):
    Label(master, text='New repository Name: ').grid(row=0, sticky=E)
    Label(master, text='Path of this repository: ').grid(row=1, sticky=E)
    Label(master, text='Support Suffix: ').grid(row=2, sticky=E)

    def selectPath():
      path_ = askdirectory()
      path.set(path_)

    path = StringVar()
    Button(master, text="Browse...", command=selectPath).grid(row=1, column=2)

    self.e1 = Entry(master)
    self.e2 = Entry(master, textvariable=path)
    self.e3 = Entry(master)
    self.e1.insert(0, "Example")
    self.e2.insert(0, "/home/guoze/02_test/")
    self.e3.insert(0, "pdf mobi")

    self.e1.grid(row=0, column=1)
    self.e2.grid(row=1, column=1)
    self.e3.grid(row=2, column=1)
    return self.e1  # initial focus

  def validate(self):
    try:
      rep_name = str(self.e1.get().strip())
      rep_path = str(self.e2.get().strip())
      support_suffix = str(self.e3.get().strip())
      support_suffix = support_suffix.split()
      self.result = [rep_name, rep_path, support_suffix]
      self.res_nums = len(self.result)
      return 1
    except (FileNotFoundError, ValueError):
      tkinter.messagebox.showwarning("Bad input",
                                     "Illegal values, please try again")
      return 0


class SelectRepDialog(Dialog):
  def body(self, master):
    self.rep_list = tk.Listbox(master)
    self.rep_list.config(fg='black', bg='#F5F5F5', bd=0.2, font=MIDFONT)
    self.rep_list.config(width=WIDTH, height=HEIGHT)

    scrollbar = tk.Scrollbar(
        master, orient=VERTICAL, command=self.rep_list.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    self.rep_list.configure(yscrollcommand=scrollbar.set)

    self.rep_list.grid(row=0)
    self.rep_list.bind("<Double-Button-1>", self.ok)
    self.rep_list.bind("<<ListboxSelect>>", self.selected)
    self.update_list()

  def selected(self, event):
    widget = event.widget
    selection = widget.curselection()
    value = widget.get(selection[0])
    self.selected_value = value

  def update_list(self):
    rep_dict = self.argv.get("all_repositories", {})
    if len(list(rep_dict.keys())) != 0:
      for i, one_rep in enumerate(rep_dict):
        rep_name = one_rep
        rep_path = rep_dict[one_rep][0]
        rep_suffix = ' '.join(str(e) for e in rep_dict[one_rep][1])
        rep_information = str(rep_name) + " (" + str(rep_path) + ") " + str(
            rep_suffix)
        self.rep_list.insert(tk.END, rep_information)

  def apply(self):
    rep_info = self.selected_value.split()
    rep_name = rep_info[0]
    self.result = rep_name
    self.res_nums = len(self.result)


class DisplayDetails(Dialog):
  def body(self, master):

    self.script_info = self.argv
    self.script_id = int(self.script_info[0])
    script_name = "Script Name: " + str(self.script_info[1])
    old_importance = int(self.script_info[2])
    old_urgency = int(self.script_info[3])
    old_tags = str(self.script_info[4])
    old_read = str(self.script_info[5])
    self.malware_report = self.argv2
    self.scan_report = self.malware_report['scans']
    self.table_data = []
    self.detected_number = 0
    for key in self.scan_report:
      element_date = []
      element_date.append(key)
      element_date.append(self.scan_report[key]['result'])
      element_date.append(self.scan_report[key]['detected'])
      element_date.append(self.scan_report[key]['version'])
      element_date.append(self.scan_report[key]['update'])
      if str(self.scan_report[key]['detected']) == 'True':
        self.detected_number = self.detected_number + 1
      self.table_data.append(element_date)


    self.file_info = tk.Frame(master, width=300, height=30)
    self.file_info.pack(side="top", fill="both", expand=True)

    Label(
        self.file_info, text=script_name, font=MIDFONT).grid(
            row=0, columnspan=2, sticky=W)
    Label(
        self.file_info, text='Importance(1~5): ').grid(
            row=1, column=0, sticky=E)
    Label(
        self.file_info, text='Urgency(1~5): ').grid(
            row=1, column=2, sticky=E)
    Label(self.file_info, text='Read(y/n): ').grid(row=1, column=4, sticky=E)
    Label(self.file_info, text='Tags: ').grid(row=2, column=0, sticky=E)
    Label(
        self.file_info, text='Detection ratio: ').grid(
            row=2, column=3, sticky=E)
    Label(
        self.file_info, text=self.detected_number).grid(
            row=2, column=4, sticky=E)

    script_info = self.argv
    e1 = Entry(self.file_info)
    e2 = Entry(self.file_info)
    e3 = Entry(self.file_info)
    e4 = Entry(self.file_info)
    # if self.argv2 == 1:
    e1.insert(0, old_importance)
    e2.insert(0, old_urgency)
    e3.insert(0, old_tags)
    e4.insert(0, old_read)

    e1.grid(row=1, column=1)
    e2.grid(row=1, column=3)
    e4.grid(row=1, column=5)
    e3.grid(row=2, column=1)

    tree_columns = ("a", "b", "c", "d", "e")
    self.table_frame = tk.Frame(master, width=600)
    self.tree = ttk.Treeview(
        self.table_frame, show="headings", height=20, columns=tree_columns)
    self.vbar = tk.Scrollbar(
        self.table_frame, orient=VERTICAL, command=self.tree.yview)
    self.tree.configure(yscrollcommand=self.vbar.set)
    self.vbar.config(command=self.tree.yview)
    self.tree.configure(yscrollcommand=self.vbar.set)
    self.tree.column("a", width=50, anchor="center")
    self.tree.column("b", width=300, anchor="center")
    self.tree.column("c", width=50, anchor="center")
    self.tree.column("d", width=50, anchor="center")
    self.tree.column("e", width=100, anchor="center")
    self.tree.heading("a", text="Company")
    self.tree.heading("b", text="Result")
    self.tree.heading("c", text="Detected")
    self.tree.heading("d", text="Version")
    self.tree.heading("e", text="Update")
    self.vbar.pack(side="right", fill="y")
    self.tree.pack(side="left", fill="both", expand=True)
    for col in tree_columns:
      self.tree.heading(
          col,
          command=
          lambda _col=col: self.treeview_sort_column(self.tree, _col, False))

    self.update_scripts_table(self.table_data)
    self.file_info.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="ew")
    self.table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
    master.grid_rowconfigure(1, weight=1)
    master.grid_columnconfigure(1, weight=1)
    self.update_scripts_table(self.table_data)

  def update_scripts_table(self, recs):
    def prettify_one(rec):
      one_row = [str(rec[0]), str(rec[1]), str(rec[2]), str(rec[3]), rec[4]]
      one_row = [item for item in one_row]
      return one_row

    recs_t = [prettify_one(rec) for rec in recs]
    for _ in map(self.tree.delete, self.tree.get_children("")):
      pass
    self.script_nums = len(recs_t)
    for i in range(len(recs_t)):
      self.tree.insert(
          "",
          "end",
          values=(recs_t[i][0], recs_t[i][1], recs_t[i][2], recs_t[i][3],
                  recs_t[i][4]))

  def treeview_sort_column(self, tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
      tv.move(k, '', index)
    tv.heading(
        col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

  def apply(self):
    return False


class EditScriptDialog(Dialog):
  def body(self, master):
    if self.argv2 == 1:
      self.script_info = self.argv
      self.script_id = int(self.script_info[0])
      script_name = "Script: " + str(self.script_info[1])
      old_importance = int(self.script_info[2])
      old_urgency = int(self.script_info[3])
      old_tags = str(self.script_info[4])
      old_read = str(self.script_info[5])
    else:
      script_name = self.argv
    Label(
        master, text=script_name, font=MIDFONT).grid(
            row=0, columnspan=2, sticky=W)
    Label(master, text='Importance(1~5): ').grid(row=1, sticky=E)
    Label(master, text='Urgency(1~5): ').grid(row=2, sticky=E)
    Label(master, text='Tags: ').grid(row=3, sticky=E)
    Label(master, text='Read(y/n): ').grid(row=4, sticky=E)
    self.script_info = self.argv
    self.e1 = Entry(master)
    self.e2 = Entry(master)
    self.e3 = Entry(master)
    self.e4 = Entry(master)
    if self.argv2 == 1:
      self.e1.insert(0, old_importance)
      self.e2.insert(0, old_urgency)
      self.e3.insert(0, old_tags)
      self.e4.insert(0, old_read)

    self.e1.grid(row=1, column=1)
    self.e2.grid(row=2, column=1)
    self.e3.grid(row=3, column=1)
    self.e4.grid(row=4, column=1)
    return self.e1  # initial focus

  def validate(self):
    try:
      importance = int(self.e1.get().strip())
      urgency = int(self.e2.get().strip())
      tags = str(self.e3.get().strip())
      read_state = str(self.e4.get().strip())
      if importance < 1 or importance > 5:
        raise ValueError("OutOfRange")
      if urgency < 1 or urgency > 5:
        raise ValueError("OutOfRange")
      if self.argv2 == 1:
        self.result = [self.script_id, importance, urgency, tags, read_state]
      else:
        self.result = [importance, urgency, tags, read_state]
      self.res_nums = len(self.result)
      return 1
    except ValueError:
      tkinter.messagebox.showwarning("Bad input",
                                     "Illegal values, please try again")
      return 0

  def apply(self):
    pass



if __name__ == '__main__':
  pass
