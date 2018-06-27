from tkinter import *
from tkinter import ttk
from pytube import YouTube
import threading
import re
from time import sleep
import os.path
import datetime
from tkinter import PhotoImage
from tkinter import font
import webbrowser
from traceback import format_exc
from subprocess import Popen
'''
Created On june 2018

@author: Vivek Sharma 
'''

# ==========================Tkinter Window==============================


root = Tk()
root.geometry('618x430')
root.title('VDM (Vikku Download manager)')
imgicon = PhotoImage(file=os.path.join("/home/vikku",'gif.png'))
root.tk.call('wm', 'iconphoto', root._w, imgicon)
root.resizable(width=True, height=False)
root.config(bg='gray95')


# =========================Global Variables=============================


color = 'gray95'
white = 'white'
black = 'black'
file_info = StringVar()
size = 0
counter = 0
dictonary = {}
dic_variable = 0
video_title= ""
st, path_variable, link_variable = StringVar(), StringVar(), StringVar()
v = IntVar()

# =============================== Frames ======================


frame1 = Frame(root, width=600, height=100, bg='gray12')
# frame2 = Frame(root, width=600, height=250, bg='lightsteelblue1')
frame3 = Frame(root, width=600, height=35, bg=white)
# frame4 = Frame(root, width=600, height=20)
frame5 = Frame(root, width=600, height=25,bg=black)
frame1.grid(row=0)
# frame2.grid(row=1)
frame3.grid(row=2)
frame5.grid(row=4)
frame1.grid_propagate(0)
# frame2.grid_propagate(0)
frame3.grid_propagate(0)
# frame4.grid_propagate(0)
def changepath(event):
    path_entry.grid(row=1, column=1, padx=5, pady=5)
    path_label.grid(row=1, column=0, padx=5, pady=5)
    path_label["text"]= "Path: "


# ==================== Frame1 Widgets ===========================


URL = Label(frame1, text="YouTube URL: ", bg='gray12',fg=white, font={'arial', 12, 'bold'})
path_label = Label(frame1, text='Path: ', bg='gray12',fg=white, font={'arial', 12, 'bold'})

ask_path_label = Label(frame1, text='select path', bg='gray12',fg="blue")
f = font.Font(ask_path_label, ask_path_label.cget("font"))
f.configure(underline=True)
ask_path_label.configure(font=f)
ask_path_label.bind('<Button-1>',changepath)
path_entry = Entry(frame1, width=40, bd=0, textvariable=path_variable)
link = Entry(frame1, width=40, bd=0, textvariable=link_variable)
quality_button = Button(frame1, text='Quality', fg=white, bg="gray12", command=lambda: quality_check())
quality_button.grid(row=0,column=2,padx=8)
URL.grid(row=0, column=0, padx=5, pady=15)
path_label.grid(row=1, column=0, padx=5, pady=5)
ask_path_label.grid(row=1, column=2, padx=5, pady=5)
path_entry.grid(row=1, column=1, padx=5, pady=5)
link.grid(row=0, column=1, padx=5, pady=15)
path_entry.grid_remove()
path_label.grid_remove()
link.focus()


# ========================= Methods Used ==========================

def quality_check_thread(counter,name):
    try:

        quality_check_thread.yt = YouTube(link_variable.get(), on_complete_callback=complete, on_progress_callback=processing)
        path_entry.grid_remove()
        video_title =quality_check_thread.yt.title
        path_label["text"]= video_title[:30]+"..."
        path_label.grid(row=1, column=1, padx=5, pady=5)

        quality_check_thread.yt.prefetch()
        stream = quality_check_thread.yt.streams.filter(progressive=True,file_extension='mp4')
        quality_check.final_stream = stream
        for i in stream.all():
            k = re.compile(r'\d\d\dp')
            mo = k.search(str(i))
            iter = mo.group()
            iter = Radiobutton(frame3, text=iter, variable=v, value=counter)
            iter.grid(row=0, column=counter + 1)
            counter += 1
        st.set('')
    except Exception:
        if link.get() == "":
            st.set("Please Enter URL")
        else:
            st.set('Cannot do Quality check, TRY AGAIN')


