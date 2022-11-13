from GbafeLib.Gba_Rom import *
import GbafeLib.Gbagfx as Gbagfx

import os
import numpy as np
from PIL import Image
import tempfile

item_icon_sheet_pointer = 0x36B4
item_icon_palette_pointer = 0x35D0

item_icon_size = 128
palette_size = 32

def set_icon_alpha(icon):
	alpha_color = icon.getpalette()[:3].copy()
	alpha_color.append(0)
	icon = icon.convert('RGBA')
	array = np.array(icon)
	for yindex, column in enumerate(array):
		for xindex, cell in enumerate(column):
			if np.array_equal(cell[:3], alpha_color[:3]):
				array[yindex][xindex] = alpha_color
	return Image.fromarray(array)

def get_icon(rom, address, palette_address, alpha=True):
	data = rom.read_bytes(address, item_icon_size)
	pal  = rom.read_bytes(palette_address, palette_size)
	tempdir = tempfile.mkdtemp()
	datafile  = tempdir + '/ItemIcon.4bpp'
	palfile   = tempdir + '/ItemIcon.pal'
	imagefile = tempdir + '/ItemIcon.png'
	with open(datafile, 'wb') as file:
		file.write(data)
	with open(palfile,  'wb') as file:
		file.write(pal )
	Gbagfx.run(datafile, imagefile, palette=palfile, width=2)
	with Image.open(imagefile) as image:
		array = np.array(image)
		item_icon = Image.fromarray(array)
		item_icon.putpalette(image.getpalette())
	os.remove(datafile )
	os.remove(palfile  )
	os.remove(imagefile)
	os.rmdir(tempdir)
	if alpha:
		item_icon = set_icon_alpha(item_icon)
	return item_icon

def get_item_icon_from_id(rom, iconid):
	item_icon_sheet_address = rom.read_pointer(item_icon_sheet_pointer)
	item_icon_address = item_icon_sheet_address + iconid * item_icon_size
	item_icon_palette_address = rom.read_pointer(item_icon_palette_pointer)
	return get_icon(rom, item_icon_address, item_icon_palette_address)

def export_item_icon(rom, iconid, name):
	get_item_icon_from_id(rom, iconid).save(name)
