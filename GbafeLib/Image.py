import GbafeLib.Gbagfx as Gbagfx

import os
import numpy as np
from PIL import Image
import tempfile

def set_image_alpha(image):
	alpha_color = image.getpalette()[:3].copy()
	alpha_color.append(0)
	image = image.convert('RGBA')
	array = np.array(image)
	for yindex, column in enumerate(array):
		for xindex, cell in enumerate(column):
			if np.array_equal(cell[:3], alpha_color[:3]):
				array[yindex][xindex] = alpha_color
	return Image.fromarray(array)

def get_image_from_bytes(data, pal='', width=0, alpha=True):
	tempdir = tempfile.mkdtemp()
	datafile  = tempdir + '/Image.4bpp'
	with open(datafile, 'wb') as file:
		file.write(data)
	palfile = ''
	if pal != '':
		palfile   = tempdir + '/Image.pal'
		with open(palfile,  'wb') as file:
			file.write(pal )
	imagefile = tempdir + '/Image.png'
	Gbagfx.run(datafile, imagefile, palette=palfile, width=width)
	with Image.open(imagefile) as tmpimage:
		array = np.array(tmpimage)
		image = Image.fromarray(array)
		image.putpalette(tmpimage.getpalette())
	os.remove(datafile )
	os.remove(palfile  )
	os.remove(imagefile)
	os.rmdir(tempdir)
	if alpha:
		image = set_image_alpha(image)
	return image