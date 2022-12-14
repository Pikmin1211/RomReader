from GbafeLib.Gba_Rom import *
from GbafeLib.Image   import *

import GbafeLib.Gbagfx as Gbagfx

import numpy as np
from PIL import Image

portrait_table_pointer = 0x5524
portrait_table_entry_length = 28

portrait_size = 4100
palette_size  = 32

class portrait_table_entry:
	def __init__(self, data):
		self.portrait_address = dereference(data[0x00:0x04])
		self.palette_address  = dereference(data[0x08:0x0C])

def arrange_portrait_tiles(array):
	newarray = np.zeros([80, 96], dtype = np.uint8)
	newarray[  0:   8,  16:  80] = array[  0:   8,   0:  64]
	newarray[ 32:  40,  16:  80] = array[  0:   8,  64: 128]
	newarray[ 64:  72,  16:  48] = array[  0:   8, 128: 160]
	newarray[ 48:  56,   0:  16] = array[  0:   8, 160: 176]
	newarray[ 48:  56,  80:  96] = array[  0:   8, 176: 192]
	newarray[  8:  16,  16:  80] = array[  0:   8, 256: 320]
	newarray[ 40:  48,  16:  80] = array[  0:   8, 320: 384]
	newarray[ 72:  80,  16:  48] = array[  0:   8, 384: 416]
	newarray[ 56:  64,   0:  16] = array[  0:   8, 416: 432]
	newarray[ 56:  64,  80:  96] = array[  0:   8, 432: 448]
	newarray[ 16:  24,  16:  80] = array[  0:   8, 512: 576]
	newarray[ 48:  56,  16:  80] = array[  0:   8, 576: 640]
	newarray[ 64:  72,  48:  80] = array[  0:   8, 640: 672]
	newarray[ 64:  72,   0:  16] = array[  0:   8, 672: 688]
	newarray[ 64:  72,  80:  96] = array[  0:   8, 688: 704]
	newarray[ 24:  32,  16:  80] = array[  0:   8, 768: 832]
	newarray[ 56:  64,  16:  80] = array[  0:   8, 832: 896]
	newarray[ 72:  80,  48:  80] = array[  0:   8, 896: 928]
	newarray[ 72:  80,   0:  16] = array[  0:   8, 928: 944]
	newarray[ 72:  80,  80:  96] = array[  0:   8, 944: 960]
	return newarray

def arrange_portrait(image, alpha=True):
	array = np.array(image)
	array = arrange_portrait_tiles(array)
	portrait = Image.fromarray(array)
	portrait.putpalette(image.getpalette())
	if alpha:
		portrait = set_image_alpha(portrait)
	return portrait

def get_portrait(rom, address, alpha=True):
	this_portrait = portrait_table_entry(rom.read_bytes(address, portrait_table_entry_length))
	data = rom.read_bytes(this_portrait.portrait_address + 4, portrait_size)
	pal =  rom.read_bytes(this_portrait.palette_address  + 0, palette_size )
	portrait = arrange_portrait(get_image_from_bytes(data, pal, 132, False), alpha)
	return portrait

def get_portrait_from_id(rom, portraitid):
	portrait_table_address = rom.read_pointer(portrait_table_pointer)
	portrait_entry_address = portrait_table_address + portraitid * portrait_table_entry_length
	return get_portrait(rom, portrait_entry_address)

def export_portrait(rom, portraitid, name):
	get_portrait_from_id(rom, portraitid).save(name)
