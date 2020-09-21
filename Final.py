# Beautified the GUI with ttkthemes and adjusted spaces using padx and pady 
import os
import time

import threading 
from tkinter import * 
from tkinter import ttk
from pygame import mixer
import tkinter.messagebox
from mutagen.mp3 import MP3
from tkinter import filedialog
from ttkthemes import themed_tk as tk



#______________________________________________________________________________
""" Initializing the Mixer """

mixer.init()  


#______________________________________________________________________________
""" Defining the Window """

root = tk.ThemedTk() 
root.get_themes()
root.set_theme("clam")
# themes that can be used- smog, radiance, vista, winxpblue,classic,clam,breeze,


root.title("Melody") 
root.iconbitmap(r'images/melody.ico')


#______________________________________________________________________________
""" Status Bar """

statusbar = ttk.Label(root, text="Welcome to Melody", relief=SUNKEN, anchor=W, font = 'Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)


#______________________________________________________________________________
""" Creating the MENU BAR """

menubar = Menu(root)
root.config(menu=menubar)


#______________________________________________________________________________
""" SubMenu 1 - File """

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File",menu=subMenu)

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    print(filename_path)
    add_to_playlist(filename_path)
    
    
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


#______________________________________________________________________________
""" SubMenu 2 - Help """

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help",menu=subMenu)

def about_us():
    tkinter.messagebox.showinfo('Melody','This is a Music Player built using python tkinter by Vishesh Mongia')
subMenu.add_command(label="About Us", command = about_us)


#______________________________________________________________________________
""" Defining Left and Right Frame """

# Left Frame = Playlist + addBtn + delBtn 

leftframe = Frame(root)
leftframe.pack(side=LEFT,padx=30,pady=30)

# Right Frame = TopFrame + MiddleFrame + BottomFrame

rightframe=Frame(root)
rightframe.pack(pady=30)


"""Right Frame Starts From Here"""
#______________________________________________________________________________
""" Top Frame (in Right Frame) """


topframe = Frame(rightframe)
topframe.pack()


#______________________________________________________________________________
""" Length Of Song (in TopFrame)"""

lengthlabel = ttk.Label(topframe, text = 'Total Length : --:--')
lengthlabel.pack(pady=5)



def show_details(play_song):
   
    file_data = os.path.splitext(play_song)
    
    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
    
    #div - gives quotient to mins and remainder to secs
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text'] = "Total Length" + ' - ' +timeformat
    
    t1 = threading.Thread(target=start_count,args=(total_length,)) # Used to look after two things at same time
    t1.start()


#______________________________________________________________________________
""" Current Time (in TopFrame)""" 
    
currenttimelabel = ttk.Label(topframe, text= 'Current Time :  --:--', relief=GROOVE)
currenttimelabel.pack()


def start_count(t):
    global paused
    # mixer.music.get_busy(): Returns False when we press stop button (music stop playing)
    current_time=0
    while current_time<=t and mixer.music.get_busy():
        
        
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins,secs)
            currenttimelabel['text'] = "Current Length" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


#______________________________________________________________________________
""" Middle Frame (in Right Frame) """

middleframe = Frame(rightframe)
middleframe.pack(pady=30,padx=30)


#______________________________________________________________________________
""" Play Option (in Middle Frame)"""

def play_music():
    global paused   # Checks if 'paused' is initialized or not
    
    if paused:      # If pause=TRUE
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"        
        paused = FALSE
        
    else:           # If pause=FALSE
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text']= "Playing Music" + ' - ' +os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found','You have not selected any file to be played')
        
  
        
playPhoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0,column=0,padx=10)


#______________________________________________________________________________
""" Pause Option (in Middle Frame)"""

paused = FALSE

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"
    
    
pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0,column=1,padx=10)
 

#______________________________________________________________________________
""" Stop Option (in Middle Frame)"""

def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"
    
stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0,column=2,padx=10)


#______________________________________________________________________________
""" Bottom Frame (in Right Frame) """

bottomframe = Frame(root)
bottomframe.pack()


#______________________________________________________________________________
""" Rewind Option (in Bottom Frame) """

def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"
    
rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0,column=0)


#______________________________________________________________________________
""" Mute Option (in Bottom Frame) """

muted = FALSE
def mute_music():
    global muted
    if muted:   # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image = volumePhoto)
        statusbar['text'] = "Music" + ' - ' +os.path.basename(filename_path)
        scale.set(70)
        muted = False
    else:       # Mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image = mutePhoto)
        statusbar['text'] = "Mute"
        scale.set(0)
        muted = TRUE
mutePhoto = PhotoImage(file='images/mute.png')   
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0,column=1)


#______________________________________________________________________________
""" Volume Option (in Bottom Frame) """

def set_vol(val):
    volume = float(val)/100
    mixer.music.set_volume(volume)
    
scale = ttk.Scale(bottomframe, from_=0, to=100, orient= HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0,column=2,padx = 15,pady=30) 

""" Left Frame starts From Here """
#______________________________________________________________________________
""" Playlist Option (in Left Frame) """

playlist = []
playlistbox = Listbox(leftframe)
playlistbox.pack()
def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index=0
    playlistbox.insert(index,filename)
    playlist.insert(index,filename_path)
    index += 1

#______________________________________________________________________________
""" Add and Del Buttons (in Left Frame) """

# Add Button
addBtn = ttk.Button(leftframe, text = "+ Add", command=browse_file)
addBtn.pack(side=LEFT)

# Del Button
def del_song():
    
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)
    
delBtn = ttk.Button(leftframe, text = "- Del", command= del_song)
delBtn.pack(side=LEFT)


#______________________________________________________________________________
""" Closing The Window-Root """

def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW",on_closing) # Over riding red cross
root.mainloop() 

""" Summary """
# 1- First of all Menu bar and Status bar are made
# 2- Then whole window is divided in two parts - Left and Right 
# 3- Then Right side is defined which is further divided into Top, Middle and Bottom Frames
# 4- Then Top frame containing (Length and Current) Time of Song is defined
# 5- Then Middle frame containing (Play , Pause and Stop) options is defined
# 6- Then Bottom frame containing (Rewind , Mute and Volume Scale) options is defined  
# 7- Then the window is closed    
    
# Styles that can be used - normal,bold,roman,italic,underline,overstrike
# Fonts that can be used - Arial, ComicSans, Fixedsys, MS Sans Serif, MS Serif, Courier New (Courier)
#     , Times New Roman(Times), Verdana  
    