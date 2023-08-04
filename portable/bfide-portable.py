from sys import exit as exit__, argv
import sys
from pathlib import Path
from tkinter import END, INSERT, IntVar, Menu, Tk, Toplevel
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Label, Radiobutton, Button
from tkinter.filedialog import asksaveasfile as filesave, askopenfile
from os.path import exists, dirname, abspath
from tkinter.messagebox import askyesno
win=Tk()
win.withdraw()
win.title("Brainfuck IDE Portable")
if getattr(sys, "frozen", False):
    script = sys._MEIPASS
else:
    script = dirname(abspath(__file__))
if not script.endswith("\\"):
    script += "\\"
win.iconbitmap(script + "icon.ico")
win.resizable(0, 0)
if not exists(script + "settings.txt"):
    with open(script + "settings.txt", "w") as f:
        f.write("10")
def print_(text):
    output.configure(state="normal")
    output.insert(END, text)
    output.configure(state="disabled")
def clear(s=None):
    output.configure(state="normal")
    output.delete("1.0", END)
    output.configure(state="disabled")
def input():
    inp.configure(state="normal")
    inp.delete("1.0", END)
    while len(inp.get("1.0", END)) == 1:
        win.update()
        if run == 0:
            inp.config(state="disabled")
            return
    inp.configure(state="disabled")
    return inp.get("1.0", END)[0]
def exit_():
    if codeinp.get("1.0", END) != "\n":
        save()
    with open(script + "settings.txt", "w") as f:
        f.write(mode)
    win.destroy()
    exit__()
saved = 0
fpath = ""
def new(a=None):
    global saved, code_
    if codeinp.get("1.0", END) != "\n":
        save()
    saved = 0
    clear()
    codeinp.delete("1.0", END)
    win.title("Brainfuck IDE Portable")
    code_ = "\n"
    check()
def save(a=None):
    global saved
    global fpath
    global code_
    if saved == 0:
        if a is None:
            if askyesno("Brainfuck IDE Portable", "Do you want to save the file?"):
                temp = filesave(defaultextension='.bf', filetypes=[("Brainfuck Files", "*.bf"), ("Text files", "*.txt")])
                if temp is not None:
                    f = open(temp.name, "w")
                    fpath = temp.name
                    f.write(codeinp.get("1.0", END)[:-1])
                    f.close()
                    saved = 1
                    win.title("Brainfuck IDE Portable: " + fpath)
        else:
            temp = filesave(defaultextension='.bf', filetypes=[("Brainfuck Files", "*.bf"), ("Text files", "*.txt")])
            if temp is not None:
                f = open(temp.name, "w")
                fpath = temp.name
                f.write(codeinp.get("1.0", END)[:-1])
                f.close()
                saved = 1
                win.title("Brainfuck IDE Portable: " + fpath)
    else:
        f = open(fpath, "w")
        f.write(codeinp.get("1.0", END)[:-1])
        code_ = codeinp.get("1.0", END)
        f.close()
        win.title("Brainfuck IDE Portable: " + fpath)
    code_ = codeinp.get("1.0", END)
    check()
    return
code_ = "\n"
def open_(a=None):
    global fpath, saved, code, code_
    if codeinp.get("1.0", END) != "\n":
        save()
    temp = askopenfile(defaultextension='.bf', filetypes=[("Brainfuck Files", "*.bf"), ("Text files", "*.txt"), ("All files", "*.*")])
    if temp is not None:
        f = open(temp.name, "r")
        fpath = temp.name
        codeinp.delete("1.0", END)
        codeinp.insert(INSERT, f.read())
        code = f.read()
        code_ = f.read()
        f.close()
        saved = 1
    save()
    win.title("Brainfuck IDE Portable: " + fpath)
    check()
