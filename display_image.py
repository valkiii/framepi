from waveshare_epd import epd7in5_V2
from PIL import Image
from wand.image import Image as WandImage
import io, traceback
import os, random
import time

def resizer(filename,w,h,img_w,img_h,vertical,folder):
	img = Image.open(folder+filename)
	#img = img.resize((w,h), Image.ANTIALIAS, box=(0,0,img_w,img_h))
	if vertical:
		img.thumbnail((360,480),Image.ANTIALIAS)
	else:
		img.thumbnail((w,h),Image.ANTIALIAS)
	img.save(folder+'resized_'+filename) 


def merger():
	from PIL import Image
	#Read the two images
	image1 = Image.open('images/elephant.jpg')
	image1.show()
	image2 = Image.open('images/ladakh.jpg')
	image2.show()
	#resize, first image
	image1 = image1.resize((426, 240))
	image1_size = image1.size
	image2_size = image2.size
	new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
	new_image.paste(image1,(0,0))
	new_image.paste(image2,(image1_size[0],0))
	new_image.save("images/merged_image.jpg","JPEG")
	new_image.show()

epd = epd7in5_V2.EPD()
epd.init()

w = epd.width
h = epd.height


files = os.listdir("Franci")
folder = "Franci/"
while True:
	random.shuffle(files)
	for filename in files:
		print(filename)
		epd.Clear()
		Image.open(folder+filename).size

		photo_w = Image.open(folder+filename).size[0]
		photo_h = Image.open(folder+filename).size[1]

		vertical = False
		if photo_w < photo_h:
			vertical = True

#if (photo_w > 800 or photo_h > 480) and vertical: 
#	resizer(filename,w,h,photo_w,photo_h)
#	pil_im = Image.open('resized_'+filename)
#	pil_im = pil_im.convert(mode='1',dither=Image.FLOYDSTEINBERG)
#	epd.display(epd.getbuffer(pil_im))

		resizer(filename,w,h,photo_w,photo_h,vertical,folder)
		photo = Image.open(folder+'resized_'+filename) 
		p_w = photo.size[0]; p_h = photo.size[1] 
		image = Image.new(mode='1', size=(w, h), color=255) 
		if vertical:
			image.paste(photo,box= ( int((w/2)-(p_w/2)),0)) 
		else:
			image.paste(photo,box= (0,0))
		epd.display(epd.getbuffer(image)) #Update display
		os.remove(folder+'resized_'+filename)
		time.sleep(30)

#print(img.size)
#s = img.size
#ratio = width/s[0]
#newimg = img.resize((int(s[0]*ratio), int(s[1]*ratio)), Image.ANTIALIAS)
#print(newimg)
#epd.display(epd.getbuffer(newimg))
