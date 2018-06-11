from tkinter import *
from tkinter import font
from pytube import YouTube


root = Tk()
root.geometry('600x410')
root.title('VDM (Vikku Download manager)')
root.resizable(width=False, height=False)
root.config(bg='gray95')


def changepath(event):
    path_label= Label(frame1, text='Path: ',bg=color,font={'arial',12,'bold'})
    path_label.grid(row=1, column=0,padx=5,pady=5)
    entry = Entry(frame1, width=40, bd=0)
    path_entry.grid(row=1, column=1, padx=5, pady=5)
    path_entry.focus()

#====================================================== Frames ==================================================
color='gray95'
white='white'
black='black'
st= StringVar()
frame1= Frame(root, width=600, height=100,bg='gray95')
frame1.grid(row=0)
v= IntVar()
frame2= Frame(root, width=600, height=230,bg='blue')
frame2.grid(row=1)
frame3= Frame(root, width=600, height=60,bg='red')
frame3.grid(row=2)
frame4= Frame(root,width=600,height=20,bg=black)
frame4.grid(row=3)
frame1.grid_propagate(0)
frame2.grid_propagate(0)
frame3.grid_propagate(0)
URL= Label(frame1, text="YouTube URL: ",bg=color,font={'arial',12,'bold'})
URL.grid(row=0,column=0,padx =5, pady=15)

path_entry = Entry(frame1, width=40, bd=0)
path_entry.grid_remove()

link= Entry(frame1,width=40,bd=0)
link.grid(row=0,column=1,padx=5, pady=15)
link.focus()
chpath= Label(frame1, text="Select path",bg=color,fg='blue')
chpath.grid(row=0,column=2,padx =5, pady=5)
f = font.Font(chpath, chpath.cget("font"))
f.configure(underline=True)
chpath.configure(font=f)
chpath.bind('<Button-1>',changepath)

def down_video(event):
    download_video(path_entry.get())

download_button= Button(frame1, text='Download',bg=black,fg=white,command=lambda : download_video(path_entry.get()))
download_button.grid(row=1,column=2,padx=15,pady=5)
link.bind('<Return>',down_video)
clear_button= Button(frame3, text='Clear',bg=black,fg=white)
clear_button.grid(row= 0,column=0,padx=15,pady=5)
high= Radiobutton(frame3,text="High",variable=v,value=1)
high.grid(row=0,column=1)
low= Radiobutton(frame3,text="low",variable=v,value=0)
low.grid(row=0,column=2)

status= Label(frame4,width=60,font=("Courier", 12),textvariable=st)
status.grid(row=1)

def complete(stream, file_handle):
    st.set("Download Complete")

size=0

def download_video(path):
    global size,st
    st.set("gathering Information...")
    yt= YouTube(link.get(),on_complete_callback=complete,on_progress_callback=processing)
    stream =yt.streams.filter(progressive=True, file_extension='mp4')
    value= int(v.get())
    if value==0:
        video = stream.last()
    elif value==1:
        video = stream.first()
    size = video.filesize
    if path is "":
        video.download('/home/vikku/Downloads/VDM/')
    else:
        video.download(path)


def processing(stream, chunk, file_handle, bytes_remaining):
    # global st
    print(int(((size - bytes_remaining)/size)*100))



root.mainloop()