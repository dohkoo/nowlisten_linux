#!/usr/bin/python
# Small program to tell you what you're listening to on spotify and broadcast out to the whole wide world.
# author: Stesha Doku | stesha@steshadoku.com
# Last Updated Sept 5, 2021
# Intended for Python3


import tkinter as tk #adds tkinter
import dbus, datetime, sched, time
import os
import vars
from ftplib import FTP

s = sched.scheduler(time.time, time.sleep)
dir_path = os.path.dirname(os.path.realpath(__file__))

oldSong = ""

def get_song(whatupdate):
    global oldSong

    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                         "/org/mpris/MediaPlayer2")
    spotify_properties = dbus.Interface(spotify_bus,
                                        "org.freedesktop.DBus.Properties")
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")

    x = datetime.datetime.now()

    newSong = metadata['xesam:title']+ " - " + metadata['xesam:artist'][0]

    if newSong != oldSong:
        # To just print the title
        print(newSong+" is playing!")
        listening_data = metadata['xesam:title']+ "<br>" + metadata['xesam:artist'][0]

        f = open(dir_path+'/listening.txt', 'w')
        f.write(listening_data)
        f.close()
        oldSong = newSong

        ftpbroadcast()

        whatupdate["text"] = newSong + "\n" + x.strftime("%b %d, %Y %H:%M")

    window.after(30*1000, get_song, whatupdate)

def ftpbroadcast():
    global dir_path
    ftp = FTP(vars.ftp_host)
    ftp.login(vars.ftp_username, vars.ftp_password)
    with open(dir_path + '/listening.txt', 'rb') as f:
        ftp.storlines('STOR %s' % '/public_html/nowlisten/listening.txt', f)
    ftp.quit()

#sets up the desktop window items
window = tk.Tk()
window.title("Now Listening To")
window.minsize(350, 100)
#label = tk.Label(text="I'm now Listening to...\n")
#label.pack()
showsong = tk.Label(text="Song to go here")
showsong.pack()

quitbutt = tk.Button(text="EXIT", fg="red", command=window.destroy)
quitbutt.pack()

window.after(0, get_song, showsong)
window.mainloop()
