import os

present = os.getcwd()
os.chdir("/home/ninjaPython/Work/learn/udn004/practicals/assignments/alphabet/demo")
for i in os.listdir(os.getcwd()):
	print(os.getcwd())
	m=""
	for x in i:
		if not x.isdigit():
			m+=x
	print("Old File:"+i)
	print("New File:"+m)
	os.rename(i,m)
