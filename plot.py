## Code owned by University College London
## Written 2020-2022
## Copyright info - See license file
## 
## the visualize_... methods are the interface methods
## i.e. the methods to directly call in your own code
##
## the first one is for 3D plot, if I remember correctly
## the second is for 2D plotting for the NTURGB+D dataset (only the 6 joints found in the EmoPain@Home dataset)
## the third is for 2D plotting for the EmoPain@Home dataset
##
## the plot visualization works better if you have normalized the joint positions data, e.g., into range -1 to 1
##
## they expect T x 6 x 3 joint_data - T represents the number of frames and 3 represents x, y, z axes -
## (the 6 joints, and their respective rows, expected are
##  chestbottom=0, thigh=1, upperarm=2, lowerleg=3, forearm=4, hip=5) 
## and 1 X T activity_labels to match
## activity_set = is the set of activity classes that exist in the data
## savefilepath = where you want to save the created video
##
## PS: I can't remember why I had different sets of methods for NTURGB+D and EmoPain@Home



import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy
import os










    
def visualize_results(joint_data, activity_labels, activity_set, savefilepath):

    joint_data = numpy.reshape(joint_data, (-1, 6, 3))
    #print(activity_labels)
    
    #print(joint_data.shape)
    #print(activity_labels.shape)
    
    ###plotting
    #setting up my plot and animation parameters
    plotvars = 'b.-'
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.set_title('Test')
    metadata = dict(title='Half Skeleton Animation', artist='Matplotlib')

    #initializing the animation
    skel, _, _ = VideoPlot.draw_halfskel(joint_data[0, :, :], ax, plotvars)
            
    anime = animation.FuncAnimation(fig, VideoPlot.update_skel, frames=5, #joint_data.shape[0], 
                                    fargs=(joint_data, skel, ax, plotvars, activity_labels, activity_set), 
                                    interval=0.3333, repeat=False)
    #saving the animation as a gif
    #you can choose to save as mp4, but you would need to use the FFMpegWriter for that
    #instead of the PillowWriter, but you need to install ffmpeg for this
    #https://www.gyan.dev/ffmpeg/builds/#release-builds
    #and put in the python folder specified in plt.rcParams['animation.ffmpeg_path']
    #above (near the import statements at the start of script
    #anime.save(savefilepath, writer=animation.PillowWriter(fps=15, metadata=metadata))
    writer=animation.FFMpegFileWriter(fps=60, metadata=metadata)
    writer.setup(fig, savefilepath, dpi=1000)
    anime.save(savefilepath, writer=writer)
    plt.show()


def visualize_results_2d_nturgbd(joint_data, activity_labels, activity_set, savefilepath):

    joint_data = numpy.reshape(data, (-1, 6, 3))

    #print(activity_labels)

    #print(joint_data.shape)
    #print(activity_labels.shape)
    
    ###plotting
    #setting up my plot and animation parameters
    plotvars = 'b.-'
    fig = plt.figure(figsize=(8, 8))#dpi=150, figsize=(8, 8))
    ax = fig.add_subplot()
    ax.set_title('Test')
    metadata = dict(title='NTURGBD Half Skeleton Animation', artist='Matplotlib')

    #initializing the animation
    skel, _, _ = VideoPlot.draw_halfskel_2d_nturgbd(joint_data[0, :, :], ax, plotvars)
            
    anime = animation.FuncAnimation(fig, VideoPlot.update_skel_2d_nturgbd, frames=500, #joint_data.shape[0], 
                                    fargs=(joint_data, skel, ax, plotvars, activity_labels, activity_set), 
                                    interval=0.3333, repeat=False)
    #saving the animation as a gif
    #you can choose to save as mp4, but you would need to use the FFMpegWriter for that
    #instead of the PillowWriter, but you need to install ffmpeg for this
    #https://www.gyan.dev/ffmpeg/builds/#release-builds
    #and put in the python folder specified in plt.rcParams['animation.ffmpeg_path']
    #above (near the import statements at the start of script
    #anime.save(savefilepath, writer=animation.PillowWriter(fps=15, metadata=metadata))
    writer=animation.FFMpegFileWriter(fps=60, metadata=metadata)
    writer.setup(fig, savefilepath)
    anime.save(savefilepath, writer=writer)
    plt.show()






