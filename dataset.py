
import os
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
		return {'Msg': otherstuff[1:-1], 'User':username, 'Date':date}
	def __init__(self):
		path="/Users/leijurv/Downloads/dank/"
		csvs=self.get_csvs(path)
		alllines=[]
		for csv in csvs:
			alllines.extend(self.load_csv(csv))
		print len(alllines)
		print alllines[0]
		print alllines[-1]
		
Dataset()