def quality_check():
    try:
        status.grid(row=0)
        mpb['value']=0
        status['bg']= "gray"
        if  not link.get().startswith("https://www.youtube.com/"):
            raise Exception
        st.set("checking for Qualities Available")
        quality_thread = threading.Thread(target=quality_check_thread, name='thread2', args=(counter,"thread2"))
        quality_thread.start()
    except Exception:
        if link.get() == "":
            st.set("Please Enter URL")
        else:
            st.set("Input valid URL")



def download_thread(path, name):
    global size, dic_variable
    try:
        try:
            stream = quality_check.final_stream
        except Exception:
            quality_check_thread.yt = YouTube(link_variable.get(), on_complete_callback=complete, on_progress_callback=processing)
            stream = quality_check_thread.yt.streams.filter( progressive = True, file_extension='mp4')
        finally:
            if path =="":
                file_check = os.path.isfile("/home/vikku/Downloads/VDM/{}.mp4".format(quality_check_thread.yt.title.strip()))
            else:
                p=os.path.join(path,quality_check_thread.yt.title.strip())
                file_check = os.path.isfile("{0}.mp4".format(p))

            if file_check:
                top  = Toplevel(root)
                top.geometry('300x180')
                top.resizable(width=False,height=True)
                Label(top,image= imgicon).grid(row=0,column=0)
                Label(top,text = "Video Already exists",font={"arial",16,"bold"}).grid(row=0,column=1)
                Button(top, text='exit',font={"arial",12,"bold"},command=lambda :top.destroy()).grid(row=1,column=1)
                top.mainloop()
                raise Exception("bye bye")

        video_title = quality_check_thread.yt.title
        path_entry.grid_remove()
        path_label["text"] = video_title[:30] + "..."
        path_label.grid(row=1, column=1, padx=5, pady=5)

        value = int(v.get())
        if value == 0:
            video = stream.first()
        elif value == 1:
            video = stream.last()
        else:
            video = stream.last()
        size = video.filesize
        if path == '':
            video.download('/home/vikku/Downloads/VDM/')
        else:
            video.download(path)
    except Exception as e:
        if link.get() == "":
            st.set("Please Enter URL")
        else:
            status["bg"]= "gray"
            log= open("log_file.txt",'a')
            log.write(format_exc())
            log.close()
            st.set("")


def down_video(event):
    download_video()


def clear():
    path_variable.set('')
    link_variable.set('')
    status.grid_remove()

def openFile(Time,title,link_data,path):
    with open("/home/vikku/PycharmProjects/idm/frame2_content.txt", 'r+') as orignal:
        data  = orignal.read()
        orignal.close()
    with open("/home/vikku/PycharmProjects/idm/frame2_content.txt", 'w') as modified:
        modified.write(Time+", "+title+", "+link_data+", "+path+"\n" + data)
        modified.close()


def complete(stream, file_handle):
    try:
        video_title = quality_check_thread.yt.title
        if path_variable.get() == "":
            absolute_path = "/home/vikku/Downloads/VDM/"
        else:
            absolute_path = path_variable.get()
        x= float(os.path.getsize(os.path.join(absolute_path,video_title)+".mp4")
                                                 /(1024*1024))
        st.set("Download Complete {0} MB".format(round(x,2)))

    except Exception as E:
        st.set("|| Download Complete ||")
    finally:
        download_time =str(datetime.datetime.now())[:16]
        openFile(download_time, video_title, link_variable.get(),absolute_path)
        sleep(0.5)
        populate(frame2)



