import matplotlib.pyplot as plt
import os
import csv
base=os.getcwd()
path=str(base)+str(os.sep)+"comm_size_files/"
nums=[802,810,822,834,844,853,863,878,883,999]
algs=["edmot","label","gemsec","scd"]
name={'label':"Label Propagation",'edmot':"EdMot",'gemsec':"GEMSEC",'scd':"SCD"}
suffix=".csv"
store={}
x_axis=[1,2,3,4,5,6,7,8,9,10]
for alg in algs:
    path2=path+alg+"/"
    file1=path2+alg+"_"
    file2=path2+"comm_map_after_slice"
    store={}
    for i in range(0,len(nums)):
        num=nums[i]
        prev_num=nums[i-1]
        if i==0:
            file=open(file1+str(num)+suffix,"r")
            creader=csv.reader(file)
            fields=next(creader)
            for row in creader:
                comm,size=map(int,row)
                store[comm]={i+1:size}
            file.close()

        else:
            file=open(file1+str(num)+suffix,"r")
            creader=csv.reader(file)
            fields=next(creader)
            to_add={}
            for row in creader:
                comm,size=map(int,row)
                to_add[comm]=size
                try:
                    store[comm][i+1]=size
                except:
                    store[comm]={i+1:size}
            file.close()
            fileafter=open(file2+str(prev_num)+suffix,"r")
            creader=csv.reader(fileafter)
            fields=next(creader)
            for row in creader:
                comm_from,comm_to=map(int,row)
                store[comm_from][i+1]=to_add[comm_to]
            fileafter.close()
    for comm in sorted(store.keys()):
        d=store[comm]
        #print(comm,store[comm])
        j=0
        x=[]
        y=[]
        for i in d.keys():
            if i==j+1 or len(x)==0:
                j=i
                x.append(i)
                y.append(d[i])
            else:
                j=i
                plt.plot(x,y)
                x=[i]
                y=[d[i]]
        plt.plot(x,y)
    plt.xlabel('Time')
    # Set the y axis label of the current axis.
    plt.ylabel('Community Size')
    # Set a title of the current axes.
    plt.title('Community Size Changes for %s'%name[alg])
    # show a legend on the plot
    # Display a figure.
    plt.savefig(str(base)+str(os.sep)+"sizes/%s_comm_sizes.png"%name[alg])
    plt.figure().clear()
    plt.close()
