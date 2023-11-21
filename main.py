import datetime
import io
from tkinter import *
from tkinter import ttk
from tkinter.tix import IMAGETEXT
import webbrowser
import pandas as pd
from tkcalendar import *
from tkinter import messagebox
from time import strftime
import os
import sys
import json
import errno
import weather
import location
import customtkinter
import requests
from PIL import ImageTk,Image
import urllib
import sys

# Create Nominatim object for geolocation


# Default stock ticker list
# tickerlist = ["MSFT", "AAPL", "TSLA", "GOOGL"]
sys.setrecursionlimit(5000)
def time():
    currenttime = strftime('%I:%M:%S %p')
    timeLabel.configure(text=currenttime)
    timeLabel.after(1000, time)


def greeting():
    currenthour = int(strftime('%H'))
    # Greeting based on the time of the day
    if 5 <= currenthour < 12:
        greetLabel.configure(text="Good morning")
    elif 12 <= currenthour < 16:
        greetLabel.configure(text="Good afternoon")
    elif 16 <= currenthour <= 23 or 0 <= currenthour < 5:
        greetLabel.configure(text="Good evening")


def date():
    # sets date
    currentdate = strftime('%A, %d %B %Y')
    dateLabel.configure(text=currentdate)


def mkdir_p(path):
    # creates path for assets and other important stuff
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


# def setstuff():
#     ct_root = Toplevel()
#     # ct_root.geometry('300x200')
#     with open("user_custom.json", 'r') as setting:
#         current_default = json.load(setting)

#     ct_root.title("Theme")
#     Label(ct_root, text='Theme', font="Algerian 20").grid(
#         row=0, column=0, columnspan=2, pady=(12, 25), padx=20)


#     Label(ct_root, text='Theme  ').grid(row=1, column=0, sticky=W)
#     th_val = StringVar()

#     th_val.set(str(current_default["colormode"]))

#     print(th_val.get())
#     th_menu = OptionMenu(ct_root, th_val, "Light", "Dark", "Auto")
#     th_menu.grid(row=2, column=1)

    # def save_changes():
    #     ans = messagebox.askokcancel("Confirmaton", "Confirm changes ?")
    #     if ans:

    #         print(current_default)
    #         # current_default["tickerlist"] = stock_entry.get().split(" ")
    #         current_default["colormode"] = str(th_val.get())

    #         a = current_default['tickerlist']
    #         if len(a) > 5:
    #             s = messagebox.askokcancel(
    #                 "Interruption ", 'Accept only the first 5 stocks? ')
    #             if not (s):
    #                 return

    #             else:
    #                 b = a[0:5]

    #                 print(b)

    #                 current_default["tickerlist"] = b

    #         with open("user_custom.json", 'w') as setting:
    #             json.dump(current_default, setting, indent=4)
    #         print(current_default)
    #         ct_root.destroy()
    #         root.destroy()
    #         os.execl(sys.executable, 'python', __file__)

    #     else:
    #         return

    # cb = Button(ct_root, text="Cancel", command=ct_root.destroy)
    # cb.grid(row=4, column=0)
    # sb = Button(ct_root, text="Save", command=save_changes)
    # sb.grid(row=4, column=1)

    # ct_root.mainloop()


stockdownloadlist = {}
flagdaynight = True
colormode = 1
# def news1():
#     news.newsparse(framenews, bgcol, fgcol, country_code,5)
# def news2():
#     New_joiner.newsparse1(framenews, bgcol, fgcol, country_code)    


