from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pytube import YouTube
import threading
import re
from time import sleep
import os.path
import datetime
import string
from tkinter import font
import webbrowser
from traceback import format_exc
from subprocess import Popen
from urllib import request
from tkinter import PhotoImage
from PIL import Image
'''
Created On june 2018

@author: Vivek Sharma 
'''


# ==========================Tkinter Window==============================

class Idm(Tk):

    def __init__(self):

        super().__init__()
        self.geometry('618x430')
        self.title('VDM (Vikku Download manager)')
        self.resizable(width=False, height=False)
        # self.config(bg='gray95')

        self.color = 'gray95'
        self.white = 'white'
        self.black = 'black'
        self.file_info = StringVar()
        self.size = 0
        self.counter = 0
        self.dictonary = {}
        self.dic_variable = 0
        self.video_title = ""
        self.st, self.path_variable, self.link_variable = StringVar(), StringVar(), StringVar()
        self.v = IntVar()

        self.set_image()
        self.initialize_frames()
        self.set_frame1_widgets()
        self.set_frame2_widgets()
        self.set_frame3_widgets()
        self.set_frame4_widgets()

    def set_image(self):

        imgicon = PhotoImage(file=os.path.join("/home/vikku", 'gif.png'))
        self.tk.call('wm', 'iconphoto', self._w, imgicon)

    def initialize_frames(self):

        self.frame1 = Frame(self, width=618, height=100, bg='gray12')
        self.frame3 = Frame(self, width=618, height=35, bg=self.white)
        self.frame4 = Frame(self, width=618, height=25, bg=self.black)
        self.frame1.grid(row=0)
        self.frame3.grid(row=2)
        self.frame4.grid(row=4)
        self.frame1.grid_propagate(0)
        self.frame3.grid_propagate(0)
        self.frame4.grid_propagate(0)

        self.bind('<Button-4>', self.mouse_scroll)
        self.bind('<Button-5>', self.mouse_scroll)

    def set_frame1_widgets(self):

        URL = Label(self.frame1, text="YouTube URL: ", bg='gray12', fg=self.white, font={'arial', 12, 'bold'})
        self.path_label = Label(self.frame1, text='Path: ', bg='gray12', fg=self.white, font={'arial', 12, 'bold'})
        ask_path_label = Label(self.frame1, text='select path', bg='gray12', fg="blue")
        f = font.Font(ask_path_label, ask_path_label.cget("font"))
        f.configure(underline=True)
        ask_path_label.configure(font=f)
        ask_path_label.bind('<Button-1>', self.changepath)
        self.path_entry = Entry(self.frame1, width=40, bd=0, textvariable=self.path_variable)
        self.link = Entry(self.frame1, width=40, bd=0, textvariable=self.link_variable)
        quality_button = Button(self.frame1, text='Quality', fg=self.white, bg="gray12",
                                command=lambda: self.quality_check())

        quality_button.grid(row=0, column=2, padx=48)
        URL.grid(row=0, column=0, padx=5, pady=15)
        ask_path_label.grid(row=1, column=2, padx=5, pady=5)
        self.link.grid(row=0, column=1, padx=5, pady=15)
        self.link.focus()
        self.link.bind('<Return>', self.down_video)

    def set_frame2_widgets(self):

        self.canvas = Canvas(self, width=618, background="white")
        self.frame2 = Frame(self.canvas, background="lightsteelblue2", width=618)
        vscroll = Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vscroll.set)

        vscroll.grid(row=0, column=1, sticky="W", ipady=120)
        self.canvas.grid(row=1, column=0, sticky=S)
        self.canvas.grid_propagate(0)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.frame2, anchor="nw")
        self.frame2.bind("<Configure>", lambda event, canvas=self.canvas: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.populate(self.frame2)

    def set_frame3_widgets(self):

        download_button = Button(self.frame3, text='Download', bg=self.black, fg=self.white,
                                 command=lambda: self.download_video())
        clear_button = Button(self.frame3, text='Clear', bg=self.black, fg=self.white, command=lambda: self.clear())

        download_button.grid(row=0, column=0, padx=15, pady=5)
        clear_button.grid(row=0, column=6, padx=15, pady=5)

    def set_frame4_widgets(self):

        s = ttk.Style()
        s.configure("red.Horizontal.TProgressbar", troughcolor='gray', background='dodger blue', thickness=30)
        self.mpb = ttk.Progressbar(self.frame4, style="red.Horizontal.TProgressbar", orient="horizontal", length=618,
                                   mode="determinate")
        self.status = Label(self.frame4, textvariable=self.st, font=("Courier", 12), bg="gray", fg=self.black)

        self.mpb.grid(row=0)
        self.mpb["maximum"] = 100

    def populate(self, frame2):
        colors = [{"fg": "black", "bg": "gray94"}, {"fg": "black", "bg": "white"}]
        label_increment = 0
        Label(frame2, text="\tVideo title \t\t\t\t Time", width=90, anchor="w", fg="midnight blue",
              bg="lightsteelblue2").grid(row=label_increment, column=0)

        with open("/home/vikku/PycharmProjects/idm/frame2_content.txt", 'r') as f:
            for line in f:
                list_item = line.split(",")
                if len(list_item[1]) > 33:
                    list_item[1] = list_item[1][:30] + "..."
                file_info = "    {}. ".format(label_increment + 1) + "{:<33}\t\t\t{} ({})".format(list_item[1],
                                                                                                  list_item[0],
                                                                                                  list_item[3].split(
                                                                                                      "/")[-2])
                label_increment += 1
                _, my_color = divmod(label_increment, 2)
                seleceted_combo = colors[my_color]

                eval_link_left = lambda x: (lambda p: self.doleft(x))
                eval_link_right = lambda x: (lambda p: self.doright(x))

                lb = Label(frame2, text=file_info, width=90, anchor='w', wraplength=600)
                lb.configure(bg=seleceted_combo["bg"])
                lb.configure(fg=seleceted_combo["fg"])
                lb.bind("<Button-1>", eval_link_left(list_item[2].strip()))
                lb.bind("<Button-3>", eval_link_right(list_item[3]))
                lb.grid(row=label_increment, column=0, pady=2, padx=1)
            f.close()

    def changepath(self, event):
        self.path_entry.grid(row=1, column=1, padx=5, pady=5)
        self.path_label.grid(row=1, column=0, padx=5, pady=5)
        self.path_label["text"] = "Path: "
        self.path_entry.focus()

    def mouse_scroll(self, event):
        if event.num == 5:
            move = 1
        elif event.num == 4:
            move = -1
        self.canvas.yview_scroll(move, "units")

    def clear(self):
        self.path_variable.set('')
        self.link_variable.set('')
        self.status.grid_remove()

    def quality_check(self):
        try:
            self.status.grid(row=0)
            self.mpb['value'] = 0
            self.status['bg'] = "gray"
            if not self.link.get().startswith("https://www.youtube.com/"):
                raise Exception
            self.st.set("checking for Qualities Available")
            quality_thread = threading.Thread(target=self.quality_check_thread, name='thread2',
                                              args=(self.counter, "thread2"))

            quality_thread.start()

        except Exception:
            if self.link.get() == "":
                self.st.set("Please Enter URL")
            else:
                self.st.set("Input valid URL")

    def quality_check_thread(self, counter, name):
        try:

            self.yt = YouTube(self.link_variable.get(), on_complete_callback=self.complete,
                              on_progress_callback=self.processing)
            self.thumbnail_thread = threading.Thread(target=self.thumbnail_thread, name='thread3',
                                              args=(counter, "thread3"))
            self.thumbnail_thread.start()
            self.thumbnail_thread.join()

            self.path_entry.grid_remove()
            self.video_title = self.yt.title
            self.path_label["text"] = self.video_title[:30] + "..."
            self.path_label.grid(row=1, column=1, padx=5, pady=5)
            self.yt.prefetch()
            stream = self.yt.streams.filter(progressive=True, file_extension='mp4')
            self.final_stream = stream

            for i in stream.all():
                k = re.compile(r'\d\d\dp')
                mo = k.search(str(i))
                iter = mo.group()
                iter = Radiobutton(self.frame3, text=iter, variable=self.v, value=counter)
                iter.grid(row=0, column=counter + 1)
                counter += 1
            self.st.set('')

        except Exception:

            if self.link.get() == "":
                self.st.set("Please Enter URL")
            else:
                self.st.set('Cannot do Quality check, TRY AGAIN')

    def thumbnail_thread(self, _, name):

        self.image_url = self.yt.thumbnail_url
        x= os.path.join("/home/vikku/","Thumbnail.jpg")
        request.urlretrieve(self.image_url,x)
        im = Image.open("/home/vikku/Thumbnail.jpg")
        im.save('/home/vikku/Thumbnail.png')

    def down_video(self, event):
        self.download_video()

    def download_video(self):

        try:
            self.status.grid(row=0)
            self.img = PhotoImage(file="/home/vikku/Thumbnail.png")
            self.status["bg"] = "gray"
            self.st.set("gathering Information...")
            self.path_variable.set(self.path_entry.get())
            if not self.link.get().startswith("https://www.youtube.com/"):
                raise Exception
            self.mpb['value'] = 0
            self.thread1 = threading.Thread(target=self.download_thread, name='thread1',
                                            args=(self.path_variable.get(), "thread1"))
            self.thread1.start()

        except Exception:
            if self.link.get() == "":
                self.st.set("Please Enter URL")
            else:
                self.st.set("input valid URL")

    def download_thread(self, path, name):

        try:
            try:
                stream = self.final_stream
            except Exception:
                self.yt = YouTube(self.link_variable.get(), on_complete_callback=self.complete,
                                  on_progress_callback=self.processing)
                stream = self.yt.streams.filter(progressive=True, file_extension='mp4')
                self.thumbnail_thread = threading.Thread(target=self.thumbnail_thread, name='thread3',
                                                         args=(self.yt,"thread3"))
                self.thumbnail_thread.start()

            finally:
                if path == "":
                    file_check = os.path.isfile(
                        "/home/vikku/Downloads/VDM/{}.mp4".format(self.string_manupulation(self.yt.title)))
                else:
                    p = os.path.join(path, self.string_manupulation(self.yt.title))
                    file_check = os.path.isfile("{0}.mp4".format(p))

                if file_check:
                    messagebox.showerror("error", "File already exists..")
                    raise Exception("bye bye")
            self.video_title = self.yt.title
            self.path_entry.grid_remove()
            self.path_label["text"] = self.video_title[:30] + "..."
            self.path_label.grid(row=1, column=1, padx=5, pady=5)
            value = int(self.v.get())

            if value == 0:
                self.video = stream.first()
            elif value == 1:
                self.video = stream.last()
            else:
                self.video = stream.last()
            self.size = self.video.filesize
            self.thumbnail_thread.join()

            thread3 = threading.Thread(target=self.create_TopLevel,name="thread3", args=(self.size,"thread3"))
            thread3.start()
            thread3.join()

        except Exception as e:
            if self.link.get() == "":
                self.st.set("Please Enter URL")
            else:
                self.status["bg"] = "gray"
                # log = open("log_file.txt", 'a')
                # log.write(format_exc())
                # log.close()
                self.st.set("")

    def create_TopLevel(self, video_size, name):

        size = (round(video_size / (1024 ** 2), 2))
        self.st.set("")
        self.top = Toplevel()
        self.top.geometry('300x180')
        self.top.title("Video-Size")
        self.top.resizable(width=False, height=False)
        self.top.configure(bg="white")
        Label(self.top, image=self.img).grid(row=0, column=0, columnspan=2, padx=40)
        Label(self.top, text="Size: {}MB DOWNLOAD?".format(size), bg=self.white, pady=10, font={"arial", 22, "bold"}) \
            .grid(row=1, column=0, padx=40, columnspan=2)
        Button(self.top, text='Yes', font={"arial", 12, "bold"},
               command=lambda: self.start_download(self.path_variable.get(), self.video)).grid(row=2, padx=40, column=0)
        Button(self.top, text='No', font={"arial", 12, "bold"},
               command=lambda: self.top.destroy()).grid(row=2, column=1)

    def start_download(self, path, video):
        self.top.destroy()
        thread4 = threading.Thread(target=self.start_download_thread, args=(path, video,))
        thread4.start()

    def start_download_thread(self, path, video):
        if path == '':
            video.download('/home/vikku/Downloads/VDM/')
        else:
            video.download(path)

    def openFile(self, Time, title, youtube_link, path):

        with open("/home/vikku/PycharmProjects/idm/frame2_content.txt", 'r+') as orignal:
            data = orignal.read()
            orignal.close()
        with open("/home/vikku/PycharmProjects/idm/frame2_content.txt", 'w') as modified:
            modified.write(Time + ", " + title + ", " + youtube_link + ", " + path + "\n" + data)
            modified.close()

    def processing(self, stream, chunk, file_handle, bytes_remaining):

        percent = int(((self.size - bytes_remaining) / self.size) * 100)
        self.st.set(str(percent) + "%")
        self.mpb["value"] = percent
        if percent >= 49:
            self.status["background"] = "dodger blue"

    def complete(self, stream, file_handle):
        try:
            if self.path_variable.get() == "":
                absolute_path = "/home/vikku/Downloads/VDM/"
            else:
                absolute_path = self.path_variable.get()
            x = float(os.path.getsize(os.path.join(absolute_path, self.string_manupulation(self.video_title)) + ".mp4")
                      / (1024 * 1024))
            self.st.set("Download Complete {0} MB".format(round(x, 2)))

        except Exception as E:
            self.st.set("|| Download Complete ||")
            print(E)

        finally:
            download_time = str(datetime.datetime.now())[:16]
            self.openFile(download_time, self.string_manupulation(self.video_title), self.link_variable.get(), absolute_path)
            sleep(0.5)
            self.populate(self.frame2)

    def doleft(self, kd):
        webbrowser.open_new_tab(kd)

    def doright(self, kd):
        Popen(["xdg-open", kd[:-1].strip()])

    def string_manupulation(self, s):
        l = list(string.ascii_letters)
        l.extend(list(string.digits))
        l.append(" ")
        p = ""
        for i in s:
            if i in l:
                p = p + i
        return p.strip()

if __name__ == '__main__':
    idm = Idm()
    idm.mainloop()

# ===================== Experiments ================================

'''
chpath= Label(frame1, text="Select path",bg=color,fg='blue')
chpath.grid(row=0,column=2,padx =5, pady=5)
f = font.Font(chpath, chpath.cget("font"))
f.configure(underline=True)
chpath.configure(font=f)
chpath.bind('<Button-1>',changepath)

    yt = YouTube(link_variable.get())
    stream = yt.streams.filter(progressive=True, file_extension='mp4')
    for i in stream.all():
        print(yt.title,end=" ")
        k = re.compile(r'\d\d\dp')
        mo = k.search(str(i))
        print(mo.group())
'''