def download_video():
    try:
        global st
        status.grid(row=0)
        status["bg"]="gray"
        st.set("gathering Information...")
        path_variable.set(path_entry.get())
        if not link.get().startswith("https://www.youtube.com/"):
            raise Exception
        mpb['value']=0
        thread1 = threading.Thread(target=download_thread, name='thread1', args=(path_variable.get(), "thread1"))
        thread1.start()
    except Exception:
        if link.get() == "":
            st.set("Please Enter URL")
        else:
            st.set("input valid URL")


def processing(stream, chunk, file_handle, bytes_remaining):
    global size
    percent = int(((size - bytes_remaining) / size) * 100)
    st.set(str(percent)+"%")
    mpb["value"] = percent
    if percent >= 49:
        status["background"] = "dodger blue"

def doleft(kd):
    webbrowser.open_new_tab(kd)
def doright(kd):
    Popen(["xdg-open",kd[:-1].strip()])
#================================= Frame2 Widgets ==================================


def populate(frame2):
    label_increment = 0
    Label(frame2, text="\tVideo title \t\t\t\t Time", width=90, anchor="w", fg="midnight blue",
            bg="lightsteelblue2").grid(row=label_increment, column=0)
    with open("/home/vikku/PycharmProjects/idm/frame2_content.txt", 'r') as f:
        for line in f:
            list_item = line.split(",")
            if len(list_item[1]) > 36:
                list_item[1] = list_item[1][:30] + "..."
            file_info = "{}. ".format(label_increment + 1) + "{:<36}\t\t\t{} ({})".format(list_item[1], list_item[0],
                                                                                       list_item[3].split("/")[-2])
            label_increment += 1

            eval_link_left = lambda x: (lambda p: doleft(x))
            eval_link_right = lambda x: (lambda p: doright(x))

            lb = Label(frame2, text=file_info, width=90, anchor='w', bg=white, wraplength=600)
            lb.bind("<Button-1>", eval_link_left(list_item[2].strip()))
            lb.bind("<Button-3>", eval_link_right(list_item[3]))
            lb.grid(row=label_increment, column=0, pady=2, padx=1)
        f.close()



canvas = Canvas(root,width=600, background="lightsteelblue2")
frame2 = Frame(canvas, background="lightsteelblue2",width=600)
vscroll = Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vscroll.set)

vscroll.grid(row=0,column=1,sticky="ns",rowspan=15)
canvas.grid(row=1,column=0,sticky=S)
canvas.create_window((3,4), window=frame2, anchor="nw")

frame2.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

populate(frame2)
# ======================= Frame3 Widgets ===========================


download_button = Button(frame3, text='Download', bg=black, fg=white, command=lambda: download_video())
clear_button = Button(frame3, text='Clear', bg=black,    fg=white, command=lambda: clear())

download_button.grid(row=0, column=0, padx=15, pady=5)
clear_button.grid(row=0, column=6, padx=15, pady=5)

link.bind('<Return>', down_video)

# ================== Frame5 Widgets =================================

s = ttk.Style()
s.configure("red.Horizontal.TProgressbar",troughcolor ='gray', background='dodger blue',thickness =30)
mpb = ttk.Progressbar(frame5,style="red.Horizontal.TProgressbar",orient ="horizontal",length = 600, mode ="determinate")
mpb.grid(row=0)
status = Label(frame5, textvariable=st, font=("Courier", 12),bg="gray",fg=black)



mpb["maximum"] = 100

# =================== Show Window ====================================

root.mainloop()

# ===================== Experiments ================================

'''
chpath= Label(frame1, text="Select path",bg=color,fg='blue')
chpath.grid(row=0,column=2,padx =5, pady=5)
f = font.Font(chpath, chpath.cget("font"))
f.configure(underline=True)
chpath.configure(font=f)
chpath.bind('<Button-1>',changepath)
'''

'''
    yt = YouTube(link_variable.get())
    stream = yt.streams.filter(progressive=True, file_extension='mp4')
    for i in stream.all():
        print(yt.title,end=" ")
        k = re.compile(r'\d\d\dp')
        mo = k.search(str(i))
        print(mo.group())
'''