run = 0
def evaluate(z=None):
    if codeinp.get("1.0", END) != "\n":
        try:
            save()
            code = codeinp.get("1.0", END)
            global run
            run = 1
            code = cleanup(list(code))
            bracemap = []
            cells, codeptr, cellptr = [0], 0, 0
            while codeptr < len(code):
                if run == 1:
                    command = code[codeptr]
                    if command == ">":
                        cellptr += 1
                    if cellptr == len(cells): cells.append(0)
                    if command == "<":
                        cellptr = 0 if cellptr <= 0 else cellptr - 1
                    if command == "+":
                        cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0
                    if command == "-":
                        cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255
                    if command == "[":
                        bracemap.append(codeptr)
                    if command == "]":
                        if cells[cellptr] == 0:
                            bracemap.pop()
                        else:
                            codeptr = bracemap[-1]
                    if command == ".": print_(chr(cells[cellptr]))
                    if command == ",": cells[cellptr] = ord(input())
                    codeptr += 1
                    win.update()
                else:
                    break
        except:
            stop()
            return
        stop()
def help(f=None):
    w = Toplevel(win)
    w.withdraw()
    w.iconbitmap(script + "icon.ico")
    w.title("Help")
    w.resizable(0, 0)
    Label(w, text="""Help:
1. Brainfuck
+   : increase cell value
-   : decrease cell value
<   : move left
>   : move right (can be used infinitely because the cells are dynamic)
[   : enter loop
]   : exit loop if current cell is 0, otherwise go to the last [
.   : print_ the ascii of the current cell (chr(cell))
,   : input 1 char (input())
          
2. Hotkeys:
ctrl-s       : save
ctrl-n       : new
ctrl-o       : open
ctrl-r       : run
ctrl-shift-s : stop
ctrl-shift-c : clear console
ctrl-b       : text to brainfuck
ctrl-h       : help
ctrl-alt-s   : settings""").grid(column=0, row=0)
    w.deiconify()
    w.mainloop()

def settings(a=None):
    global darkmode, keybind
    w = Toplevel(win)
    w.withdraw()
    w.iconbitmap(script + "icon.ico")
    w.title("Settings")
    w.resizable(0, 0)
    darkmode_btt = Radiobutton(w, text="Enable dark mode", variable=darkmode, value=True)
    darkmode_btt_2 = Radiobutton(w, text="Disable dark mode", variable=darkmode, value=False)
    darkmode_btt.grid(column=0, row=0)
    darkmode_btt_2.grid(column=0, row=1)
    darkmode_btt = Radiobutton(w, text="Enable keybinds", variable=keybind, value=True)
    darkmode_btt_2 = Radiobutton(w, text="Disable keybinds", variable=keybind, value=False)
    darkmode_btt.grid(column=0, row=2)
    darkmode_btt_2.grid(column=0, row=3)
    btt = Button(w, text="Apply", command=lambda: updatesettings(str(keybind.get()) + str(darkmode.get())))
    btt.grid(column=0, row=4)
    w.deiconify()
    w.mainloop()

def cleanup(code):
  return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))
def stop(a=None):
   global run
   run = 0
mode = open(script + "settings.txt", "r").read()
def updatesettings(setting):
    global mode
    keybindings_enabled = setting[0] == "1"
    dark_mode_enabled = setting[1] == "1"
    mode = ""
    if not keybindings_enabled:
        win.unbind_all("<Control-s>")
        win.unbind_all("<Control-n>")
        win.unbind_all("<Control-o>")
        win.unbind_all("<Control-r>")
        win.unbind_all("<Control-Shift-S>")
        win.unbind_all("<Control-Shift-C>")
        win.unbind_all("<Control-b>")
        win.unbind_all("<Control-h>")
        win.unbind_all("<Control-Alt-s>")
        mode += "0"
    else:
        win.bind_all("<Control-s>", save)
        win.bind_all("<Control-n>", new)
        win.bind_all("<Control-o>", open_)
        win.bind_all("<Control-r>", evaluate)
        win.bind_all("<Control-Shift-S>", stop)
        win.bind_all("<Control-Shift-C>", clear)
        win.bind_all("<Control-b>", texttobrainfuck)
        win.bind_all("<Control-h>", help)
        win.bind_all("<Control-Alt-s>", settings)

        mode += "1"
    if dark_mode_enabled:
        win.configure(background="black")
        codeinp.configure(background="black", foreground="white")
        inp.configure(background="black", foreground="white")
        output.configure(background="black", foreground="white")
        mode += "1"
    else:
        win.configure(background="white")
        codeinp.configure(background="white", foreground="black")
        inp.configure(background="white", foreground="black")
        output.configure(background="white", foreground="black")
        mode += "0"
