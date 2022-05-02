import numpy as np
import cv2
import math as mt
import sys, tty, termios, os

zeilen = 700
spalten = 1000

bild = np.zeros((zeilen, spalten, 3), dtype=np.uint8)

filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)

def build_kosy():
	for x in range(spalten):
		y = round(zeilen/2)
		try:
			bild[y][x-1] = [255,255,255]
		except IndexError:
			continue
	for y in range(zeilen):
		try:
			bild[y][round(spalten/2)] = [255,255,255]
		except IndexError:
			continue			
	return

def plot(dim=(480, 640), zoom=1, perioden=6, amplitude=100, color=[255,0,0], exp=False):
	rows = dim[0]
	cols = dim[1]
	amp = amplitude
	per = perioden
	for x in range(cols):
		xind = x
		x = x - round(cols/2)
		
		
		if exp:
			perioden /= zoom
			amplitude *= zoom
		else:
			perioden = per / zoom
			amplitude = amp *zoom
		#y =  rows - round(amplitude * (1 / (1+ 2.7 **(-0.1*x))) + 0.5 * rows) #Sigmoid
		#y = rows - round(amplitude*mt.sin(perioden*x* 2 * mt.pi/cols) + 0.5 * rows) #Sinus
		#y = rows-(round(a * x + m))%rows #Lineare Funktion ax+m
		#y = rows-round(b**x + 0.5*rows) #Exponentialfunktion
		y = rows-round(amplitude*mt.tan(perioden*x*2*mt.pi/cols)+0.5*rows)
		try:
			bild[y-2][xind-1] = color
		except IndexError:
			continue
		try:
			bild[y-1][xind-1] = color
		except IndexError:
			continue
		try:
			bild[y][xind-1] = color
		except IndexError:
			continue
		try:
			bild[y+1][xind-1] = color
		except IndexError:
			continue
		try:
			True
			bild[y+2][xind-1] = color
		except IndexError:
			continue
def user_scaling(perioden, amplitude, zoom, a, m, changer, exp):
		# aplitude +- with w,s respectively
		# periodes +- with d,a respectively
		# zoom +- with z,t respectively
		# a +- with g,f respectively
		# m +- with m,n respectively
		# changer +- with v,c respectively
		# e to change exponentiated-state
		# i for info
		# q to exit
		inp = sys.stdin.read(1)[0]
		if inp == 'q':
			exit()
		if inp == 'w':
			amplitude += changer
		elif inp == 's':
			amplitude = max([amplitude - changer, 0.01])
		elif inp == 'd':
			perioden += changer* 0.001
		elif inp == 'a':
			perioden -= changer* 0.001
		elif inp == 'z':
			zoom += changer * 0.001
		elif inp == 't':
			zoom -= changer*0.001
		elif inp == 'g':
			a += changer*0.001
		elif inp == 'f':
			a -= changer*0.001
		elif inp == 'm':
			m += changer*0.001
		elif inp == 'n':
			m -= changer*0.001
		elif inp == 'v':
			changer += changer
		elif inp == 'c':
			if changer < 1:
				changer = 1
			else:
				changer -= int(changer/2)
		elif inp == 'e':
			exp = not exp
		elif inp == 'r':
			a = 1
			m = 0
			zoom = 1
			perioden =  6
			amplitude = 100
			changer = 64
			color = [0,255,0]
			exp = False
			b = 1.015
		elif inp == 'i':
			info = 60*"-" +"\n\t\t\tInfo\n"+ 60*"-"+"\n\namplitude +,- with w,s respectively\nperiodes +,- with d,a respectively\nzoom +,- with z,t respectively\na +,- with g,f respectively\nm +,- with m,n respectively\nscalar +,- with v,c respectively\ne to change exponentiated-state\ni for info\nq to quit program\n\n" + 60*"-"
			os.system('clear')
			print(info)
			input("\nPress ENTER to continue!")
			os.system('clear')
		return (perioden, amplitude, zoom, a, m, changer, exp)


a = 1
m = 0
zoom = 1
perioden =  6
amplitude = 100
changer = 64
color = [0,255,0]
exp = False
b = 1.015
while True:
	bild = np.zeros((zeilen, spalten, 3), dtype=np.uint8)
	build_kosy()
	plot(dim=(zeilen, spalten), zoom=zoom, perioden=perioden, amplitude=amplitude, color=color, exp=exp)
	cv2.imshow("Plot", bild)
	#amplitude = int(abs(np.random.normal(loc = 100, scale = 10)))
	#perioden = np.random.normal(loc = 6, scale = 2)
	cv2.waitKey(10)
	perioden, amplitude, zoom, a, m, changer, exp = user_scaling(perioden, amplitude, zoom, a, m, changer, exp)
	cv2.imshow("Plot", bild)
	os.system('clear')
	print(60*"-" +"\n\t\t\tStats\n"+ 60*"-"+f"\n\namplitude:{amplitude}\n#periods:{perioden}\nzoom:{zoom}\n\nscalar:{changer}\nexponentiated:{exp}\n\n" + 60*"-")