if __name__ == '__main__':  # this is the main function of the program
    tickerlist = "{}"
    color = 'light'
    if color.lower() == 'dark':
        colormode = 1
    elif color.lower() == 'light':
        colormode = -1
    else:
        colormode = 0
    mkdir_p("assets")
    # gets information from the location file
    city_name, country_name, country_code = location.location()
    hour = int(strftime('%H'))

    # function to change between lightmode and dark mode depending upon user preferences and time
    if ((0 <= hour < 6 or 18 < hour <= 23) and colormode == 0) or colormode == 1:
        bgcol = "#2596be"
        fgcol = "white"
        flagdaynight = False
    else:
        bgcol = "white"
        fgcol = "black"

    # Tkinter boilerplate shit
    root = Tk()
    root.geometry("1370x730")
    root.title("ZF News")
    root.configure(bg=bgcol)
    root.resizable(False,False)
    bgp = PhotoImage('photozf.png')
    Label(root,image=bgp).place(x=0,y=0)
    # Frames

    # frame for daytime
    framedaytime = Frame(root)
    framedaytime.grid(row=0, column=1, columnspan=2, padx=(5, 0), sticky="n")
    framedaytime.configure(bg=bgcol)

    # frame for weather
    frameweather = Frame(root)
    frameweather.grid(row=0, column=0, padx=(30, 0), sticky="n")
    frameweather.configure(bg=bgcol)

    # frame for calander
    framecal = Frame(master=root)
    framecal.grid(row=0, column=3, rowspan=9, pady=(10, 90),sticky='n')
    framecal.config(bg=bgcol)

    framestock = Frame(root)
    framestock.grid(row=1, column=0, columnspan=1, sticky="n")
    framestock.configure(bg=bgcol)
        

    framenews = Frame(root)
    framenews.grid(row=1, column=1, padx=(30, 20), columnspan=2, sticky="n")
    framenews.configure(bg=bgcol)

    tv1 = ttk.Treeview(framecal)
    tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).
    # treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
    # treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
    # tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget

    
    def clear():
        for child in framenews.winfo_children():
            child.destroy()


    def newsparse2(number):
        clear() #function to process all the news
        
        newsLabel = Label(framenews, text = "DIV C - News", font =("century gothic bold", 20), bg=bgcol, fg=fgcol) #sets heading
        newsLabel.pack(pady = (0,10))

        try:
            img_url = data1['articles'][number]['urlToImage']
            raw_data = urllib.request.urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((450,250))
            photo = ImageTk.PhotoImage(im)
        except:
            img_url = 'https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg'
            raw_data = urllib.request.urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((450, 250))
            photo = ImageTk.PhotoImage(im)    
        image_new = Button(framenews,image = photo,justify='left',borderwidth = 2,bg = "Black")
        image_new.image = photo
        image_new.bind("<Button-1>", lambda e,url=data1['articles'][number]['url']:open_site(url))
        image_new.pack(pady=(0,5),padx = (0,20))
        heading = Button(framenews,text=data1['articles'][number]['title'],bg='white',fg='black',wraplength=450,justify='left',borderwidth = 0)
        heading.bind("<Button-1>", lambda e,url=data1['articles'][number]['url']:open_site(url))
        heading.pack(pady=(0,5),padx = (0,20))
        heading.config(font=('verdana',15))
        details = Button(framenews, text=data1['articles'][number]['description'], bg='white', fg='black', wraplength=450,justify='left',borderwidth = 0)
        details.pack(pady=(0, 5),padx = (0,20))
        details.bind("<Button-1>", lambda e,url=data1['articles'][number]['url']:open_site(url))
        details.config(font=('verdana', 12))
        if number != 0:
            prev = Button(text='Previous',width=33,height=3,command=lambda :newsparse2(number-1),bg='white',borderwidth=0)
            prev.place(x = 320, y = 670)
        if number != len(data1['articles'])-1:
            next = Button(text='Next',width=33,height=3,command=lambda :newsparse2(number+1),bg='white',borderwidth=0)   
            next.place(x = 570, y = 670)
    def newsparse3(number):
        clear() #function to process all the news
        newsLabel = Label(framenews, text = "DIV E/A/U/I - News", font =("century gothic bold", 20), bg=bgcol, fg=fgcol) #sets heading
        newsLabel.pack(pady = (0,10))

        try:
            img_url = data2['articles'][number]['urlToImage']
            raw_data = urllib.request.urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((450,250))
            photo = ImageTk.PhotoImage(im)
        except:
            img_url = 'https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg'
            raw_data = urllib.request.urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((450, 250))
            photo = ImageTk.PhotoImage(im)    
        image_new = Button(framenews,image = photo,justify='left',borderwidth = 2, bg = "Black")
        image_new.image = photo
        image_new.bind("<Button-1>", lambda e,url=data2['articles'][number]['url']:open_site(url))
        image_new.pack(pady=(0,5),padx = (0,20))
        heading = Button(framenews,text=data2['articles'][number]['title'],bg='white',fg='black',wraplength=450,justify='left',borderwidth = 0)
        heading.bind("<Button-1>", lambda e,url=data2['articles'][number]['url']:open_site(url))
        heading.pack(pady=(0,5),padx = (0,20))
        heading.config(font=('verdana',15))
        details = Button(framenews, text=data2['articles'][number]['description'], bg='white', fg='black', wraplength=450,justify='left',borderwidth = 0)
        details.pack(pady=(0, 5),padx = (0,20))
        details.bind("<Button-1>", lambda e,url=data2['articles'][number]['url']:open_site(url))
        details.config(font=('verdana', 12))
        if number != 0:
            prev = Button(text='Previous',width=33,height=3,command=lambda :newsparse3(number-1),bg='white',borderwidth=0)
            prev.place(x = 320, y = 670)
        if number != len(data2['articles'])-1:
            next = Button(text='Next',width=33,height=3,command=lambda :newsparse3(number+1),bg='white',borderwidth=0)   
            next.place(x = 570, y = 670) 
    def newsparse4(number):
        clear() #function to process all the news
        newsLabel = Label(framenews, text = "DIV T - News", font =("century gothic bold", 20), bg=bgcol, fg=fgcol) #sets heading
        newsLabel.pack(pady = (0,10))

        try:
            img_url = data3['articles'][number]['urlToImage']
            raw_data = urllib.request.urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((450,250))
            photo = ImageTk.PhotoImage(im)
        except:
            img_url = 'https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg'
            raw_data = urllib.request.urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((450, 250))
            photo = ImageTk.PhotoImage(im)    
        image_new = Button(framenews,image = photo,justify='left',borderwidth = 2,bg = "Black")
        image_new.image = photo
        image_new.bind("<Button-1>", lambda e,url=data3['articles'][number]['url']:open_site(url))
        image_new.pack(pady=(0,5),padx = (0,20))
        heading = Button(framenews,text=data3['articles'][number]['title'],bg='white',fg='black',wraplength=450,justify='left',borderwidth = 0)
        heading.bind("<Button-1>", lambda e,url=data3['articles'][number]['url']:open_site(url))
        heading.pack(pady=(0,5),padx = (0,20))
        heading.config(font=('verdana',15))
        details = Button(framenews, text=data3['articles'][number]['description'], bg='white', fg='black', wraplength=450,justify='left',borderwidth = 0)
        details.pack(pady=(0, 5),padx = (0,20))
        details.bind("<Button-1>", lambda e,url=data3['articles'][number]['url']:open_site(url))
        details.config(font=('verdana', 12))
        if number != 0:
            prev = Button(text='Previous',width=33,height=3,command=lambda :newsparse4(number-1),bg='white',borderwidth=0)
            prev.place(x = 320, y = 670)
        if number != len(data3['articles'])-1:
            next = Button(text='Next',width=33,height=3,command=lambda :newsparse4(number+1),bg='white',borderwidth=0)   
            next.place(x = 570, y = 670)                        

    # Widgets
    def open_site(url):
        webbrowser.open(url)    
    # Greetings and date time
    greetLabel = Label(framedaytime, font=(
        "bahnschrift", 20), bg=bgcol, fg=fgcol)
    greeting()

    timeLabel = Label(framedaytime, font=(
        "century gothic", 40), bg=bgcol, fg=fgcol)
    time()

    dateLabel = Label(framedaytime, font=(
        "bahnscrift", 15), bg=bgcol, fg=fgcol)
    date()

    greetLabel.grid(row=0, column=4, padx=(0, 0), sticky='n')
    timeLabel.grid(row=1, column=4, padx=(0, 0), sticky='n')
    dateLabel.grid(row=2, column=4, padx=(0, 0), sticky='n')

    # Weather information is set in the next few lines of code using information from the weather file

    weathertextLabel = Label(frameweather, text="Weather", font=(
        "century gothic bold", 25), bg=bgcol, fg=fgcol)
    weatherLabel = Label(frameweather, font=(
        "century gothic", 20), bg=bgcol, fg=fgcol)
    weatherLabel.configure(text=weather.weather(city_name), compound="right")

    locLabel = Label(frameweather, text="%s, %s" % (
        city_name, country_name), font=("century gothic", 20), bg=bgcol, fg=fgcol)

    # loads the weather asset png
    weatherim = PhotoImage(file="assets/weather.png")
    weatherLabel.configure(image=weatherim)

    weathertextLabel.grid(row=1, column=1, sticky="n")
    weatherLabel.grid(row=2, column=1, sticky="nw")

    locLabel.grid(row=0, column=1, sticky="n", padx=(0, 0))
    current_time = datetime.datetime.now()

    month = current_time.month-1
    year = current_time.year
    day = current_time.day
    data1 = requests.get(f'https://newsapi.org/v2/everything?q=Automotive Patents&from={year}-{month}-{day}&sortBy=publishedAt&apiKey=6c2ae8915e2946fc9da93547c6578250',verify=False).json()
    data2 = requests.get(f'https://newsapi.org/v2/everything?q=EMobility&from={year}-{month}-{day}&sortBy=publishedAt&apiKey=6c2ae8915e2946fc9da93547c6578250',verify=False).json()    
    data3 = requests.get(f'https://newsapi.org/v2/everything?q=Transmission&from={year}-{month}-{day}&sortBy=publishedAt&apiKey=6c2ae8915e2946fc9da93547c6578250',verify=False).json()    

    newsparse2(0)
    optionsLabel = Label(framestock, text="Options", font=(
        "century gothic bold", 20), bg=bgcol, fg=fgcol)
    optionsLabel.grid(row=0, column=0, columnspan=2, sticky="n", pady=(30, 0))
    rownumgraph = 1
    sidebar_button_1 = customtkinter.CTkButton(framestock,text= 'News - DIV C',width=300,height=50)
    sidebar_button_1.bind("<Button-1>", lambda e,:newsparse2(0))
    sidebar_button_1.grid(row=1, column=0, padx=10, pady=10)
 
    sidebar_button_2 = customtkinter.CTkButton(framestock,text= 'News - DIV E/A/U/I',width=300,height=50)
    sidebar_button_2.bind("<Button-1>", lambda e,:newsparse3(0))
    sidebar_button_2.grid(row=2, column=0, padx=10, pady=10)

    sidebar_button_3 = customtkinter.CTkButton(framestock,text= 'News - DIV T',width=300,height=50)
    sidebar_button_3.grid(row=3, column=0, padx=10, pady=10)
    sidebar_button_3.bind("<Button-1>", lambda e,:newsparse4(0))
    
    sidebar_button_4 = customtkinter.CTkButton(framestock, command=print("HI"),text= 'New Joiners',width=300,height=50)
    # sidebar_button_4.bind("<Button-1>", lambda e,:newsparse4(0))
    sidebar_button_4.grid(row=4, column=0, padx=10, pady=10)

    sidebar_button_5 = customtkinter.CTkButton(framestock,text= 'Patents',width=300,height=50)
    sidebar_button_5.grid(row=5, column=0, padx=10, pady=10)
    sidebar_button_5.bind("<Button-1>", lambda e,patenturl = 'https://www.thedrive.com/category/patents':open_site(patenturl))
    # calls stock function within stock file to load stock data into the stock labels
    # rownum = stock.stock(tickerlist, framestock, bgcol, fgcol, yf,
    #                      stockdownloadlist, flagdaynight, rownumgraph)+1

    # News data

    # currency converter and exchange rates
    framecc = Frame(framestock, highlightbackground=fgcol,
                    highlightthickness=2, width=350)
    # framecc.grid(row=rownum, column=0, columnspan=3, pady=(25, 0))
    # framecc.configure(bg=bgcol, width=350)

    # Menu bar for options and help

    # variable to hold input am
    # # From country name label and dropdown
    # Label(framecc, text="From: ", bg=bgcol, font='Banschrift 13',
    #       fg=fgcol).grid(row=rownum-1, column=0, padx=55, pady=(0, 0))
    # MenuFrom = OptionMenu(framecc, choice_from, *choices)
    # MenuFrom.grid(row=rownum, column=0, padx=(0, 35))

    # # To country name label and dropdown
    # Label(framecc, text="To: ", bg=bgcol, font='Banschrift 13', fg=fgcol).grid(
    #     row=rownum-1, column=1, pady=(0, 0), padx=55)
    # MenuTo = OptionMenu(framecc, choice_to, *choices)
    # MenuTo.grid(row=rownum, column=1, padx=(0, 0))

    # # Input amount label and dropdown
    # Label(framecc, text="Amount: ", bg=bgcol, fg=fgcol).grid(
    #     row=rownum+1, column=0, padx=(0, 35))



    # Click action on the entry box
       
    def action(event):
        print('hi')
    # Unclick action on the entry box            
    # Unclick action on the entry box



    # Result output Label
    # result_label = Label(framecc, bg=bgcol, font=('Banschrift', 13), fg=fgcol)
    # result_label.grid(row=rownum+2, column=0, columnspan=2)

    # # Convert action button
    # Cal_button = Button(framecc, text="Convert", bg=bgcol, fg=fgcol, command=lambda: Currency_Wigide_manager.convert(
    #     amt=amount, result_L=result_label, toChoice=choice_to, fromChoice=choice_from, FG=fgcol, BG=bgcol))
    # Cal_button.grid(row=rownum+1, column=1)

    # Calendar Widgets

    # Calendar functions

    # def LISTevents(date):

    #     global rem
    #     E_Wid = Toplevel(master=root)
    #     E_Wid.title("Event listing.")
    #     Label(master=E_Wid, text="All Events ").grid(row=0, column=0)
    #     op_field = Text(master=E_Wid, font="Courier 14", width=30)
    #     with open('reminder.json', 'r', encoding="utf8") as f:
    #         rem = json.load(f)
    #     s = ""
    #     for j in sorted(rem):
    #         for i in rem[j]:
    #             s += f"{j}:{i}\n"

    #     op_field.insert(END, s)
    #     op_field.config(state=DISABLED)
    #     op_field.grid(row=1, column=0)
    #     Button(E_Wid, text="Close", command=E_Wid.destroy).grid(
    #         row=2, column=0, sticky=S)

    #     E_Wid.mainloop()
    # res_l = Text(master=framecal, width=32, height=17,
    #              font="Courier 14", bg=bgcol, fg=fgcol)
    # res_l.grid(row=2, column=0, columnspan=3, sticky=W)

    # def ADDevent(date):
    #     global rem
    #     E_Wid = Toplevel(master=root)
    #     E_Wid.title("Event Adding.")
    #     Label(master=E_Wid, text=f"Date of the event {date}.").pack()
    #     E_Name = Entry(master=E_Wid)
    #     E_Name.pack()
    #     date = str(date)
    #     print(date)

    #     def ADDER():

    #         if date not in rem:

    #             rem[date] = []
    #         rem[date].append(str(E_Name.get()))
    #         print(rem)
    #         with open('reminder.json', 'w', encoding="utf8") as f:
    #             json.dump(rem, f)
    #         ans = messagebox.showinfo(
    #             title="successfully Added", message="Event added successfully to the Plans.")
    #         print(ans)

    #         E_Wid.destroy()
    #     Button(E_Wid, text="Add Event", command=ADDER).pack()

    #     E_Wid.mainloop()

    # def DELevent(date):
    #     MessageDIS = "Select the event no. \n"
    #     date = str(date)
    #     MessageDIS = {}
    #     print(rem)
    #     try:
    #         for i in range(len(rem[date])):
    #             MessageDIS[(f"{i+1 :>3} : {rem[date][i] :>15}\n")] = i

    #     except KeyError:
    #         messagebox.showerror("Event Error", "No Events on the day.")
    #         return
    #     E_Wid = Toplevel(master=root)
    #     E_Wid.title("Event Deletion.")
    #     Label(master=E_Wid, text="Event Deletion").grid(row=0, column=1)
    #     Label(master=E_Wid, text="Event Ids : ").grid(row=1, column=0)
    #     del_date = StringVar()
    #     MenuDate = OptionMenu(E_Wid, del_date, *MessageDIS.keys())
    #     MenuDate.grid(row=1, column=1)

    #     def del_confirm():
    #         question = messagebox.showwarning(
    #             "Please confirm", "please confirm")
    #         if question:
    #             rem[date].pop(int(MessageDIS[del_date.get()])-1)
    #             if not (rem[date]):
    #                 del (rem[date])
    #             with open('reminder.json', 'w', encoding="utf8") as f:
    #                 json.dump(rem, f)
    #             E_Wid.destroy()

    #     Button(master=E_Wid, text="Ok",
    #            command=del_confirm).grid(row=2, column=0)
    #     Button(master=E_Wid, text="Cancel",
    #            command=E_Wid.destroy).grid(row=2, column=2)

    #     E_Wid.mainloop()

    cal = Calendar(framecal, font="Courier 14")
    cal.grid(row=0, column=0, sticky=W, columnspan=3,pady = (20,0),padx = (110 , 0))

    # def listing_SELDATE(date):
    #     try:
    #         date = str(date)
    #         res_l.config(state=NORMAL)
    #         res_l.delete("1.0", END)
    #         # print(date)
    #         with open('reminder.json', 'r', encoding="utf8") as f:
    #             rem = json.load(f)
    #         if (not (rem)) or (date not in rem) or (not (rem[date])):
    #             res_l.insert(END, "No Plans.")
    #         elif date in rem:
    #             s = ""
    #             for j in rem[date]:
    #                 s += f"{date}:{j}\n"

    #             res_l.insert(END, s)
    #             res_l.config(state=DISABLED)


    #         Timer(1, lambda: listing_SELDATE(cal.selection_get())).start()
    #     except Exception:
    #         pass

    # listing_SELDATE(cal.selection_get())

    # with open('reminder.json', 'r', encoding="utf8") as f:
    #     rem = json.load(f)
    #     print(rem)

    # choice_what = StringVar()
    # choice_what.set("Add Event")
    # functions = {"Add Event": ADDevent.__name__,
    #              "List all Events": LISTevents.__name__, "Delete Event": DELevent.__name__}
    Label(framecal, text="Upcoming events",bg=bgcol, fg=fgcol,font =("century gothic bold", 20)).grid(row=1, column=1, sticky=W, pady = (20,0), padx=(100,0))  
    dataframe1 = pd.read_excel(r"C:\news\Upcoming_Events.xlsx")  
    tv1["column"] = list(dataframe1.columns) 
    tv1["show"] = "headings"
    tv1.column("Date", width=150)
    tv1.column("Event", width=150)
    tv1.column("Time", width=150)
    tv1.grid(row=2,column=0,sticky=NS,columnspan=3,pady = (20,0),padx = (70 , 0))
    style = ttk.Style()
    style.configure("Treeview.columns", font=(None, 20))
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name    
        df_rows = dataframe1.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row)   
    # events_lable = Label(framecal, text=dataframe1,bg=bgcol, fg=fgcol,font =("Calibri", 15), anchor= "w")
    # events_lable.grid( row=4, column=1, pady = (0,0))
    # print(dataframe1)
    # MenuFrom = OptionMenu(framecal, choice_what, *functions.keys())
    # MenuFrom.grid(column=1, row=1, sticky=W, pady=(20,20))
    # event_caller = Button(framecal, text="OK", command=lambda: eval(
    #     f"{functions[choice_what.get()]}(cal.selection_get())"))
    # event_caller.grid(row=1, column=2, sticky='e',pady=(20, 20))

    # framecal.bind('<Return>', lambda _: eval(f"{functions[choice_what.get()]}(cal.selection_get())"))
    # root.bind('<Return>', lambda _: eval(f"{functions[choice_what.get()]}(cal.selection_get())"))

    root.mainloop()
