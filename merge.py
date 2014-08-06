#This file is to merge two or more files containing the best scores of different times.

import moving_max, get_data
import random 
import math, multiprocessing, time
import os 
import exceptions 
import string 
import re
import ast
import glob
import main

#input two or more dates that you want to merge
#for someotherfilename, type 'someotherfilename'

#obtain all files with the format 'scores*_best' to merge
merge_input = glob.glob(main.get_save_dir() + 'best/' + 'scores*_best') 
#specify output file name
merge_output = 'output.txt'

#takes only the file name instead of the full path
for i in range(len(merge_input)):
    merge_input[i] = merge_input[i].split('/')[-1]

#if you want to merge with your current output
#Note: will give an error if merge_output does not exist yet
merge_input.append(merge_output) #comment this line out if you do not want to

f = [0]*len(merge_input)
content = [0]*len(merge_input)

#merges two files
def merge(content1, content2):
    #joins the list
    merged_file = content1 + content2 
    #uses a 2-D array called merged_list to save all information
    merged_list = [[0 for x in xrange(3)] for x in xrange(len(merged_file))] 
    for i in range(len(merged_file)):
        merged_list[i][0] = int(merged_file[i].split(' / ')[0]) #extracting date info
        merged_list[i][1] = ast.literal_eval(merged_file[i].split(' / ')[1]) #extracting parameter info
        merged_list[i][2] = float(merged_file[i].split(' / ')[2]) #extracting scores as float
   
    merged_list.sort(key=lambda x: (x[0] , x[2])) #sort data by chronological order, then by score

    temp = {}

    #assign parameters and scores into each date and time
    #when two dates have different ''best'' scores, the best one will be used because
    #the data are sorted
    for m,v,n in merged_list:
        temp[m] = v,n

    temp_file = open(main.get_save_dir() + 'best/temp_file.txt','w') 
    temp_file = open(main.get_save_dir() + 'best/temp_file.txt','a') 
    
    #writing results into temp_file
    for m in sorted(temp.iterkeys()):
        temp_file.write(str(m)+' / '+str(temp[m][0])+' / '+str(temp[m][1])+'\n')

    temp_file = open(main.get_save_dir() + 'best/temp_file.txt','r') 
    
    return temp_file.readlines()


"""def combine(file1, file2, first_date1, first_date2, last_date1, last_date2):
    if max(first_date1, first_date2) < min(last_date1, last_date2):
        merge(file1, file2)

    merge(content[0], content[0])"""


#f[i] opens the i-th file as specified in merge_input
#content[i] reads the i-th file
for i in range(len(merge_input)):
    f[i] = open(main.get_save_dir() + 'best/' + str(merge_input[i]),'r')
    content[i] = f[i].readlines()

#merges content[i] and content[i+1]
#saves output_content in content[i+1]
#repeats until all contents are merged
for i in range(len(merge_input)-1):
    output_content = merge(content[i], content[i+1])
    content[i+1] = output_content

#opens output file
g = open(main.get_save_dir() + 'best/' + merge_output,'w') 
g = open(main.get_save_dir() + 'best/' + merge_output,'a') 

#uses a 2-D array called output_file to save all information
output_file = [[0 for x in xrange(3)] for x in xrange(len(output_content))] 

for i in range(len(output_file)):
    output_file[i][0] = output_content[i].split(' / ')[0] #extracting date string
    output_file[i][1] = ast.literal_eval(output_content[i].split(' / ')[1]) #extracting parameter info
    output_file[i][2] = output_content[i].split(' / ')[2] #extracting scores string

    #write all file into merge_output
    g.write(output_file[i][0] + ' / ' + str(output_file[i][1]) + ' / ' + output_file[i][2])

g.close() 
