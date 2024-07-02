import re
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk

#print to terminal asking for dvrscan filename
print("Input DVR scan filename with .txt extension: ")
txt = input()
#txt = "log.txt"
#created file name variable
edl = "event.edl"
#different fps variables
f23 = 24000/1001
f24 = 24.000
f29 = 30000/1001
f30 = 30.000
f59 = 60000/1001
f60 = 60.000
#auto timeline and Frame drop names
#print("Input title name.")
title = "Timeline" #input("")
fcm = "NON-DROP FRAME"
#print("Select AV type:")
#input()
av = "AX"
#time to add to recorded time
addtime = "01:00:00:00"
#source fps of videos
sourcefps = f60
#output or modified fps
selectedfps = f60
#get the location of python script location
scriptloc = os.path.dirname(os.path.realpath(__file__))
#get file save location
saveloc = scriptloc
#get current working directory
currentloc = os.getcwd()

#take the time and convert it to frames so it can have math operations performed on it
def timecodetoframes(value, fps):
    value = value.replace(".",":")
    return round(sum((frames * float(time) for frames, time in zip((3600 * fps, 60 * fps, fps, 1), value.split(":")))))

#take frames and convert to time of source or selected fps
def frameconverter(value,fps):
    return '{h:02d}:{m:02d}:{s:02d}:{f:02d}' \
            .format(h = int(value / (3600 * fps)),
                    m = int(value / (60 * fps) % 60),
                    s =int(value / fps % 60),
                    f =int(value % fps))

#convert time of source
def sconv(value, fps):
    tmcd = timecodetoframes(value, fps)
    return (frameconverter(tmcd, fps))

#convert time of source with added value of timeline/recording value
def conv(value, addvalue, fps):
    tmcd = timecodetoframes(value, fps)
    rectime = timecodetoframes(addvalue, fps)
    ntime = rectime + tmcd
    return (frameconverter(ntime, fps))

#create a new file and setup base output for the file with Title : Timeline and FCM: Non-drop frame then closes the file
def createfile(value):
    f = open(scriptloc+"\\"+value, 'w')
    f.write("TITLE: " + title + "\n")
    f.write("FCM: " + fcm + "\n\n")
    f.close()

#opens the file, adds the value to file then closes the file
def add(value):
    f = open(scriptloc+"\\"+edl, 'a')
    f.write(value)
    f.close()

#call the creation of the edl file and give it the "event.edl" name
createfile(edl)

#opens the file, then creates variables for the line numbers and clipname
def createlines():
    with open(scriptloc+"\\"+txt) as file:
        numi = 1
        clipname = ""

        #loop over each line of the dvrscan file and search for the video name and add it to the clipname variable
        for line in file:
            if re.findall("Opened video", line):
                line = re.sub(r"\[DVR-Scan] Opened video ", "", line)
                line = line.replace(" (3840 x 2160 at 23.976 FPS).", "")
                clipname = line
            #loop over each line and search for the source in and out times and then remove unnecessary parts of the output
            if re.findall("[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9]", line):
                line = re.sub(r"Event    [0-9]", "", line)
                line = re.sub(r"Event   [0-9][0-9]", "", line)
                line = re.sub(r"Event  [0-9][0-9][0-9]", "", line)
                line = line.replace("|", "")
                line = line.replace(".",":")
                #split up the lines based on spaces for easier access of functions
                line = line.split(" ")
                #convert the source time from string to int so math can be performed then back to string
                sourcein = sconv((line[6]), sourcefps)
                #durat = sconv(line[10]), sourcefps)
                sourceout = sconv((line[14]), sourcefps)
                #convert the source time to selected fps and add the base time for the timeline
                recin = conv((line[6]), addtime, selectedfps)
                recout = conv((line[14]), addtime, selectedfps)
                #place the numbers for each line in correct format and then step forward to next number
                num = '{0:0>3}'.format(numi)
                numi += 1
                #printing the values of each to the terminal for diagnostic
                print(f'{sourcein} {sourceout} {recin} {recout}')
                #fill out line in event.edl file and make an empty line
                add(f'{num}  {av}       V     C        {sourcein} {sourceout} {recin} {recout}  \n')
                add(f'* FROM CLIP NAME: {clipname}\n')

createlines()
#print value of frames of the time to add to the record time to terminal for diagnostic
#print(timecodetoframes(addtime, selectedfps))
#print paths for diagnostics
#print(scriptloc)
#print(currentloc)
#print completed location to terminal to show operation is complete
print(f'Completed, event.edl placed in {saveloc} directory')