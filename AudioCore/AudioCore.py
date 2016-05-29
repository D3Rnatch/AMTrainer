
import pyaudio
import sys
import time
import wave

#	class audio_core : class to handle the reading from input audio chan.
#		TO BE USED ONLY FOR ACOUSTIQ TRAINING.
class audio_core :

	def __init__(self, filename = "") :
		# this constructor inits
		self.p = pyaudio.PyAudio()	  # instanciate the pyaudio module
		if filename != "" :		  # if wave file given in entry
			self.filename = filename
		else :
			self.filename = "record.raw"
		self.CHUNK = 1024
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 2
		self.RATE = 44100
		self.stream_data = []
		self.alreadyStreaming = False

	def setFilename(self, filename) :
		self.filename = filename
		
	def startStreaming(self) :
		try :
			if self.alreadyStreaming == False :
				self.stream = self.p.open(format = self.FORMAT,
            	    	channels = self.CHANNELS,
            	    	rate = self.RATE,
            	    	input=True,
            	    	frames_per_buffer=self.CHUNK)
				self.alreadyStreaming = True
			else :
				data = self.stream.read(self.CHUNK)
				self.stream_data.append(data)
		except Exception, e :
			print e
	
	def stopStreaming(self) :
		if self.stream.is_active():
			# dump to file :
			print "AudioCore : dumping to file " + self.filename
			waveFile = wave.open(self.filename, 'wb')
			waveFile.setnchannels(self.CHANNELS)
			waveFile.setsampwidth(self.p.get_sample_size(self.FORMAT))
			waveFile.setframerate(self.RATE)
			waveFile.writeframes(b''.join(self.stream_data))
			waveFile.close()
			print ".... Finished !"
			
			self.stream_data[:] = []
			
			self.alreadyStreaming = False
			self.stream.stop_stream()
			self.stream.close()
		
		
		
		
