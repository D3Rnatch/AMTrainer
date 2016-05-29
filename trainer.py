

import sys, os, time
sys.path.insert(0, 'AudioCore/')
from AudioCore import *

string_to_be_read = []
max_value = 0
RECORD_TIME = 8
trainerFile = "config\sentences"
output_file_pattern = ""

def dumpData(f1,f2,ind,str,fileid) :
	global output_file_pattern
	
	# dump data to file
	# f2.write(fileid)
	# dts = output_file_pattern + "%d"%ind
	# dt = "<s> "+str+" </s> ("+dts+")"
	# f1.write(dt)
	
	dts = output_file_pattern + "%d"%ind
	f2.write(dts + "\n")
	dt = "<s> " + str + " </s> (" + dts + ")\n"
	f1.write(dt)
	

def loadString() :
	global max_value
	global string_to_be_read
	
	file = open(trainerFile, 'r')

	data = file.readline()
	while data != "" :
		string_to_be_read.append(data)
		data = file.readline()
		max_value = max_value + 1
		
	for i in range(0,len(string_to_be_read)) :
		print string_to_be_read[i] + "\n"
	
def usage() :
	print "Usage for script is : "
	print " filename"

if __name__ == "__main__" :
	if len(sys.argv) < 2 :
		usage()
		exit()
	output_file_pattern = sys.argv[1]
	index = 0
	root = "data\\"
	#output_file_pattern = output_file_pattern + "%d.wav" % index
	print output_file_pattern
	
	print "================= starting the recording ======================\n"
	end = False
	
	# loading sentences
	loadString()
	
	Audio = audio_core("")
	
	transcript_file = open("config\\dernacth.transcription","wb")
	ids_file = open("config\\dernacth.fileids","wb")
	
	while end == False :
		temp = output_file_pattern + "%d.wav" % index
		outputfile = root + temp
		print "current text file " + outputfile
		print "Please read this sentence at top : \n======================================"
		print string_to_be_read[index]
		Audio.setFilename(outputfile)
		Audio.startStreaming()
		print "TOP"
		
		for i in range (0,int(Audio.RATE / Audio.CHUNK * RECORD_TIME)) :
			Audio.startStreaming()
		
		Audio.stopStreaming()
		
		dumpData(transcript_file,ids_file,index,string_to_be_read[index],temp)
		
		print "======= END OF RECORD =========\n\n\n\n\n\n\n"
		
		index = index + 1
		
		if index == max_value :
			end = True
			
	transcript_file.close()
	ids_file.close()
	