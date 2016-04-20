
import os
import numpy as np
class Dataset():
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
			return 0
		o=ord(char)
		if(o>=ord('a') and o<=ord('z')):
			return o-ord('a')+2
		return 1
	def sample(self,line):
		max_chars_per_msg=10
		temp=np.zeros((max_chars_per_msg,28),dtype="bool")
		for i in range(max_chars_per_msg):
			if(i<len(line['Msg'])):
				temp[i][self.indexfromchar(line['Msg'][i])]=1
	def load_csvs_from_folder(self,path):
		csvs=self.get_csvs(path)
		for csv in csvs:
			lines=self.load_csv(csv)
			samples=self.converttosamples(lines)
			print lines[0]
			print samples[0]
	def __init__(self):
		print "INIT"

if __name__=="__main__":
	d = Dataset()
	d.load_csvs_from_folder("/Users/leijurv/Downloads/dank/")