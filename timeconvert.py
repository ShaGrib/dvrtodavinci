import re
from datetime import datetime
import math

#setup
#dvrscan filename
print("Input DVR scan filename with .txt extension: ")
txt = input()
#created file name
edl = "event.edl"
#different fps
f23 = 24000/1001
f24 = 24.000
f29 = 30.000/1001
f30 = 30.000
f59 = 60.000/1001
f60 = 60.000
#auto timeline and Frame drop names
title = "Timeline" #input("Input Title:")
fcm = "NON-DROP FRAME" #input("Input Frame type:")
av = "AX"
#time to add to recorded time
btime = 86400

#
def timecodetoframes(value, fps):
    value = value.replace(".",":")
    return round(sum((frames * float(time) for frames, time in zip((3600 * fps, 60 * fps, fps, 1), value.split(":")))))

def frameconverter(value,fps):
    return '{h:02d}:{m:02d}:{s:02d}:{f:02d}' \
            .format(h = int(value / (3600 * fps)),
                    m = int(value / (60 * fps) % 60),
                    s =int(value / fps % 60),
                    f =int(value % fps))

def sconv(value, fps):
    tmcd = timecodetoframes(value, fps)
    return (frameconverter(tmcd, fps))


def conv(value, fps):
    tmcd = timecodetoframes(value, fps)
    tmcd = tmcd+btime
    return (frameconverter(tmcd, fps))

def createfile(value):
    f = open(value, 'w')
    f.write("TITLE: " + title + "\n")
    f.write("FCM: " + fcm + "\n\n")
    f.close()

def add(value):
    f = open(edl, 'a')
    f.write(value)
    f.close()

createfile(edl)

with open(txt) as a:
    numi = 1
    clipname = ""

    
    for line in a:
        if re.findall("Opened video", line):
            line = re.sub(r"\[DVR-Scan] Opened video ", "", line)
            line = line.replace(" (3840 x 2160 at 23.976 FPS).", "")
            clipname = line
        if re.findall("[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9]", line):
            b = re.sub(r"Event    [0-9]", "", line)
            c = re.sub(r"Event   [0-9][0-9]", "", b)
            d = re.sub(r"Event  [0-9][0-9][0-9]", "", c)
            e = re.sub("\|", "", d)
            f = e.replace(".",":")
            g = re.sub("\s+$", "", f)
            h = g.split(" ")
            sourcein = sconv((h[6]), f23)
            #durat = sconv(h[10]), f23)
            sourceout = sconv((h[14]), f23)
            recin = conv((h[6]), f23)
            recout = conv((h[14]), f23)
            num = '{0:0>3}'.format(numi)
            numi += 1
            add(f'{num}  {av}       V     C        {sourcein} {sourceout} {recin} {recout}  \n* FROM CLIP NAME: {clipname}')
            add("\n")
