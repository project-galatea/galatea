
import os
import numpy as np
class Dataset():
	def __init__(self, logger):
		self._logger = logger

		self._logger.info("Dataset init.")

	def get_csvs(self,path):
		content_list = []
		for content in os.listdir(path): # "." means current directory
			if content.endswith(".csv"):
				content_list.append(path+content)
		return content_list

	def load_csv(self,path):
		with open(path) as g:
			stuff=g.readlines()
		lines=[line[:-1] for line in stuff[1:]]#cut off the \n at the end of each one, and also cut off the first line which is a csv header
		return [self.parseline(line) for line in lines]

	def parseline(self,line):
		splitted=line.split(",")
		usernameandtime=splitted[-2:]
		username=splitted[-1]
		date=splitted[-2]
		otherstuff=",".join(splitted[:-2])#there might have been commas in the first part, so put those back
		otherstuff=otherstuff[1:-1].lower()
		return {'Msg': otherstuff, 'User':username, 'Date':date}

	def converttosamples(self,lines):
		return [self.sample(line) for line in lines]

	def indexfromchar(self,char):
		if(char==' '):
			return 1
		o=ord(char)
		if(o>=ord('a') and o<=ord('z')):
			return o-ord('a')+3
		return 2

	def sample(self,line):
		max_chars_per_msg=10
		temp=np.zeros((max_chars_per_msg+1,29),dtype="bool")
		for i in range(max_chars_per_msg):
			if(i<len(line['Msg'])):
				temp[i][self.indexfromchar(line['Msg'][i])]=1
		if(len(line['Msg'])>max_chars_per_msg):
			temp[max_chars_per_msg][0]=1
		else:
			temp[len(line['Msg'])-1][0]=1
		return temp

	def load_csvs_from_folder(self,path):
		csvs = self.get_csvs(path)
		num_msgs_to_concat = 2 #TODO move these to config
		max_chars_per_msg = 10
		X = np.zeros((0,(max_chars_per_msg+1)*num_msgs_to_concat,29), dtype="bool")
		Y = np.zeros((0,max_chars_per_msg+1,29), dtype="bool")

		for csv in csvs:
			lines = self.load_csv(csv)
			samples = self.converttosamples(lines)
			for i in range(0,len(samples)-num_msgs_to_concat-1,1):
				concatted = np.zeros((0, 29),dtype="bool")
				for j in range(i,i+num_msgs_to_concat,1):
					concatted = np.concatenate([concatted,samples[j]])
				X = np.append(X,concatted)
				Y = np.append(Y,samples[i+num_msgs_to_concat])

		self._logger.debug(str(X[0]))
		self._logger.debug(str(Y[0]))

if __name__=="__main__":
	d = Dataset()
	d.load_csvs_from_folder(process.argv[1])