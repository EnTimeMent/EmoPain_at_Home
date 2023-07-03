
## Code owned by University College London
## Written 2020-2022
## Copyright info - See license file

### - This file contains the methods for extracting joints position data from the EmoPain@Home dataset
### - as well as extracting self-report labels from the dataset.

import csv
import os
import json
import numpy



def loadalldata(sourcefolder):

    participantdata = {}
    alldata = {}


    for folder in os.listdir(sourcefolder):
        #print(p)
        
        foldernamesplit = folder.split("_")
        pid = int(foldernamesplit[0][1:])
        #print(pid)
	activitylabelsplit = foldernamesplit[1].split(".")
	activity_label = activitylabelsplit[0]
	#print(activity_label)


	
	ddata, ddatadatetime = getfulldata(os.path.join(sourcefolder, folder)
        if len(ddata) != 0: participantdata[ddatadatetime] = ddata
	if len(participantdata) != 0: alldata[str(pid)] = participantdata


    print("all data now loaded")    
    print("")

    #print(alldata)

    return alldata




def getfulldata(datafolderpath):

    fulldata = {}

    meta = getmeta(datafolderpath)

    if len(meta) == 0: return fulldata, None
    
    year, month, day, hour, minute, second = getstarttime(meta)
    samplingrate = float(meta['frequency'])
    framecount = int(meta['frame_count'])
    fulldata['year'] = year
    fulldata['month'] = month
    fulldata['day'] = day
    fulldata['hour'] = hour
    fulldata['minute'] = minute
    fulldata['second'] = second
    fulldata['samplingrate'] = samplingrate
    fulldata['framecount'] = framecount
    fulldatakey = '_'.join([str(year), str(month), str(day), str(hour), str(minute)])
    
    dfiles = getfoldercontent(datafolderpath, '', 'meta')
    for file in dfiles:
        data, bone, isdata = getbonedata(file, meta)
        if isdata: fulldata[bone] = data

    return fulldata, fulldatakey


def getmeta(datafolderpath):

    meta = {}

    if os.path.getsize(os.path.join(datafolderpath, 'meta.json')) == 0: return meta

    with open(os.path.join(datafolderpath, 'meta.json')) as metafile:


        meta = json.load(metafile)
        
    return meta


def getstarttime(meta):
    
    datetimecode = meta['measured']
    datetimecodesplit = datetimecode.split('T')
    datesplit = datetimecodesplit[0].split('-')
    year = int(datesplit[0])
    month = int(datesplit[1])
    day = int(datesplit[2])
    
 
    timesplit = datetimecodesplit[1].split(':')
    hour = int(timesplit[0])
    minute = int(timesplit[1])
    secondandmilli = timesplit[2].split('+')
    secondandmillisplit = secondandmilli[0].split('.')
    millisecond = float(secondandmillisplit[1][:3])    
    second = float(secondandmillisplit[0]) + millisecond/1000.0

    return year, month, day, hour, minute, second
     

def getbonedata(fullfilename, meta):

    dataarr  = numpy.array([])
    isbonedata = False

    fullfilenamesplit = os.path.split(fullfilename)
    filenamesplit = fullfilenamesplit[1].split('.')
    fileext = filenamesplit[1]
    
    filenamesplit = filenamesplit[0].split('_')
    angleorpos = filenamesplit[0]
    bone = filenamesplit[1]

    
    if fileext == 'csv' and angleorpos.lower()=='positions' and isinbones(meta['bones'], bone):

        isbonedata = True

        with open(fullfilename, 'r') as csvfile:

            data = []         
            rowcount = 0
            myreader = csv.reader(csvfile)

            for row in myreader:

                if rowcount >= 1:

                    valcount = 0
                    temp = []

                    for val in row:


                        if valcount >=1 and valcount <=3:
                            temp.append(float(val))

                        valcount+=1 


                    data.append(temp)

                rowcount+=1
            dataarr = numpy.array(data)

            #print(dataarr.shape)

    return dataarr, bone, isbonedata


def isinbones(bonelist, bone):

    for b in bonelist:

        if b==bone: return True

    return False


def getfoldercontent(folderpath, inclusion, exclusion):

    content = []

    if not os.path.isdir(folderpath): return content
            
    for c in os.listdir(folderpath):

        fits = True

        if inclusion!='' and (inclusion.lower() not in c.lower()): fits = False
        if exclusion!='' and (exclusion.lower() in c.lower()): fits = False 
            
        if fits: content.append(os.path.join(folderpath, c))

    return content
    


def load_selfreport_labels(sourcefile):

    with open(sourcefile, 'r') as csvfile:

        labels = {}

        rowcount = 0
        myreader = csv.reader(csvfile)

        for row in myreader:

            if rowcount >= 1:

                valcount = 0
                painworryconfidence = []
                instance = {}

                for val in row:

                    if valcount == 0:
                        pid = int(val)

                    elif valcount == 2:
                        activity = int(val)

                    elif valcount == 4:
                        challenging = False
                        if val.lower() == 'yes': challenging = True

                    elif valcount == 5:
                        day = int(val)
                         
                    elif valcount == 6:
                        month = int(val)

                    elif valcount == 7:
                        year = int(val)
                     
                    elif valcount == 8:
                        hour = int(val)

                    elif valcount == 9:
                        minute = int(val)

                    elif valcount == 10:
                        painworryconfidence.append(float(val))

                    elif valcount == 11:
                        painworryconfidence.append(float(val))

                    elif valcount == 12:
                        painworryconfidence.append(float(val))

                    elif valcount == 13:
                        sequence = int(val)
                     
                    valcount += 1

                instancekey = '_'.join([str(pid), str(year), str(month), str(day), str(hour), str(minute)])
                instance['activity'] = activity
                instance['challenging'] = challenging
                instance['labels'] = painworryconfidence
                instance['sequenceid'] = (pid*20)+sequence
                labels[instancekey] = instance

            rowcount += 1


        
    
    print("all labels now loaded")
    print("")

    #print(labels)

    return labels
                 


    
        






        
