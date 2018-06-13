from tkinter import *
from tkinter import font
from pytube import YouTube
import threading

'''
Created On
  
@author: Vivek Sharma 
'''

#==========================Tkinter Window==============================


root = Tk()
root.geometry('600x410')
root.title('VDM (Vikku Download manager)')
root.resizable(width=False, height=False)
root.config(bg='gray95')

#=========================Global Variables=============================


color='gray95'
white='white'
black='black'
size=0
st,path_variable,link_variable= StringVar(),StringVar(),StringVar()
v= IntVar()

#=============================== Frames ======================


frame1= Frame(root, width=600, height=100,bg='gray95')
frame2= Frame(root, width=600, height=230,bg='blue')
frame3= Frame(root, width=600, height=60,bg='red')
frame4= Frame(root,width=600,height=20,bg=black)
frame1.grid(row=0)
frame2.grid(row=1)
frame3.grid(row=2)
frame4.grid(row=3)
frame1.grid_propagate(0)
frame2.grid_propagate(0)
frame3.grid_propagate(0)
frame4.grid_propagate(0)

#==================== Frame1 Widgets ===========================


URL= Label(frame1, text="YouTube URL: ",bg=color,font={'arial',12,'bold'})
path_label = Label(frame1, text='Path: ', bg=color, font={'arial', 12, 'bold'})
path_entry = Entry(frame1, width=40, bd=0,textvariable=path_variable)
link= Entry(frame1,width=40,bd=0,textvariable=link_variable)

URL.grid(row=0,column=0,padx =5, pady=15)
path_label.grid(row=1, column=0, padx=5, pady=5)
path_entry.grid(row=1, column=1, padx=5, pady=5)
link.grid(row=0,column=1,padx=5, pady=15)
link.focus()

#========================= Methods Used ==========================


def download_thread(path,name):
    global size
    try:
        yt= YouTube(link_variable.get(),on_complete_callback=complete,on_progress_callback=processing)
        stream =yt.streams.filter(progressive=True, file_extension='mp4')
        value= int(v.get())
        if value==0:
            video = stream.last()
        elif value==1:
            video = stream.first()
        else:
            video =stream.last()\

        size = video.filesize
        if path =='':
            video.download('/home/vikku/Downloads/VDM/')
        else:
            video.download(path)
    except Exception:
        st.set('DownloadError | '+link_variable.get())


def down_video(event):
    download_video()


def clear():
    path_variable.set('')
    link_variable.set('')


def complete(stream, file_handle):
    st.set("Download Complete")


def download_video():
    global st
    st.set("gathering Information...")
    path_variable.set(path_entry.get())
    print(path_entry.get() == '')
    thread1 = threading.Thread(target=download_thread, name='thread1', args=(path_variable.get(),"thread1"))
    thread1.start()


def processing(stream, chunk, file_handle, bytes_remaining):
    global size
    percent = int(((size - bytes_remaining) / size) * 100)
    st.set(percent)

#======================= Frame3 Widgets ===========================


download_button= Button(frame3, text='Download',bg=black,fg=white,command=lambda : download_video())
clear_button= Button(frame3, text='Clear',bg=black,fg=white,command=lambda :clear())
high= Radiobutton(frame3,text="High",variable=v,value=1)
low= Radiobutton(frame3,text="low",variable=v,value=0)
download_button.grid(row=0,column=0,padx=15,pady=5)
clear_button.grid(row= 0,column=3,padx=15,pady=5)
high.grid(row=0,column=1)
low.grid(row=0,column=2)
link.bind('<Return>',down_video)

#================== Frame4 Widgets =================================


status= Label(frame4,textvariable=st,width=60,font=("Courier", 12))
status.grid(row=1)


#=================== Show Window ====================================

root.mainloop()


#===================== Experiments ================================

'''
chpath= Label(frame1, text="Select path",bg=color,fg='blue')
chpath.grid(row=0,column=2,padx =5, pady=5)
f = font.Font(chpath, chpath.cget("font"))
f.configure(underline=True)
chpath.configure(font=f)
chpath.bind('<Button-1>',changepath)
'''