def visualize_results_athome_2d(joint_data, activity_labels, activity_set, savefilepath):

    joint_data = numpy.reshape(data, (-1, 6, 3))
    activity_labels = numpy.repeat(labels, no_of_frames)
    #print(activity_labels)
    
    #print(joint_data.shape)
    #print(activity_labels.shape)
    
    ###plotting
    #setting up my plot and animation parameters
    plotvars = 'b.-'
    fig = plt.figure(figsize=(8, 8))#dpi=150, figsize=(8, 8))
    ax = fig.add_subplot()
    ax.set_title('Test')
    metadata = dict(title='Notch Half Skeleton Animation', artist='Matplotlib')

    #initializing the animation
    skel, _, _ = VideoPlot.draw_halfskel_2d(joint_data[0, :, :], ax, plotvars)
            
    anime = animation.FuncAnimation(fig, VideoPlot.update_skel_athome_2d, frames=joint_data.shape[0], 
                                    fargs=(joint_data, skel, ax, plotvars, activity_labels, activity_set), 
                                    interval=0.3333, repeat=False)
    #saving the animation as a gif
    #you can choose to save as mp4, but you would need to use the FFMpegWriter for that
    #instead of the PillowWriter, but you need to install ffmpeg for this
    #https://www.gyan.dev/ffmpeg/builds/#release-builds
    #and put in the python folder specified in plt.rcParams['animation.ffmpeg_path']
    #above (near the import statements at the start of script
    #anime.save(savefilepath, writer=animation.PillowWriter(fps=15, metadata=metadata))
    writer=animation.FFMpegFileWriter(fps=60, metadata=metadata)
    writer.setup(fig, savefilepath)
    anime.save(savefilepath, writer=writer)
    plt.show()




