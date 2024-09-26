#!/usr/local/bin/python3

# Version 3.0

import os
import sys
import click

os.system('sudo rm -r /Users/admin/Desktop/For\ TV/Test')

def write_dat(name,BOOL):
	dat = open("/Users/admin/Documents/Scripts/Automation/HEVCConverter/"+name+".dat", "w")
	n = dat.write(str(BOOL).upper())
	dat.close()

def read_dat(name):

	with open("/Users/admin/Documents/Scripts/Automation/HEVCConverter/shutdown.dat", "r") as file:
		for line in file:
			text = line.split('.')[0]
		if text == "TRUE":
			return True
		elif text == "FALSE":
			return False
		else:
			click.secho('''Error: read_dat() couldn't read dat file''',fg='red')


@click.command()
@click.option('-s','--shutdown',is_flag=True, default=False,help="shutsdown computer when finished", required=False)
@click.option('-t','--terminate',is_flag=True, default=False,help="terminates after next conversion",required=False)
@click.option('-d','--destination',default='''/Users/admin/Desktop/For TV/''',required=False)
@click.argument('source',default=None, required=False)

def hevc(source, destination, shutdown, terminate):
	if not source:
		if shutdown:
			write_dat("shutdown",True)
			click.secho('Computer will shutdown when complete',fg='green')
		elif terminate:
			write_dat("terminate",True)
			click.secho('Program will terminate after next conversion',fg='green')
		else:
			click.secho('Error: Insuficient arguments. Use hevc --help for list of options.',fg='red')
	else:
		# try:
		# Write data files
		write_dat("shutdown",shutdown)
		write_dat("terminate",terminate)

		os.chdir(source)

		videoExtensions = ['.mp4','.mov','.mkv','.avi','.webm']

		# Get relevent files by extension

		videos = [i for i in os.listdir(source) if os.path.splitext(i)[1].lower() in videoExtensions]
		print(videos)

		if len(videos) == 0:
			click.secho('Error: No videos found in directory',fg='red')
			quit()

		# Create folder in For TV
		os.mkdir("/Users/admin/Desktop/For TV/"+os.path.basename(source))

		# Convert them
		for i in videos:
			print('--------------------')
			print(i)
			print('--------------------')
			os.system('ffmpeg -i {} -map 0 -c:v libx264 -crf 18 -vf format=yuv420p -c:a copy -c:s copy {}'.format(i,destination+"/"+os.path.basename(source)+"/"+i))

			if read_dat("terminate"):
				quit()

		if read_dat("shutdown"):
			os.system('sudo shutdown -h now')

		# except OSError as e:
		# 	if e.errno == 2:
		# 		click.secho('Error: No such file or directory',fg='red')
		# 		quit()

		# 	elif e.errno == 17:
		# 		click.secho('Error: folder already exists',fg='red')
		# 		quit()
		# 	else:
		# 		click.secho('Unexpected error with errno: '+e.errno,fg='red')


if __name__ == "__main__":
	hevc()
