#!/usr/bin/env python
# Copyright 2022 Ross Vicario

import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from numpy import linspace
from azim_trans import AzimuthalProjection

if len(sys.argv) != 2:
    print("Must have exactly 2 arguments: \"slug\" \"filename\"")
    exit(-1)

file = r'{}'.format(sys.argv[1])
# trim off the file extension
fileTrim = file.split('.')[0]

with open(file, 'r') as f:
    # 1) read the lat/lon from input  file

    # first line is header in a CSV
    line = f.readline().strip().split(',')

    if not line:
        print("File",f,"was empty")
        exit(-1)

    # find the indices of the lat/lon
    latInd = line.index("latitude")
    lonInd = line.index("longitude")

    # get the second line
    line = f.readline().strip().split(',')
    if not len(line):
        print("File",f,"had no data")
        exit(-1)

    # skip until the first recording was found
    while "NO_FIX" in line:
        line = f.readline().strip().split(',')

    if line[0] == '':
        print("File",f,"had no fixes")
        exit(-1)
    
    # 2) Convert the data from lat/lon to x/y

    # use the first GPS coordinate to center the Azimuthal Projection
    AP = AzimuthalProjection(float(line[latInd]),float(line[lonInd]))

    # start the list empty
    xPoints = []
    yPoints = []

    while line[0] != '':
        if "NO_FIX" in line:
            continue
        # convert the lat/lon to x/y plane
        x,y = AP.latlon_to_xy(float(line[latInd]),float(line[lonInd]))

        # add points to list
        xPoints.append(x)
        yPoints.append(y)

        # get the next line
        line = f.readline().strip().split(',')

    # 3) Create the graph

    plt.rcParams['axes.facecolor'] = '#E4E4E4'
    plt.rcParams['axes.axisbelow'] = True
    plt.grid(color='white',linewidth=1.5) 

    # g is the gradient for color map
    # g is used with scatter plot to indicate order
    g = linspace(start=0,stop=100,num=len(xPoints))

    # create the scatter plot. note that 0,0 is the starting point
    fig = plt.scatter(x=xPoints,y=yPoints,s=10,c=g,cmap='plasma_r')

    plt.title('GPS Recording: '+fileTrim,fontweight='bold')
    plt.xlabel('Easting (m)')
    plt.ylabel('Northing (m)')
    plt.yticks(rotation=45,ha='right')

    # save the plot as a pdf
    pdf = PdfPages(fileTrim+'.pdf')
    pdf.savefig()
    pdf.close()

    # display the plot
    plt.show()