class VideoPlot():

    
    def draw_halfskel(halfaskel, ax, plotvars):



        ax.clear()
        ax.set(xlim3d=(-1, 1), xlabel='X')
        ax.set(ylim3d=(-1, 1), ylabel='Y')
        ax.set(zlim3d=(-1, 1), zlabel='Z')
        ax.set_axis_off()
        #ax.autoscale()
        ax.set_facecolor('w')


        halfaskel = numpy.reshape(halfaskel, (-1, 6, 3))
        t=0

        chestbottom=0
        thigh=1
        upperarm=2
        lowerleg=3
        forearm=4
        hip=5

        x = 0
        y = 2
        z = 1
        
        plotvarschest = 'ko-'
        #plotvarschest = plotvars

        skel = []


        chest_hip = ax.plot([halfaskel[t, chestbottom, x], halfaskel[t, hip, x]],
                [halfaskel[t, chestbottom, y], halfaskel[t, hip, y]],
                [halfaskel[t, chestbottom, z], halfaskel[t, hip, z]], plotvarschest)
        
        hip_thigh = ax.plot([halfaskel[t, hip, x], halfaskel[t, thigh, x]],
                [halfaskel[t, hip, y], halfaskel[t, thigh, y]],
                [halfaskel[t, hip, z], halfaskel[t, thigh, z]], plotvars)

        thigh_leg = ax.plot([halfaskel[t, thigh, x], halfaskel[t, lowerleg, x]],
                [halfaskel[t, thigh, y], halfaskel[t, lowerleg, y]],
                [halfaskel[t, thigh, z], halfaskel[t, lowerleg, z]], plotvars)

        arm_arm = ax.plot([halfaskel[t, upperarm, x], halfaskel[t, forearm, x]],
                [halfaskel[t, upperarm, y], halfaskel[t, forearm, y]],
                [halfaskel[t, upperarm, z], halfaskel[t, forearm, z]], plotvars)


        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        zlim = ax.get_zlim()
        predicted_activity_text = ax.text(xlim[0], ylim[0], (zlim[0]+zlim[1])/2.0, '')
        groundtruth_activity_text = ax.text(xlim[0], ylim[0], zlim[1], '')


        #print(chest_hip)
           
        skel.extend(chest_hip)
            
        skel.extend(hip_thigh)

        skel.extend(thigh_leg)

        skel.extend(arm_arm)

        

        return skel, groundtruth_activity_text
    


        
    def update_skel(tau, data, skel, ax, plotvars, labels, classes):

      
        groundtruth_activity_template = 'groundtruth activity = %s'
        

	## these are the classes expected in the dataset that I used
        #classes = ['bal', 'sit', 'rf', 'ssta',
                        'stas', 'sta', 'bend', 'walk']
    
        newskel, predicted_activity_text, groundtruth_activity_text = VideoPlot.draw_halfskel(data[tau, :, :], ax, plotvars)
    
        for oldp, newp in zip(skel, newskel):

            oldp.set_data_3d(newp.get_data_3d())

        #print(tau)
        #print(labels[tau,])
        groundtruth_activity_text.set_text(groundtruth_activity_template %(classes[labels[tau,]]))


        return skel, groundtruth_activity_text




    def draw_halfskel_2d_nturgbd(halfaskel, ax, plotvars):



        ax.clear()
        ax.set(xlim=(-1.5, 1.5), xlabel='X')
        ax.set(ylim=(-1.5, 1.5), ylabel='Y')
        ax.set_axis_off()
        #ax.autoscale()
        ax.set_facecolor('w')


        halfaskel = numpy.reshape(halfaskel, (-1, 6, 3))
        t=0

        chestbottom=0
        thigh=1
        upperarm=2
        lowerleg=3
        forearm=4
        hip=5

        x = 2
        z = 1
        
        plotvarschest = 'ko-'
        #plotvarschest = plotvars

        skel = []


        chest_hip = ax.plot([halfaskel[t, chestbottom, x], halfaskel[t, hip, x]],
                [halfaskel[t, chestbottom, z], halfaskel[t, hip, z]], plotvarschest)
        
        hip_thigh = ax.plot([halfaskel[t, hip, x], halfaskel[t, thigh, x]],
                [halfaskel[t, hip, z], halfaskel[t, thigh, z]], plotvars)

        thigh_leg = ax.plot([halfaskel[t, thigh, x], halfaskel[t, lowerleg, x]],
                [halfaskel[t, thigh, z], halfaskel[t, lowerleg, z]], plotvars)

        arm_arm = ax.plot([halfaskel[t, upperarm, x], halfaskel[t, forearm, x]],
                [halfaskel[t, upperarm, z], halfaskel[t, forearm, z]], plotvars)


        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        groundtruth_activity_text = ax.text(xlim[0], ylim[1], '')


        #print(chest_hip)
           
        skel.extend(chest_hip)
            
        skel.extend(hip_thigh)

        skel.extend(thigh_leg)

        skel.extend(arm_arm)

        

        return skel, groundtruth_activity_text


    

    def update_skel_2d_nturgbd(tau, data, skel, ax, plotvars, labels, classes):

        
        groundtruth_activity_template = 'groundtruth activity = %s'

	## these are the classes expected in the dataset that I used
 
        # classes = ['sit', 'reach', 'sit to stand',
        #                'stand to sit', 'stand', 'walk']
        
        # nturgbd_classes = ['drink water', 'eat meal', 'brush teeth', 'brush hair',
        #           'drop', 'pick up', 'throw', 'sit down', 'stand up',
        #           'clapping', 'reading', 'writing', 'tear up paper',
        #           'put on jacket', 'take off jacket', 'put on a shoe',
        #           'take off a shoe', 'put on glasses', 'take off glasses',
        #           'put on a hat/cap', 'take off a hat/cap', 'cheer up',
        #           'hand waving', 'kicking something', 'reach into pocket',
        #           'hopping', 'jump up', 'phone call', 'play with phone/tablet',
        #           'type on a keyboard', 'point to something', 'taking a selfie',
        #           'check time (from watch)', 'rub two hands', 'nod head/bow',
        #           'shake head', 'wipe face', 'salute', 'put palms together',
        #           'cross hands in front', 'sneeze/cough', 'staggering', 'falling down',
        #           'headache', 'chest pain', 'back pain', 'neck pain', 'nausea/vomiting',
        #           'fan self', 'punch/slap',
        #           'kicking', 'pushing', 'pat on back', 'point finger', 'hugging',
        #           'giving object', 'touch pocket', 'shaking hands', 'walking towards', 'walking apart']
    
        newskel, groundtruth_activity_text = VideoPlot.draw_halfskel_2d_nturgbd(data[tau, :, :], ax, plotvars)
    
        for oldp, newp in zip(skel, newskel):

            oldp.set_data(newp.get_data())

        #print(tau)
        #print(labels[tau,])
        groundtruth_activity_text.set_text(groundtruth_activity_template %(nturgbd_classes[labels[tau,]]))



        return skel, groundtruth_activity_text




     def draw_halfskel_2d(halfaskel, ax, plotvars):



        ax.clear()
        ax.set(xlim=(-1.5, 1.5), xlabel='X')
        ax.set(ylim=(-1.5, 1.5), ylabel='Y')
        ax.set_axis_off()
        #ax.autoscale()
        ax.set_facecolor('w')


        halfaskel = numpy.reshape(halfaskel, (-1, 6, 3))
        t=0

        chestbottom=0
        thigh=1
        upperarm=2
        lowerleg=3
        forearm=4
        hip=5

        x = 0
        z = 1
        
        plotvarschest = 'ko-'
        #plotvarschest = plotvars

        skel = []


        chest_hip = ax.plot([halfaskel[t, chestbottom, x], halfaskel[t, hip, x]],
                [halfaskel[t, chestbottom, z], halfaskel[t, hip, z]], plotvarschest)
        
        hip_thigh = ax.plot([halfaskel[t, hip, x], halfaskel[t, thigh, x]],
                [halfaskel[t, hip, z], halfaskel[t, thigh, z]], plotvars)

        thigh_leg = ax.plot([halfaskel[t, thigh, x], halfaskel[t, lowerleg, x]],
                [halfaskel[t, thigh, z], halfaskel[t, lowerleg, z]], plotvars)

        arm_arm = ax.plot([halfaskel[t, upperarm, x], halfaskel[t, forearm, x]],
                [halfaskel[t, upperarm, z], halfaskel[t, forearm, z]], plotvars)


        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        groundtruth_activity_text = ax.text(xlim[0], ylim[1], '')


        #print(chest_hip)
           
        skel.extend(chest_hip)
            
        skel.extend(hip_thigh)

        skel.extend(thigh_leg)

        skel.extend(arm_arm)

        

        return skel, groundtruth_activity_text 

            

    def update_skel_athome_2d(tau, data, skel, ax, plotvars, labels, classes):

        
        groundtruth_activity_template = 'groundtruth activity = %s'

	## these are the classes expected in the dataset that I used
        
       # classes = ['sit', 'reach', 'sit to stand',
                        'stand to sit', 'stand', 'walk']

       # athome_classes = ['bathroom_clean', 'bedsheet_change', 'window_clean',
       #         'dust', 'dust_sweep', 'doc_file',
       #         'clothe_dry', 'iron', 'wash_load_unload',
       #         'dish_wash_load', 'wash_load', 'wall_paint',
       #         'shelf_paint', 'lunch_prep', 'box_sort',
       #         'kitchen_sweep', 'room_tidy', 'dish_wash_unload',
       #         'shop_unload', 'wash_unload', 'vacuum',
       #         'car_vacuum', 'walk', 'wash_up',
       #         'garden_water', 'yoga']
    
        newskel, groundtruth_activity_text = VideoPlot.draw_halfskel_2d(data[tau, :, :], ax, plotvars)
    
        for oldp, newp in zip(skel, newskel):

            oldp.set_data(newp.get_data())

        #print(tau)
        #print(labels[tau,])
        groundtruth_activity_text.set_text(groundtruth_activity_template %(athome_classes[labels[tau,]]))
        


        return skel, groundtruth_activity_text
            
    