def clearcode(a=None):
    codeinp.delete("1.0", END)
def check():
    if code_ != codeinp.get("1.0", END):
        if not win.title().endswith(" *"):
            win.title(win.title() + " *")
    else:
        win.after(1, check)
def cdc(i):
  t = i % 10
  if t > 5: i += 10
  return i - t

def StrToBrf(v):
  s = 10 * '+' + '['
  t = ""
  for i in range(len(v)):
    i_ord = ord(v[i])
    i_cdc = cdc(ord(v[i]))
    i_max = 256 - i_ord
    s += '>' + ('-' * i_max if (i_max < 128) else '+' * (i_cdc // 10))
    t += '>' + ('+' if (i_ord - i_cdc > 0) else '-') * abs(i_ord - i_cdc)
  s += '<' * len(v) + '-]' + t + (len(v) - 1) * '<' + '[.>]'
  return s
def texttobrainfuck(s=None):
    w=Toplevel(win)
    w.title("Text to Brainfuck")
    w.iconbitmap(script + "icon.ico")
    text = ScrolledText(w, width=30, height=10)
    text.grid(column=0, row=0)
    out = ScrolledText(w, width=30, height=10)
    out.grid(column=0, row=1)
    out.config(state="disabled")
    def strtobrf(a):
        a = StrToBrf(a)
        out.config(state="normal")
        out.delete("1.0", END)
        out.insert(INSERT, a)
        out.config(state="disabled")
    btt = Button(w, text="Convert", width=41, command=lambda: strtobrf(text.get("1.0", END)[:-1]))
    btt.grid(column=0, row=2)
    w.mainloop()
keybind = IntVar(value=int(mode[0]))
darkmode = IntVar(value=int(mode[1]))
codeinp = ScrolledText(width=200, height=30)
codeinp.grid(column=0, row=0)
inp = ScrolledText(width=200, height=1)
inp.grid(column=0, row=2)
inp.configure(state="disabled")
output = ScrolledText(width=200, height=15)
output.grid(column=0, row=1)
output.configure(state="disabled")
menu = Menu(win)
win.configure(menu=menu)
file = Menu(menu, tearoff="off")
file.add_command(label="New", underline=0, command=new)
file.add_command(label="Save", underline=0, command=lambda: save(1))
file.add_command(label="Open...", underline=0, command=open_)
file.add_command(label="Exit", underline=0, command=exit_)
code = Menu(menu, tearoff="off")
code.add_command(label="Run", underline=0, command=evaluate)
code.add_command(label="Stop", underline=0, command=stop)
code.add_command(label="Clear console", underline=0, command=clear)
menu.add_cascade(label="File", menu=file)
menu.add_cascade(label="Code", menu=code)
tools = Menu(menu, tearoff="off")
tools.add_command(label="Help", underline=0, command=help)
tools.add_command(label="Settings", underline=0, command=settings)
tools.add_command(label="Text to Brainfuck", underline=0, command=texttobrainfuck)
menu.add_cascade(label="Tools", menu=tools)
win.bind_all("<Control-s>", save)
win.bind_all("<Control-n>", new)
win.bind_all("<Control-o>", open_)
win.bind_all("<Control-r>", evaluate)
win.bind_all("<Control-Shift-S>", stop)
win.bind_all("<Control-Shift-C>", clear)
win.bind_all("<Control-b>", texttobrainfuck)
win.bind_all("<Control-h>", help)
win.bind_all("<Control-Alt-s>", settings)
updatesettings(mode)
win.protocol("WM_DELETE_WINDOW", exit_)
if len(argv) > 1:
    f_ = open(argv[1], "r")
    codeinp.insert(INSERT, f_.read())
    code_ = f_.read()
    win.title("Brainfuck IDE Portable: " + argv[1])
    f_.close()
    saved = 1
    fpath = argv[1]
    save()
win.deiconify()
win.after(10, check)
win.mainloop()