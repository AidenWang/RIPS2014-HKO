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
#for scores.txt_yyyymmddhhnn_best, type yyyymmddhhnn
#for someotherfilename, type 'someotherfilename'

merge_input = glob.glob(main.get_save_dir() + 'best/' + 'scores*_best') #obtain all dates to merge
merge_output = 'output.txt' #output file name

for i in range(len(merge_input)):
    merge_input[i] = merge_input[i].split('/')[-1]

merge_input.append('output.txt') #if you want to merge with output.txt

f = [0]*len(merge_input)
content = [0]*len(merge_input)

def merge(content1, content2):
    merged_file = content1 + content2
    merged_list = [[0 for x in xrange(3)] for x in xrange(len(merged_file))] 
    for i in range(len(merged_file)):
        merged_list[i][0] = int(merged_file[i].split(' / ')[0]) #extracting date info
        merged_list[i][1] = ast.literal_eval(merged_file[i].split(' / ')[1]) #extracting parameter info
        merged_list[i][2] = float(merged_file[i].split(' / ')[2]) #extracting scores info
   
    merged_list.sort(key=lambda x: (x[0] , x[1]))

    temp = {}

    for m,v,n in merged_list:
        temp[m] = v,n

    temp_file = open(main.get_save_dir() + 'best/temp_file.txt','w') 
    temp_file = open(main.get_save_dir() + 'best/temp_file.txt','a') 
    
    for m in sorted(temp.iterkeys()):
        temp_file.write(str(m)+' / '+str(temp[m][0])+' / '+str(temp[m][1])+'\n')

    temp_file = open(main.get_save_dir() + 'best/temp_file.txt','r') 
    
    return temp_file.readlines()


"""def combine(file1, file2, first_date1, first_date2, last_date1, last_date2):
    if max(first_date1, first_date2) < min(last_date1, last_date2):
        merge(file1, file2)

    merge(content[0], content[0])"""



for i in range(len(merge_input)):
    f[i] = open(main.get_save_dir() + 'best/' + str(merge_input[i]),'r')
    content[i] = f[i].readlines()

for i in range(len(merge_input)-1):
    output_content = merge(content[i], content[i+1])
    content[i+1] = output_content

g = open(main.get_save_dir() + 'best/' + merge_output,'w') 
g = open(main.get_save_dir() + 'best/' + merge_output,'a') 

output_file = [[0 for x in xrange(3)] for x in xrange(len(output_content))] 

for i in range(len(output_file)):
    output_file[i][0] = output_content[i].split(' / ')[0] #extracting date string
    output_file[i][1] = ast.literal_eval(output_content[i].split(' / ')[1]) #extracting parameter info
    output_file[i][2] = output_content[i].split(' / ')[2] #extracting scores string
    g.write(output_file[i][0] + ' / ' + str(output_file[i][1]) + ' / ' + output_file[i][2])

g.close() 
