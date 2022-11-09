from os import pathsep
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from tkinter.messagebox import showinfo
from tkinter.messagebox import askquestion
from tkinter.messagebox import showerror, showwarning
from tkinter.messagebox import askokcancel
import tkinter.ttk as ttk
import webbrowser
import configparser
try:
    import os, sys
    import win32print
    import win32api
    import subprocess
    from win10toast import ToastNotifier
    notifier = ToastNotifier()
except:
    pass

def main():
    current_dir = os.getcwd()
    gui = Tk()
    gui.geometry("680x680")
    global fsVar
    fsVar = False
    gui.attributes('-fullscreen',fsVar)

    global openFilename
    openFilename = False

    global selectedText
    selectedText = False

    global wrapVar
    wrapVar = False

    global fontvar
    global sizevar
    config = configparser.ConfigParser()
    config.read("settings.ini")
    Font = config['Font']
    Colors = config['Colors']
    NoobNote = config['NoobNote']
    iconvar = NoobNote["icon"]
    titlevar = NoobNote["title"]
    fontvar = Font["fontvar"]
    sizevar = Font["sizevar"]
    bgvar = Colors["bgvar"]
    fgvar = Colors["fgvar"]
    selectbgvar = Colors["selectbgvar"]
    selectfgvar = Colors["selectfgvar"]
    toolbar_color = Colors["toolbar_color"]
    gui.title(titlevar)
    gui.iconbitmap(iconvar)

    def newFile(e):
        global openFilename
        text.delete("1.0", END)
        gui.title(f'New File - {titlevar}')
        openFilename = "none"

    def openFile(e):
        try:
            text.delete("1.0", END)
            file = filedialog.askopenfilename(initialdir=current_dir, title="Choose A File", filetypes=(("All Files", "*.*"),("Text Files", "*.txt"), ("Python Files", "*.py"), ("Config Files", "*.ini") ,("Ruby Files", "*.rb"), ("HTML Files", "*.html"), ("JSON Files", "*.json"), ("Javascript Files", "*.js"), ("CSS Files", "*.css"), ("Shell Files", "*.sh"), ("Batch Files", "*.bat")))
            if file:
                global openFilename
                openFilename = file
            name = file
            gui.title(f'{name} - {titlevar}')

            file = open(file, 'r')
            content = file.read()
            text.insert(END, content)
            file.close()
        except:
            showerror("Not opened", "No file name given")

    About = "NoobNote is a beginner friendly python project.It is registered under the MIT lisence. Feel free to use it however you like. NoobNote is feature rich and can easily replace Notepad for beginners when learning to code or for writing simple files. Hope you enjoy using it."
    Author = "I am a learning python and wrote this to learn tkinter. Check out some of my other projects at https://github.com/newtoallofthis123. Also Check out my Website for other projects https://newtoallofthis123.github.io/About. Hope you enjoy using it."

    def saveAs(e):
        try:
            file = filedialog.asksaveasfilename(defaultextension=".*", initialdir=current_dir, title="Save file as", filetypes=(("All Files", "*.*"),("Text Files", "*.txt"), ("Python Files", "*.py"), ("Config Files", "*.ini") ,("Ruby Files", "*.rb"), ("HTML Files", "*.html"), ("JSON Files", "*.json"), ("Javascript Files", "*.js"), ("CSS Files", "*.css"), ("Shell Files", "*.sh"), ("Batch Files", "*.bat")))
            if file:
                name = file
                gui.title(f'{name} - {titlevar}')

                file = open(file, 'w')
                file.write(text.get(1.0, END))
                file.close()
        except:
            showerror("Not Saved", "No file name given")

    def saveFile(e):
        try:
            global openFilename
            if openFilename:
                file = openFilename
                file = open(file, 'w')
                file.write(text.get(1.0, END))
                file.close()
            else:
                saveAs(e)
        except:
            showerror("Not Saved", "No file saved")

    def time_cal():
        from time import strftime
        from datetime import datetime
        from datetime import date
        current_t = datetime.now()
        current_date = str(date.today())
        current_t_f = current_t.strftime("%H:%M:%S")
        timeAnddate = (f'{current_t_f} {current_date}')
        return timeAnddate
        
    try:
        import sqlite3
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute("""CREATE TABLE recent(
                path text
            )""")
        except:
            pass
    except:
        pass

    def save_for_later(e):
        global openFilename
        import sqlite3
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute("""CREATE TABLE recent(
                path text
            )""")
        except:
            pass
        c.execute("INSERT INTO recent VALUES (:path)",
        {
            'path': openFilename
        })
        conn.commit()
        recent_menu_content()
    
    def show_recent(e):
        recent_gui = Tk()
        recent_gui.title("Saved Files - NoobNote")
        recent_gui.geometry("400x400")
        recent_gui.iconbitmap("icon.ico")
        def open_in_file(e):
            text.delete("1.0", END)
            file_path = list_.selection_get()
            global openFilename
            openFilename = file_path
            file = open(openFilename, 'r')
            content = file.read()
            text.insert(END, content)
            gui.title(f'{openFilename}-{titlevar}')
            file.close()
        import sqlite3
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM recent")
        saved_file_list = c.fetchall()
        list_ = Listbox(recent_gui, fg="black", bg="white", font=("Cascadia Code", 12), borderwidth=0, selectborderwidth=0, width=60, height=20)
        list_.pack()
        for path in saved_file_list:
            list_.insert(END, path)
        list_.bind('<Double-Button>', open_in_file)
        recent_gui.mainloop()

    def delete_recent(e):
        import sqlite3
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        # c.execute("DELETE from recent;")
        c.execute("DROP TABLE recent")

    def save_exit(e):
        saveFile(False)
        gui.quit()

    def cutText(e):
        global selectedText
        if e:
            selectedText = gui.clipboard_get()
        else:
            if text.selection_get():
                selectedText = text.selection_get()
                text.delete("sel.first", "sel.last")
                gui.clipboard_clear()
                gui.clipboard_append(selectedText)

    def copyText(e):
        global selectedText
        if e:
            selectedText = gui.clipboard_get()
        if text.selection_get():
            selectedText = text.selection_get()
            gui.clipboard_clear()
            gui.clipboard_append(selectedText)

    def pasteText(e):
        global selectedText
        if e:
            selectedText = gui.clipboard_get()
        else:
            if selectedText:
                positionCursor = text.index(INSERT)
                text.insert(positionCursor, selectedText)

    def boldText(e):
        try:
            boldFont = font.Font(text, text.cget("font"))
            boldFont.configure(weight="bold")

            text.tag_configure("bold", font=boldFont)
            current_tags = text.tag_names("sel.first")
            if "bold" in current_tags:
                text.tag_remove("bold",  "sel.first", "sel.last")
            else:
                text.tag_add("bold", "sel.first", "sel.last")
        except:
            showerror("Selection", "No text selected")

    def italicText(e):
        try:
            italicFont = font.Font(text, text.cget("font"))
            italicFont.configure(slant="italic")

            text.tag_configure("italic", font=italicFont)
            current_tags = text.tag_names("sel.first")
            if "italic" in current_tags:
                text.tag_remove("italic",  "sel.first", "sel.last")
            else:
                text.tag_add("italic", "sel.first", "sel.last")
        except:
            showerror("Selection", "No text selected")

    def underlineText(e):
        try:
            underlineFont = font.Font(text, text.cget("font"))
            underlineFont.configure(underline=True)

            text.tag_configure("underline", font=underlineFont)
            current_tags = text.tag_names("sel.first")
            if "underline" in current_tags:
                text.tag_remove("underline",  "sel.first", "sel.last")
            else:
                text.tag_add("underline", "sel.first", "sel.last")
        except:
            showerror("Selection", "No text selected")

    def textColor():
        colorChoice = colorchooser.askcolor()[1]
        bgFont = font.Font(text, text.cget("font"))
        #bgFont.configure(slant="italic")

        text.tag_configure("colored", font=bgFont, foreground=colorChoice)
        current_tags = text.tag_names("sel.first")
        if "colored" in current_tags:
            text.tag_remove("colored",  "sel.first", "sel.last")
        else:
            text.tag_add("colored", "sel.first", "sel.last")

    def ColorAllText():
        colorChoice = colorchooser.askcolor()[1]
        if colorChoice:
            text.config(fg=colorChoice)

    def bgColor():
        colorChoice = colorchooser.askcolor()[1]
        if colorChoice:
            text.config(bg=colorChoice)

    def showInfo():
        showinfo("About NoobNote", About)

    def aboutAuthor():
        showinfo("NoobScience", Author)

    def docOpen(e):
        try:
            text.delete(1.0, END)
            doc = open("README.txt")
            gui.title("NoobNote Docs")
            docContent = doc.read()
            text.insert(END, docContent)
        except:
            showerror("Doc", "README.txt not Found")

    def fullScreen(e):
        global fsVar
        if fsVar:
            gui.attributes('-fullscreen',False)
            fsVar = False
        else:
            fsVar = True
            gui.attributes('-fullscreen',True)

    def lightTheme(e):
        gui.config(bg="white")
        text.config(fg = "black",bg="white", selectbackground=selectbgvar, selectforeground=selectfgvar, insertbackground="black")

    def darkTheme(e):
        gui.config(bg="black")
        text.config(fg="white",bg="black", selectbackground="yellow", selectforeground="black", insertbackground="white")

    def relaxTheme(e):
        gui.config(bg="#F2DD2D")
        text.config(fg="black",bg="#F2DD2D", selectbackground="#FA9133", selectforeground="black", insertbackground="black")

    def hackerTheme():
        gui.config(bg="#282923")
        text.config(fg="#A6E22B",bg="#282923", selectbackground="#CCFF87", selectforeground="black", insertbackground="#A6E22B")

    def timeDate(e):
        from datetime import datetime
        from datetime import date
        current_t = datetime.now()
        current_date = str(date.today())
        current_t_f = current_t.strftime("%H:%M:%S")
        timeAnddate = (f'{current_t_f} {current_date}')
        text.insert(END, timeAnddate)

    def selectAll(e):
        text.tag_add('sel', '1.0', 'end')

    def clearAll(e):
        text.delete(1.0, END)

    def del_text(e):
        try:
            text.delete(SEL_FIRST, SEL_LAST)
        except:
            showerror("Error", "No Text Selected to Search")

    def right_click_menu(e):
        rightClickmenu.tk_popup(e.x_root, e.y_root)

    def openNoobweb():
        webbrowser.open("https://newtoallofthis123.github.io/About")

    def openWeb():
        webbrowser.open("https://newtoallofthis123.github.io/NoobNote")

    def source():
        webbrowser.open("https://github.com/newtoallofthis123/NoobNote")

    def projects():
        webbrowser.open("https://github.com/newtoallofthis123")

    def issues():
        webbrowser.open("https://github.com/newtoallofthis123/NoobNote/issues")

    def printFile(e):
        try:
            printerName = win32print.GetDefaultPrinter()
            printAsk = f'Do you want to print with your deflaut printer: {printerName} ? You can change your default printer in your system preferences'
            printChoice = askquestion("Print File?", printAsk)
            if printChoice == 'yes':
                fileToprint = filedialog.askopenfilename(initialdir=current_dir, title="Select File to Print", filetypes=(("All Files", "*.*"),("Text Files", "*.txt"), ("Python Files", "*.py"), ("Config Files", "*.ini") ,("Ruby Files", "*.rb"), ("HTML Files", "*.html"), ("JSON Files", "*.json"), ("Javascript Files", "*.js"), ("CSS Files", "*.css"), ("Shell Files", "*.sh"), ("Batch Files", "*.bat")))
                if fileToprint:
                    win32api.ShellExecute(0, "print", fileToprint, None, ".", 0)
            elif printChoice == 'no':
                showerror("Printing Aborted", "Printing Aborted")
            else:
                showerror("Error", "Something went wrong. Printing Aborted")
        except:
            showerror("Unable to Print", "Something went wrong.Printer is most likely offline. Try again when the printer is online or report this issue to https://github.com/newtoallofthis123/NoobNote/issues")

    def newWinmain(e):
        main()

    def quit1(e):
        gui.quit()

    def quit2(e):
        e.quit()

    def fontSettings(e):
        text.config(font=(e, sizevar))

    def fontsizeSetting(e, f):
        text.config(font=(e, f))

    def zoomIn(e):
        global sizevar
        sizevar = int(sizevar) + 1
        text.config(font=(fontvar, sizevar))

    def zoomOut(e):
        global sizevar
        sizevar = int(sizevar) - 1
        text.config(font=(fontvar, sizevar))

    def sizeSettings(e):
        text.config(font=e)

    def word_wrap(e):
        global wrapVar
        if wrapVar:
            text.config(wrap=WORD)
            wrapVar = False
        else:
            wrapVar = True
            text.config(wrap="none")


    def openNoobweb():
        webbrowser.open("https://newtoallofthis123.github.io/About")

    def showInfo():
        showinfo("About NoobNote", About)

    def aboutAuthor():
        showinfo("NoobScience", Author)

    def projects():
        webbrowser.open("https://github.com/newtoallofthis123")

    def openleafweb():
        webbrowser.open("https://newtoallofthis123.github.io/leaf")

    def source():
        webbrowser.open("https://github.com/newtoallofthis123/leaf")

    def issue():
        webbrowser.open("https://github.com/newtoallofthis123/leaf/issues")

    def quit1(e):
        gui.quit()

    def doc(e):
        webbrowser.open("https://newtoallofthis123.github.io/leaf")



        about = Menu(_menu, tearoff=False)
        _menu.add_cascade(label="Help", menu=about)
        about.add_command(label="Read the Docs", command=lambda: doc(False))
        about.add_command(label="About Author", command=aboutAuthor)
        about.add_command(label="About Leaf", command=showInfo)
        about.add_command(label="NoobScience Website", command=openNoobweb)
        about.add_command(label="Leaf Website", command=openleafweb)
        about.add_command(label="View Source Code", command=source)
        about.add_command(label="Report a Issue", command=issue)
        about.add_command(label="Some of my other projects", command=projects)


        gui.bind('<Control-q>', quit1)

        gui.mainloop()
        def openNoobweb():
               webbrowser.open("https://newtoallofthis123.github.io/About")

        def showInfo():
               showinfo("About NoobNote", About)

        def aboutAuthor():
                showinfo("NoobScience", Author)

        def projects():
                webbrowser.open("https://github.com/newtoallofthis123")

        def openleafweb():
                webbrowser.open("https://newtoallofthis123.github.io/leaf")

        def source():
                webbrowser.open("https://github.com/newtoallofthis123/leaf")

        def issue():
                webbrowser.open("https://github.com/newtoallofthis123/leaf/issues")

                about = Menu(_menu, tearoff=False)
                _menu.add_cascade(label="Help", menu=about)
                about.add_command(label="Read the Docs", command=lambda: doc(False))
                about.add_command(label="About Author", command=aboutAuthor)
                about.add_command(label="About Leaf", command=showInfo)
                about.add_command(label="NoobScience Website", command=openNoobweb)
                about.add_command(label="Leaf Website", command=openleafweb)
                about.add_command(label="View Source Code", command=source)
                about.add_command(label="Report a Issue", command=issue)
                about.add_command(label="Some of my other projects", command=projects)


            

    def month_calendar(e):
        from datetime import datetime
        from datetime import date
        import time
        import calendar
        date_now = date.today()
        _month = int(date_now.month)
        _year = int(date_now.year)
        cal = calendar.month(_year, _month)
        text.insert(END, cal)

    def year_calendar(e):
        from datetime import datetime
        from datetime import date
        import time
        import calendar
        date_now = date.today()
        _month = int(date_now.month)
        _year = int(date_now.year)
        cal = calendar.calendar(_year)
        text.insert(END, cal)

    def show_year_calendar():
        from datetime import datetime
        from datetime import date
        import time
        import calendar
        year_cal = Tk()
        year_cal.resizable(False, False)
        year_cal.config(bg="black")
        year_cal.iconbitmap('icon.ico')
        date_now = date.today()
        _month = int(date_now.month)
        _year = int(date_now.year)
        year_cal.title("Month Calendar for: " + str(_year))
        cal = calendar.calendar(_year)
        label = Label(year_cal, text=cal, fg="white", bg="black", font=("Cascadia Code", 12))
        label.pack()

    def show_month_calendar():
        from datetime import datetime
        from datetime import date
        import time
        import calendar
        month_cal = Tk()
        month_cal.resizable(False, False)
        month_cal.config(bg="black")
        month_cal.iconbitmap('icon.ico')
        date_now = date.today()
        _month = int(date_now.month)
        _year = int(date_now.year)
        month_cal.title("Year Calendar for: " + str(_month) + "  " + str(_year))
        cal = calendar.month(_year, _month)
        label = Label(month_cal, text=cal, fg="white", bg="black", font=("Cascadia Code", 18))
        label.pack()


    def run(e):
        try:
            if openFilename.endswith(".py"):
                try:
                    os.system("C:/Users/User/AppData/Local/Programs/Python/Python39/python.exe " + openFilename)
                except:
                    showerror("Python Not Found", "Python is not found in your path. Add it or try reinstalling or installing python")
            if openFilename.endswith(".html"):
                try:
                    folder = filedialog.askdirectory(initialdir=current_dir, title="Choose A folder",)
                    os.system("cd..")
                    os.system("cd " + folder)
                    os.system("start https://localhost:8000")
                    os.system("python -m http.server")
                except:
                    showerror("Something went wrong", "SomeThing went wrong. Try agian or report the issue at https://github.com/newtoallofthis123/NoobNote/issues")
            if openFilename.endswith(".java"):
                try:
                    os.system("java " + openFilename)
                except:
                    showerror("Something went wrong", "Check your code and check if java is in your system path")
            if openFilename.endswith(".rb"):
                try:
                    os.system("ruby " + openFilename)
                except:
                    showerror("Something went wrong", "Check your code and check if ruby is in your system path")
            if openFilename.endswith(".bat"):
                try:
                    os.system(openFilename)
                except:
                    showerror("Something went wrong", "Check your code or are you sure you are running on windows?")
            if openFilename.endswith(".sh"):
                try:
                    os.system("cd resources")
                    os.system("bash " + openFilename)
                except:
                    showerror("Something went wrong", "Check your code and check if bash is in your system path")
            if openFilename.endswith(".js"):
                try:
                    os.system("node " + openFilename)
                except:
                    showerror("Something went wrong", "Check your code and check if node is in your system path")
        except:
            showerror("Error", "Are you sure you are running a supported type? Check the docs for more info")

    def clock(e):
        try:
            from time import strftime
            clock_widget = Tk()
            clock_widget.geometry("540x100")
            clock_widget.title("Clock Widget")
            clock_widget.iconbitmap("icon.ico")
            def clockconfig():
                time_clock = strftime('%H:%M:%S %p')
                clock_text.config(text = time_clock)
                clock_text.after(1000, clockconfig)
            clock_text = Label(clock_widget, bg="black", fg="#00FF54", font=("Cascadia", 72),borderwidth=0)
            clock_text.pack()
            clockconfig()
            mainloop()
        except:
            print("ShadowGuy123")

    def search_google():
        try:
            content = text.selection_get()
            url = 'https://www.google.com/search?hl=en&q=' + content
            webbrowser.open(url)
        except:
            showerror("Error", "No Text Selected to Search")
 



    def search_yt():
        try:
            content = text.selection_get()
            url = 'https://www.youtube.com/results?search_query=' + content
            webbrowser.open(url)
        except:
            showerror("Error", "No Text Selected to Search")

   
    def search_github():
        try:
            content = text.selection_get()
            url = 'https://github.com/search?q=' + content
            webbrowser.open(url)
        except:
            showerror("Error", "No Text Selected to Search")

   

    def encode_64():
        try:
            import base64
            string = text.selection_get()
            string_bytes = string.encode("ascii")
            base64_bytes = base64.b64encode(string_bytes)
            base64_string = base64_bytes.decode("ascii")
            text.insert(END, base64_string)
        except:
            showerror("Error occured", "Something went wrong. Try Again or report the issue at https://github.com/newtoallofthis123/NoobNote/issues")

    def decode_64():
        try:
            import base64
            string = text.selection_get()
            string_bytes = string.encode("ascii")
            base64_bytes = base64.b64decode(string_bytes)
            base64_string = base64_bytes.decode("ascii")
            text.insert(END, base64_string)
        except:
            showerror("Error occured", "The selected string is not encoded to decode")

    def hash_md5():
        import hashlib
        content = str(text.selection_get())
        encoded = content.encode()
        hash_str = hashlib.md5(encoded)
        hash_hexa = hash_str.hexdigest()
        text.insert(END, hash_hexa)

   

    def settings_gui(e):
        def save_settings(e):
            settings_file = 'settings.ini'
            file = open(settings_file, 'w')
            if font_entry.get() == "":
                font_entry_ = "Cascadia Code"
            else:
                font_entry_ = font_entry.get()
            if size_entry.get() == "":
                size_entry_ = "14"
            else:
                size_entry_ = size_entry.get()
            if bg_entry.get() == "":
                bg_entry_ = "white"
            else:
                bg_entry_ = bg_entry.get()
            if fg_entry.get() == "":
                fg_entry_ = "black"
            else:
                fg_entry_  = fg_entry.get()
            if select_bg_entry.get() == "":
                select_bg_entry_ = "#F9C500"
            else:
                select_bg_entry_ = select_bg_entry.get()
            if select_fg_entry.get() == "":
                select_fg_entry_ = "black"
            else:
                select_fg_entry_ = select_fg_entry.get()
            if icon_entry.get() == "":
                icon_entry_ = "icon.ico"
            else:
                icon_entry_ = icon_entry.get()
            if title_entry.get() == "":
                title_entry_ = "LiteNote"
            else:
                title_entry_ = title_entry.get()
            if toolbar_entry.get() == "":
                toolbar_entry_ = "#F0F0F0"
            else:
                toolbar_entry_ = toolbar_entry.get()

            content = f'[Font]\nfontvar = {font_entry_}\nsizevar = {size_entry_}\n\n[Colors]\nbgvar = {bg_entry_}\nfgvar = {fg_entry_}\nselectbgvar = {select_bg_entry_}\nselectfgvar = {select_fg_entry_}\ntoolbar_color = {toolbar_entry_}\n\n[NoobNote]\nicon = {icon_entry_}\ntitle = {title_entry_}\n\n[Profile]\nauthorvar = NoobScience\nprojectvar = NoobNote\nlinkvar = https://newtoallofthis123.github.io/About'
            file.write(content)
            file.close()
            try:
                set_gui.destroy()
            except:
                pass
            try:
                runner_gui.destroy()
            except:
                pass
            try:
                find_gui.destroy()
            except:
                pass
            try:
                music_gui.destroy()
            except:
                pass
            try:
                gui.destroy()
            except:
                pass
        set_gui = Tk()
        set_gui.title("Settings - LiteNote")
        set_gui.iconbitmap("icon.ico")
        set_gui.geometry("400x280")
        set_root = Frame(set_gui,)
        set_root.pack()
        font_label = Label(set_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text="Font")
        font_label.grid(row=0, column=0)
        font_entry = Entry(set_root, font=("Cascadia Code", 12), fg="black", bg="white", borderwidth=0)
        font_entry.grid(row=0, column=1, padx=10, pady=1)
        font_entry.insert(0, fontvar)
        size_label = Label(set_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text="Size")
        size_label.grid(row=1, column=0)
        size_entry = Entry(set_root, font=("Cascadia Code", 12), fg="black", bg="white", borderwidth=0)
        size_entry.grid(row=1, column=1, padx=10, pady=1)
        size_entry.insert(0, sizevar)
        fg_label = Label(set_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text="Font Color")
        fg_label.grid(row=2, column=0)
        fg_entry = Entry(set_root, font=("Cascadia Code", 12), fg="black", bg="white", borderwidth=0)
        fg_entry.grid(row=2, column=1, padx=10, pady=1)
        fg_entry.insert(0, fgvar)
        bg_label = Label(set_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text="Background Color")
        bg_label.grid(row=3, column=0)
        bg_entry = Entry(set_root, font=("Cascadia Code", 12), fg="black", bg="white", borderwidth=0)
        bg_entry.grid(row=3, column=1, padx=10, pady=1)
        bg_entry.insert(0, bgvar)
        select_fg_label = Label(set_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text="Selection Font Color")
        select_fg_label.grid(row=4, column=0)
        select_fg_entry = Entry(set_root, font=("Cascadia Code", 12), fg="black", bg="white", borderwidth=0)
        select_fg_entry.grid(row=4, column=1, padx=10, pady=1)
        select_fg_entry.insert(0, selectfgvar)
        select_bg_label = Label(set_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text="Selection Background Color")
        select_bg_label.grid(row=5, column=0)
        select_bg_entry = Entry(set_root, font=("Cascadia Code", 12), fg="black", bg="white", borderwidth=0)
        select_bg_entry.grid(row=5, column=1, padx=10, pady=1)
        select_bg_entry.insert(0, selectbgvar)
        toolbar_label = Label(set_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text="Toolbar Color")
        toolbar_label.grid(row=6, column=0)
        toolbar_entry = Entry(set_root, font=("Cascadia Code", 12), fg="black", bg="white", borderwidth=0)
        toolbar_entry.grid(row=6, column=1, padx=10, pady=1)
        toolbar_entry.insert(0, toolbar_color)
        icon_label = Label(set_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text="Icon Path")
        icon_label.grid(row=7, column=0)
        icon_entry = Entry(set_root, font=("Cascadia Code", 12), fg="black", bg="white", borderwidth=0)
        icon_entry.grid(row=7, column=1, padx=10, pady=1)
        icon_entry.insert(0, iconvar)
        title_label = Label(set_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text="Title")
        title_label.grid(row=8, column=0)
        title_entry = Entry(set_root, font=("Cascadia Code", 12), fg="black", bg="white", borderwidth=0)
        title_entry.grid(row=8, column=1, padx=10, pady=1)
        title_entry.insert(0, titlevar)
        save = Button(set_gui, font=("Cascadia Code", 12), fg="black", bg="white", text="Save", borderwidth=0, command=lambda: save_settings(False))
        save.pack()
        set_gui.mainloop()

    def runner(e):
        runner_gui = Tk()
        runner_gui.iconbitmap('icon.ico')
        runner_gui.title("Runner")
        runner_gui.resizable(False, False)
        runner_gui.geometry("300x40+200+200")
        def right_click_menu(e):
            runner_rightClickmenu.tk_popup(e.x_root, e.y_root)
        def run_command(e):
            command_ = str.lower(command_input.get())
            if command_ == "!open":
                openFile(False)
            if command_ == "!new":
                newFile(False)
            if command_ == "!saveas":
                saveAs(False)
            if command_ == "!save":
                saveFile(False)
            if command_ == "!run":
                run(False)
            if command_ == "!options":
                settings_gui(False)
            if command_ == "!quit":
                runner_gui.quit()
            if command_ == "!settings":
                settings_gui(False)
            if command_ == "!help":
                text.delete("1.0", END)
                file = 'README.txt'
                name = file
                gui.title(f'{name} - {titlevar}')
                file = open(file, 'r')
                content = file.read()
                text.insert(END, content)
                file.close()
            if "!g" in command_:
                content = command_.split("!g ")
                actual_content = content[1]
                url = 'https://www.google.com/search?hl=en&q=' + actual_content
                webbrowser.open(url)
            if "!yt" in command_:
                content = command_.split("!yt ")
                actual_content = content[1]
                url = 'https://www.youtube.com/results?search_query=' + actual_content
                webbrowser.open(url)
            if "!web" in command_:
                content = command_.split("!web ")
                actual_content = content[1]
                webbrowser.open(actual_content)
            if "!file" in command_:
                content = command_.split("!file ")
                actual_content = content[1]
                text.delete("1.0", END)
                file = actual_content
                name = file
                gui.title(f'{name} - {titlevar}')
                file = open(file, 'r')
                content = file.read()
                text.insert(END, content)
                file.close()
            if "!cmd" in command_:
                content = command_.split("!cmd ")
                actual_content = content[1]
                os.system(f'{actual_content}')
            if "!m" in command_:
                content = command_.split("!m ")
                actual_content = content[1]
                webbrowser.open(f'mailto:{actual_content}')
            if "!theme" in command_:
                content = command_.split("!theme ")
                actual_content = content[1]
                if actual_content == "light":
                    lightTheme(False)
                if actual_content == "dark":
                    darkTheme(False)
                if actual_content == "relax":
                    relaxTheme(False)
                if actual_content == "hacker":
                    hackerTheme(False)
            if command_ == "!h":
                text.delete("1.0", END)
                file = "hotkeys.txt"
                name = file
                gui.title(f'HotKeys - {titlevar}')
                file = open(file, 'r')
                content = file.read()
                text.insert(END, content)
                file.close()

    def find(e):
        find_gui = Tk()
        find_gui.title("Find")
        find_gui.iconbitmap("icon.ico")
        content = text.get("1.0", END)
        content_list = content.split(" ")
        print(content_list)
        dev_label = Label(find_gui, font=("Cascadia Code", 12), fg="red", bg="#F0F0F0", text="Under Development")
        dev_label.pack()
        find_root = Frame(find_gui)
        find_root.pack()
        find_label = Label(find_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text="Find: ")
        find_label.grid(row=1, column=0)
        find_input = Entry(find_root, font=("Cascadia Code", 12), fg="black", bg="white", borderwidth=0,)
        find_input.grid(row=1, column=1)
        def search(list,n):
            for i in range(len(list)):
                if list[i] == n:
                    return True
            return False
        if search(content_list, find_input.get()) == True:
            print("Hello World")

    def mini_terminal(e):
        terminal = Tk()
        terminal.title("Mini Terminal")
        terminal.iconbitmap("icon.ico")
        terminal.geometry("250x80")
        terminal.resizable(False, False)
        def terminal_run(e):
            command_given = str(terminal_command.get())
            terminal_command.delete(0,END)
            try:
                os.system(command_given)
                try:
                    os.system("pause")
                except:
                    pass
            except:
                showerror("Something went wrong", "Something went wrong. Try again with a correct system command")
        terminal_title = Label(terminal, bg="#F0F0F0", fg="black", borderwidth=0, font=("Cascadia Code", 14), text="Enter System Command")
        terminal_title.pack()
        terminal_command = Entry(terminal, bg="white", fg="black", borderwidth=0, width=30,font=("Cascadia Code", 12))
        terminal_command.pack()
        dev_label = Label(terminal, font=("Cascadia Code", 12), fg="red", bg="#F0F0F0", text="Under Development")
        dev_label.pack()
        terminal_command.bind("<Return>", terminal_run)
        terminal.mainloop()

    def update(e):
        import update_check
        update_check.check_updates()


    def cal(e):
        import cal
        cal.cal_func()

    def read_selected():
        import pyttsx3
        engine = pyttsx3.init()
        selected_text_to_read = text.selection_get()
        engine.say(selected_text_to_read)
        engine.runAndWait()
    def read_all():
        import pyttsx3
        engine = pyttsx3.init()
        selected_text_to_read = text.get(1.0, END)
        engine.say(selected_text_to_read)
        engine.runAndWait()

    def about_():
        about = f'{titlevar} is a simple Notepad written purely in python with tkinter.\nIt is very feature rich though being light weight at the same time.\n{titlevar} is a beginner friendly project and is very easy to understand.\nIt is registered under the MIT License, Hence you are free to use it.\nTo learn more on how to contribute, see CONTRIBUTE.md and README.md\nTo learn to use {titlevar} functions, see MODULE.md or pypi.org/NoobNote\n'
        author = f'I wrote NoobNote to learn tkinter(python gui module) and python.\nI also wanted to have a good alternative to Notepad, but not notepad++.\nHence NoobNote, it is as light weight, fast and as simple as Notepad,\nbut at the same time, a bit more feature rich, private and secure.\nNoobNote took a considerable amount of time and effort to make.\nso, if you want to contribute, be sure to check out CONTRIBUTE.md\n'
        details = f'Author: NoobScience\nProjectName: NoobNote\nWebsite: tinu.be/NoobNote\nAuthor Website: tinu.be/About\nGithub: @newtoallofthis123\n'
        about_gui = Tk()
        about_gui.title(f'About {titlevar}')
        about_gui.iconbitmap(f'{iconvar}')
        about_gui.geometry("780x600")
        about_gui.resizable(False, False)
        def quit_3(e):
            about_gui.destroy()
        title = Label(about_gui, font=("Cascadia Code", 18), fg="black", bg="#F0F0F0", text=titlevar)
        title.pack()
        subtitle = Label(about_gui, font=("Lucida Handwriting", 10), fg="black", bg="#F0F0F0", text="A Simple Light Weight NotePad, by NoobScience\n")
        subtitle.pack()
        about_root = Frame(about_gui,)
        about_root.pack()
        about_title = Label(about_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text="About: ")
        about_title.grid(row=0, column=0)
        about_title_content = Label(about_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text=about)
        about_title_content.grid(row=0, column=1)
        about_title = Label(about_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text="About Author: ")
        about_title.grid(row=1, column=0)
        about_title_content = Label(about_root, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text=author)
        about_title_content.grid(row=1, column=1)
        about_details = Label(about_gui, font=("Cascadia Code", 14), fg="black", bg="#F0F0F0", text="Details")
        about_details.pack()
        about_details_content = Label(about_gui, font=("Cascadia Code", 12), fg="black", bg="#F0F0F0", text=details)
        about_details_content.pack()
        about_root_2 = Frame(about_gui, bg="red")
        about_root_2.pack()
        about_author_website_btn = Button(about_root_2, text="Author-Web\t", font=("Cascadia Code", 12),fg="black", bg="white", borderwidth=0, command=openNoobweb)
        about_author_website_btn.grid(row=0, column=0)
        about_NoobNote_website_btn = Button(about_root_2, text="NoobNote-Web\t", font=("Cascadia Code", 12),fg="black", bg="white", borderwidth=0, command=openWeb)
        about_NoobNote_website_btn.grid(row=0, column=1)
        about_author_github_btn = Button(about_root_2, text="Author-Github\t", font=("Cascadia Code", 12),fg="black", bg="white", borderwidth=0, command=projects)
        about_author_github_btn.grid(row=0, column=2)
        about_NoobNote_github_btn = Button(about_root_2, text="NoobNote-Github\t", font=("Cascadia Code", 12),fg="black", bg="white", borderwidth=0, command=source)
        about_NoobNote_github_btn.grid(row=0, column=3)
        about_gui.bind('<Return>', quit_3)

    toolbar = Frame(gui, bg=toolbar_color, borderwidth=0)
    toolbar.pack(fill=X)

    root = Frame(gui,)
    root.pack()

    scroll_text = Scrollbar(gui,)
    scroll_text.pack(side=RIGHT, fill=Y)

    horizontal_scroll = Scrollbar(gui,orient='horizontal')
    horizontal_scroll.pack(side=BOTTOM, fill=X, ipadx=10)

    textWidth = gui.winfo_screenwidth()
    textHeight = int(gui.winfo_screenheight())

    text = Text(gui, width=textWidth, height=textHeight, font=(fontvar, sizevar), borderwidth=0,selectbackground=selectbgvar, selectforeground=selectfgvar, undo=True, yscrollcommand=scroll_text.set, xscrollcommand=horizontal_scroll.set, fg=fgvar, bg=bgvar,)
    text.pack()

    menu = Menu(gui,)
    gui.config(menu=menu,)

    fileMenu = Menu(menu, tearoff=False,)
    menu.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="New", command=lambda: newFile(False))
    #fileMenu.add_command(label="New Window", command=lambda: newWinmain(False))
    fileMenu.add_command(label="Open", command=lambda: openFile(False))
    fileMenu.add_command(label="Save", command=lambda: saveFile(False))
    fileMenu.add_command(label="SaveAs", command=lambda: saveAs(False))
    fileMenu.add_separator()
    recentMenu = Menu(fileMenu, tearoff=False)
    fileMenu.add_cascade(label="Recently Saved", menu=recentMenu)
    fileMenu.add_command(label="All Saved Files", command=lambda: show_recent(False))
    fileMenu.add_command(label="Save for later", command=lambda: save_for_later(False))
    fileMenu.add_command(label="Delete Saved List", command=lambda: delete_recent(False))
    fileMenu.add_separator()
    fileMenu.add_command(label="Print", command=lambda: printFile(False))
    fileMenu.add_separator()
    fileMenu.add_command(label="Save & Exit", command=lambda: save_exit(False))
    fileMenu.add_command(label="Exit", command=gui.quit())

    editMenu = Menu(menu, tearoff=False)
    menu.add_cascade(label="Edit", menu=editMenu)
    editMenu.add_command(label="Cut", command=lambda: cutText(False))
    editMenu.add_command(label="Copy", command=lambda: copyText(False))
    editMenu.add_command(label="Paste", command=lambda: pasteText(False))
    editMenu.add_command(label="Select All", command=lambda: selectAll(False))
    editMenu.add_command(label="Clear All", command=lambda: clearAll(False))
    editMenu.add_command(label="Delete Selected", command= lambda: del_text(False))
    editMenu.add_separator()
    editMenu.add_command(label="Undo", command=text.edit_undo)
    editMenu.add_command(label="Redo", command=text.edit_redo)
    editMenu.add_separator()
    editMenu.add_command(label="Read Out Everything", command=read_all)
    editMenu.add_command(label="Read Out Selected", command=read_selected)

    textFormatMenu = Menu(menu, tearoff=False)
    menu.add_cascade(label="Format", menu=textFormatMenu)
    textFormatMenu.add_command(label="Bold", command=lambda: boldText(False))
    textFormatMenu.add_command(label="Italic", command=lambda: italicText(False))
    textFormatMenu.add_command(label="Underline", command=lambda: underlineText(False))
    textFormatMenu.add_separator()
    textFormatMenu.add_command(label="Zoom In", command= lambda: zoomIn(False))
    textFormatMenu.add_command(label="Zoom Out", command= lambda: zoomOut(False))
    textFormatMenu.add_separator()
    textFormatMenu.add_command(label="Encode in Base64", command=encode_64)
    textFormatMenu.add_command(label="Decode Base64 String", command=decode_64)
    textFormatMenu.add_separator()
    textFormatMenu.add_checkbutton(label="Word Wrap", command= lambda: word_wrap(False))

    FontSettings = Menu(menu, tearoff=False)
    menu.add_cascade(label="Font", menu=FontSettings)
    FontSettings.add_command(label="Arial", command=lambda: fontSettings("Arial"))
    FontSettings.add_command(label="Lucida Console", command=lambda: fontSettings("Lucida Console"))
    FontSettings.add_command(label="Cascadia Code", command=lambda: fontSettings("Cascadia Code"))
    FontSettings.add_command(label="Microsoft Sans Serif", command=lambda: fontSettings("Microsoft Sans Serif"))
    FontSettings.add_command(label="Consolas", command=lambda: fontSettings("Consolas"))
    FontSettings.add_command(label="Comic Sans MS", command=lambda: fontSettings("Comic Sans MS"))
    FontSettings.add_command(label="Calibri", command=lambda: fontSettings("Calibri"))
    FontSettings.add_command(label="Times New Roman", command=lambda: fontSettings("Times New Roman"))
    FontSettings.add_command(label="Lucida Calligraphy", command=lambda: fontSettings("Lucida Calligraphy"))
    FontSettings.add_command(label="Lucida Handwriting", command=lambda: fontSettings("Lucida Handwriting"))

    viewMenu = Menu(menu, tearoff=False)
    menu.add_cascade(label="View", menu=viewMenu)
    viewMenu.add_command(label="Toggle FullScreen", command=lambda: fullScreen(False))
    viewMenu.add_command(label="Docs", command=lambda: docOpen(False))
    viewMenu.add_separator()
    viewMenu.add_command(label="Time and Date", command=lambda: timeDate(False))
    viewMenu.add_separator()
    viewMenu.add_command(label="Clock Widget", command=lambda: clock(False))
    viewMenu.add_separator()
    viewMenu.add_command(label="Show Month Calendar", command=show_month_calendar)
    viewMenu.add_command(label="Show Year Calendar", command=show_year_calendar)
    viewMenu.add_separator()
    viewMenu.add_command(label="Options", command=lambda: settings_gui(False))

    searchMenu = Menu(menu, tearoff=False)
    menu.add_cascade(label="Search", menu=searchMenu)
    searchMenu.add_command(label="Search with Google", command=search_google)
    searchMenu.add_command(label="Search with YouTube", command=search_yt)
    searchMenu.add_command(label="Search with Github", command=search_github)

    toolsMenu = Menu(menu, tearoff=False)
    menu.add_cascade(label="Tools", menu=toolsMenu)
    toolsMenu.add_command(label="Calculator", command=lambda: cal(False))
    toolsMenu.add_separator()
    toolsMenu.add_command(label="Insert Month Calendar", command=lambda: month_calendar(False))
    toolsMenu.add_command(label="Insert Year Calendar", command=lambda: year_calendar(False))
    toolsMenu.add_separator()
    toolsMenu.add_command(label="Run File", command=lambda: run(False))
    toolsMenu.add_separator()
    toolsMenu.add_command(label="Generate md5 Hash", command=hash_md5)
    toolsMenu.add_separator()
    toolsMenu.add_command(label="Mini Terminal", command=lambda: mini_terminal(False))

    colorMenu = Menu(menu, tearoff=False)
    menu.add_cascade(label="Color", menu=colorMenu)
    colorMenu.add_command(label="All Text Color", command=ColorAllText)
    colorMenu.add_command(label="BackGround", command=bgColor)
    colorMenu.add_command(label="Selected Text Color", command=textColor)
    colorMenu.add_separator()
    colorMenu.add_command(label="Light Theme", command=lambda: lightTheme(False))
    colorMenu.add_command(label="Dark Theme", command=lambda: darkTheme(False))
    colorMenu.add_command(label="Relaxing Theme", command=lambda: relaxTheme(False))
    colorMenu.add_command(label="Hacker Theme", command=hackerTheme)

    aboutMenu = Menu(menu, tearoff=False)
    menu.add_cascade(label="Help", menu=aboutMenu)
    aboutMenu.add_command(label="About", command=about_)
    aboutMenu.add_separator()
    aboutMenu.add_command(label="Check for Updates", command=lambda: update(False))
    aboutMenu.add_separator()
    aboutMenu.add_command(label="NoobNote Website", command=openWeb)
    aboutMenu.add_command(label="Fork NoobNote", command=source)
    aboutMenu.add_command(label="Report any issues", command=issues)

    scroll_text.config(command=text.yview)
    horizontal_scroll.config(command=text.xview)

    rightClickmenu = Menu(gui, tearoff=False)
    rightClickmenu.add_command(label="Open File", command= lambda: openFile(False))
    rightClickmenu.add_command(label="New File", command= lambda: newFile(False))
    rightClickmenu.add_command(label="Save File", command= lambda: saveFile(False))
    rightClickmenu.add_separator()
    rightClickmenu.add_command(label="Copy", command= lambda: copyText(False))
    rightClickmenu.add_command(label="Cut", command= lambda: cutText(False))
    rightClickmenu.add_command(label="Paste", command= lambda: pasteText(False))
    rightClickmenu.add_separator()
    rightClickmenu.add_command(label="Bold", command=lambda: boldText(False))
    rightClickmenu.add_command(label="Italic", command=lambda: italicText(False))
    rightClickmenu.add_command(label="Underline", command=lambda: underlineText(False))
    rightClickmenu.add_separator()
    rightClickmenu.add_command(label="Select All", command= lambda: selectAll(False))
    rightClickmenu.add_command(label="Clear All", command= lambda: clearAll(False))
    rightClickmenu.add_command(label="Delete Selected", command= lambda: del_text(False))
    rightClickmenu.add_separator()
    rightClickmenu.add_command(label="Run", command= lambda: run(False))
    rightClickmenu.add_separator()
    rightClickmenu.add_command(label="Insert Time", command= lambda: timeDate(False))
    rightClickmenu.add_command(label="Insert Month Calendar", command= lambda: month_calendar(False))
    rightClickmenu.add_separator()
    rightClickmenu.add_command(label="Toggle FullScreen", command= lambda: fullScreen(False))
    rightClickmenu.add_separator()
    rightClickmenu.add_checkbutton(label="Word Wrap")
    rightClickmenu.add_separator()
    rightClickmenu.add_command(label="Light Theme", command= lambda: lightTheme(False))
    rightClickmenu.add_command(label="Dark Theme", command= lambda: darkTheme(False))
    rightClickmenu.add_separator()
    rightClickmenu.add_command(label="About", command= about_)
    rightClickmenu.add_command(label="Settings", command= lambda: settings_gui(False))
    rightClickmenu.add_separator()
    rightClickmenu.add_command(label="Quit", command= lambda: quit1(False))
    rightClickmenu.add_command(label="Save & Exit", command= lambda: save_exit(False))

    def recent_menu_content():
        try:
            def open_in_file(e):
                text.delete("1.0", END)
                file_path = e[0]
                global openFilename
                openFilename = file_path
                file = open(openFilename, 'r')
                content = file.read()
                text.insert(END, content)
                gui.title(f'{openFilename}-{titlevar}')
                file.close()
            import sqlite3
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("SELECT * FROM recent")
            saved_file_list = c.fetchall()
            for path in saved_file_list:
                file_path = path
            recentMenu.add_command(label=file_path, command=lambda: open_in_file(file_path))
        except:
            pass
    recent_menu_content()

    gui.bind('<Control-Key-x>', cutText)
    gui.bind('<Control-Key-c>', copyText)
    gui.bind('<Control-Key-v>', pasteText)
    gui.bind('<F11>', fullScreen)
    gui.bind('<F11>', fullScreen)
    gui.bind('<Control-L>', lightTheme)
    gui.bind('<Control-l>', lightTheme)
    gui.bind('<Control-d>', darkTheme)
    gui.bind('<Control-D>', darkTheme)
    gui.bind('<Control-A>', selectAll)
    gui.bind('<Control-a>', selectAll)
    gui.bind('<Control-g>', clearAll)
    gui.bind('<Control-G>', clearAll)
    gui.bind('<Delete>', del_text)
    gui.bind('<Control-b>', boldText)
    gui.bind('<Control-i>', italicText)
    gui.bind('<Control-u>', underlineText)
    gui.bind('<Control-h>', docOpen)
    gui.bind('<Control-H>', docOpen)
    gui.bind('<Control-o>', openFile)
    gui.bind('<Control-n>', newFile)
    gui.bind('<Control-S>', saveAs)
    gui.bind('<Control-s>', saveFile)
    gui.bind('<Control-N>', newWinmain)
    gui.bind('<Control-q>', quit1)
    gui.bind('<Control-p>', printFile)
    gui.bind('<Control-t>', mini_terminal)
    gui.bind('<Control-m>', month_calendar)
    gui.bind('<Control-y>', year_calendar)
    gui.bind('<Control-j>', clock)
    gui.bind('<Control-w>', timeDate)
    gui.bind('<Button-3>', right_click_menu)
    gui.bind('<Control-Key-plus>', zoomIn)
    gui.bind('<Control-Key-minus>', zoomOut)
    gui.bind('<Control-r>', runner)
    gui.bind('<Control-f>', find)
    gui.bind('<F5>', run)

    gui.mainloop()

if __name__ == '__main__':
    main()
