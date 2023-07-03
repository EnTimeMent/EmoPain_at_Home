## Code owned by University College London
## Written 2020-2022
## Copyright info - See license file
## 
## **Note** - getfulldata() is based on the _read_skeleton() method
## in https://github.com/shahroudy/NTURGB-D/blob/master/Python/txt2npy.py

### - This file contains the class for processing NTU RGB+D joints position data
### - to match the EmoPain@Home dataset, for the purpose of representation learning


import csv
import os
import json
import numpy
from sklearn.preprocessing import OneHotEncoder
from dataClass import *
from angle import *


rightjointids = {'chestbottom': '1', 'thigh':'17', 'upperarm':'9', 'lowerleg':'18', 'forearm':'10', 'hip':'0'}
leftjointids = {'chestbottom': '1', 'thigh':'13', 'upperarm':'5', 'lowerleg':'14', 'forearm':'6', 'hip':'0'}

joints = ['chestbottom', 'thigh', 'upperarm', 'lowerleg', 'forearm', 'hip']
fixedseqlen = 240
randomseed = 1


class NTURGBDdata:

    def __init__(self, datafolderpath):

        self.preloaded_data = NTURGBDdata.preload(datafolderpath)
        print("preloaded done")
        

    def preload(datafolderpath):

        preloadeddata = {}

        ind = 0

        for filename in os.listdir(datafolderpath):

            preloadeddata[str(ind)] = os.path.join(datafolderpath, filename)
            
            ind += 1        

        return preloadeddata


    def get_instance_indices(self):

        instanceids = []

        for key in self.preloaded_data:

            instanceids.append(int(key))

        return numpy.array(instanceids)


    def get_subject_indices(self):

        instanceids = []
        subjectids = []

        for key in self.preloaded_data:

            instanceids.append(int(key))
            filename = os.path.basename(self.preloaded_data[key])
            subjectids.append(int(filename[9:12]))

        return numpy.array(instanceids), numpy.array(subjectids)
    

    def get_task_indices(self):

        instanceids = []
        taskids = []

        for key in self.preloaded_data:

            instanceids.append(int(key))
            filename = os.path.basename(self.preloaded_data[key])
            task_and_ext = filename[17:].split('.')
            taskids.append(int(task_and_ext[0]))

        return numpy.array(instanceids), numpy.array(taskids)




    def one_hot_enc(num_classes, class_label):

        #print(class_label)

        enc = numpy.zeros((1, num_classes))

        enc[:, class_label] = 1

        return enc
    

    def preprocess(self, instanceids):

        #counter = 0

        data = numpy.array([])
        #otherdata = numpy.array([])



        for key in instanceids:

            #print(counter)
            #counter+=1

            try:
                tempdata = NTURGBDdata.getfulldata(self.preloaded_data[key])
            except KeyError:
                tempdata = NTURGBDdata.getfulldata(self.preloaded_data[key.decode()])


            for body in tempdata:

            

                leftjoints = []
                rightjoints = []

                for j in joints:

                    rightjoints.append(tempdata[body][rightjointids[j]])
                
                #for j in joints:

                    #leftjoints.append(tempdata[body][leftjointids[j]])


                temptempdata = NTURGBDdata.preprocess_basic(rightjoints)

                if temptempdata.shape[0] > 0:
            
                    if data.shape[0]==0:

                        data = copy.deepcopy(temptempdata)
                        #otherdata = copy.deepcopy(tempotherdata)
                        #data = numpy.concatenate([data, NTURGBDdata.preprocess_basic(leftjoints)], axis=0)

                    else:

                        data = numpy.concatenate([data, temptempdata], axis=0)
                        #otherdata = numpy.concatenate([otherdata, tempotherdata], axis=0)


        #startdata = numpy.reshape(startdata, (startdata.shape[0], -1))
        #scaledstartdata, _ = Data.normalize(startdata, scaletype='minmax', minmax_featurerange=(-1, 1))
        n_instances = data.shape[0]
        dur_instances = data.shape[1]
        data = numpy.transpose(numpy.reshape(data, (data.shape[0]*data.shape[1], -1)), (1, 0))
        scaleddata, _ = Data.normalize(data, scaletype='minmax', minmax_featurerange=(-1, 1))

        #scaledstartdata = numpy.reshape(scaledstartdata, (scaledstartdata.shape[0], 1, -1, 3))
        scaleddata = numpy.reshape(numpy.transpose(scaleddata, (1, 0)), (n_instances, dur_instances, -1, 3))

        idealdiff = numpy.zeros((scaleddata.shape[0], 1))

        alldata = []
        alldata.append(scaleddata)
        #alldata.append(scaledotherdata)

        alldata.append(idealdiff)



        return (scaleddata, alldata)



    def preprocess_raw_with_task(self, instanceids):

        #counter = 0


        data = numpy.array([])
        #otherdata = numpy.array([])
        tasks = numpy.array([])
        persons = numpy.array([])


        for key in instanceids:

            #print(counter)
            #counter+=1

            
            tempdata = NTURGBDdata.getfulldata(self.preloaded_data[str(key)])
                

            filename = os.path.basename(self.preloaded_data[str(key)])
            task_and_ext = filename[17:].split('.')
            
            task = numpy.reshape(int(task_and_ext[0])-1, (1, 1))
            #print(task)


            for body in tempdata:

                

                    leftjoints = []
                    rightjoints = []

                    for j in joints:

                        rightjoints.append(tempdata[body][rightjointids[j]])
                    
                    #for j in joints:

                        #leftjoints.append(tempdata[body][leftjointids[j]])


                    temptempdata = NTURGBDdata.preprocess_basic(rightjoints)

                    if temptempdata.shape[0] > 0:
                
                        if data.shape[0]==0:

                            data = copy.deepcopy(temptempdata)
                            #otherdata = copy.deepcopy(tempotherdata)
                            #data = numpy.concatenate([data, NTURGBDdata.preprocess_basic(leftjoints)], axis=0)
                            tasks = numpy.copy(task)
                        else:

                            data = numpy.concatenate([data, temptempdata], axis=0)
                            #otherdata = numpy.concatenate([otherdata, tempotherdata], axis=0)
                            tasks = numpy.concatenate([tasks, task], axis=0)
                
                


        n_instances = data.shape[0]
        dur_instances = data.shape[1]

        #scaledstartdata = numpy.reshape(scaledstartdata, (scaledstartdata.shape[0], 1, -1, 3))
        data = numpy.reshape(data, (n_instances, dur_instances, -1, 3))



        return data, tasks
    


    def preprocess_basic(jointsdatalist):

        jointsdata = numpy.array(jointsdatalist)
        #if jointsdata.shape[1] <= 1: return numpy.array([])
        jointsdata = numpy.transpose(jointsdata, (1, 0, 2))
        jointsdata = numpy.expand_dims(jointsdata, axis=0)


        #startjointsdata = jointsdata[:, 0, :, :]
        #otherjointsdata = jointsdata[:, 1:, :, :] - startjointsdata
        

        if jointsdata.shape[1] < fixedseqlen: jointsdata = NTURGBDdata.loopseq_pad(jointsdata)
        #if jointsdata.shape[1] < fixedseqlen: jointsdata = NTURGBDdata.last_pad(jointsdata)
        if jointsdata.shape[1] > fixedseqlen: jointsdata = jointsdata[:, :fixedseqlen, :, :]
        #print(jointsdata.shape)
        
        return jointsdata
    


    def loopseq_pad(arr):

        #print(arr.shape[1])

        while arr.shape[1] < fixedseqlen:

            padlen = fixedseqlen - arr.shape[1]
            padarr = arr[:, :padlen, :, :]

            if len(padarr.shape) == 3: padarr = numpy.expand_dims(padarr, axis=1)

            arr = numpy.concatenate([arr, padarr], axis=1)


        return arr



    def last_pad(arr):

        last_val = arr[:, arr.shape[1]-1, :, :]

        padlen = fixedseqlen - arr.shape[1]

        padarr = numpy.expand_dims(last_val, axis=1)
        padarr = numpy.repeat(padarr, padlen, axis=1)


        arr = numpy.concatenate([arr, padarr], axis=1)


        return arr


    

    #based on the _read_skeleton() method
    #in https://github.com/shahroudy/NTURGB-D/blob/master/Python/txt2npy.py
    def getfulldata(datafilepath):

        f = open(datafilepath, 'r')
        data = f.readlines()
        f.close()

        numofjoints = 25
        numofframes = int(data[0][:-1])

        row = 1
        fulldata = {}

        for frame in numpy.arange(0, numofframes):
            
            numofbodies = int(data[row][:-1])
            row += 1
            
            if numofbodies == 0:
                continue 
            ### skip the empty frame 
            ##bodymat['nbodys'].append(bodycount)
            for body in numpy.arange(0, numofbodies):
               
                
                bodyinfo = data[row][:-1].split(' ')
                bodyid = bodyinfo[0]
                row += 1

                if bodyid in fulldata:

                    bodydata = fulldata[bodyid]

                else:

                    bodydata = {}

                
                
                numofjoints = int(data[row][:-1])
                row += 1
                
                for joint in numpy.arange(0, numofjoints):

                    if str(joint) in bodydata:
                        jointdata = bodydata[str(joint)]
                        
                    else:
                        jointdata = []

                    
                    jointframedata = data[row][:-1].split(' ')
                    jointframedata = [float(val) for val in jointframedata[:3]]
                    jointdata.append(jointframedata)
                    bodydata[str(joint)] = jointdata

                    
                    row += 1

                fulldata[bodyid] = bodydata
                
        return fulldata


