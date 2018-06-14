from tkinter import *
from tkinter import ttk
from pytube import YouTube
import threading
import re

'''
Created On june 2018

@author: Vivek Sharma 
'''

# ==========================Tkinter Window==============================


root = Tk()
root.geometry('600x430')
root.title('VDM (Vikku Download manager)')
root.resizable(width=False, height=False)
root.config(bg='gray95')


# =========================Global Variables=============================


color = 'gray95'
white = 'white'
black = 'black'
size = 0
counter = 0
dictonary = {}
dic_variable = 0
st, path_variable, link_variable = StringVar(), StringVar(), StringVar()
v = IntVar()

# =============================== Frames ======================


frame1 = Frame(root, width=600, height=100, bg='gray12')
frame2 = Frame(root, width=600, height=230, bg='gray95')
frame3 = Frame(root, width=600, height=60, bg="gray40")
frame4 = Frame(root, width=600, height=20)
frame5 = Frame(root, width=600, height=20,bg=black)
frame1.grid(row=0)
frame2.grid(row=1)
frame3.grid(row=2)
frame4.grid(row=3)
frame5.grid(row=4)
frame1.grid_propagate(0)
frame2.grid_propagate(0)
frame3.grid_propagate(0)
frame4.grid_propagate(0)

# ==================== Frame1 Widgets ===========================


URL = Label(frame1, text="YouTube URL: ", bg='gray12',fg=white, font={'arial', 12, 'bold'})
path_label = Label(frame1, text='Path: ', bg='gray12',fg=white, font={'arial', 12, 'bold'})
path_entry = Entry(frame1, width=40, bd=0, textvariable=path_variable)
link = Entry(frame1, width=40, bd=0, textvariable=link_variable)
quality_buttons = Button(frame1, text='Quality', fg=black, bg=white, command=lambda: quality_check())
quality_buttons.grid(row=0,column=2)
URL.grid(row=0, column=0, padx=5, pady=15)
path_label.grid(row=1, column=0, padx=5, pady=5)
path_entry.grid(row=1, column=1, padx=5, pady=5)
link.grid(row=0, column=1, padx=5, pady=15)
link.focus()


# ========================= Methods Used ==========================

def quality_check_thread(counter,name):
    try:

        quality_check_thread.yt = YouTube(link_variable.get(), on_complete_callback=complete, on_progress_callback=processing)
        quality_check_thread.yt.prefetch()
        stream = quality_check_thread.yt.streams.filter(progressive=True, file_extension='mp4')
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
    st.set("checking for Qualities Available")
    quality_thread = threading.Thread(target=quality_check_thread, name='thread2', args=(counter,"thread2"))
    quality_thread.start()



def download_thread(path, name):
    global size, dic_variable
    try:
        try:
            stream = quality_check.final_stream
        except Exception:
            quality_check_thread.yt = YouTube(link_variable.get(), on_complete_callback=complete, on_progress_callback=processing)
            stream = quality_check_thread.yt.streams.filter(progressive=True, file_extension='mp4')

        dictonary["f_label{}".format(dic_variable)] = quality_check_thread.yt.title
        dic_variable += 1

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
    except Exception:
        if link.get() == "":
            st.set("Please Enter URL")
        else:
            st.set('DownloadError | ' + link_variable.get())


def down_video(event):
    download_video()


def clear():
    path_variable.set('')
    link_variable.set('')


def complete(stream, file_handle):
    st.set("Download Complete")
    # for ki, vi in dictonary:
    #     ki = Label(frame2, bg='pink', width=60, font=("Courier", 12), justify='center',  text=vi)
    #     ki.grid(row =ki[-1], column=0, pady=2)


def download_video():
    global st
    st.set("gathering Information...")
    path_variable.set(path_entry.get())
    mpb['value']=0
    thread1 = threading.Thread(target=download_thread, name='thread1', args=(path_variable.get(), "thread1"))
    thread1.start()


def processing(stream, chunk, file_handle, bytes_remaining):
    global size
    percent = int(((size - bytes_remaining) / size) * 100)
    st.set(str(percent)+"%")
    mpb["value"] = percent


#======================== Frame2 Widgets ===========================


# ======================= Frame3 Widgets ===========================


download_button = Button(frame3, text='Download', bg=black, fg=white, command=lambda: download_video())
clear_button = Button(frame3, text='Clear', bg=black, fg=white, command=lambda: clear())
download_button.grid(row=0, column=0, padx=15, pady=5)
clear_button.grid(row=0, column=6, padx=15, pady=5)

link.bind('<Return>', down_video)

# ================== Frame4 Widgets =================================


status = Label(frame4, textvariable=st, width=60, font=("Courier", 12), bg="midnight blue",fg=white)
status.grid(row=1)
mpb = ttk.Progressbar(frame5,orient ="horizontal",length = 600, mode ="determinate")
mpb.grid()
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