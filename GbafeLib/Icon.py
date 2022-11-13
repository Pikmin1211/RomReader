from GbafeLib.Gba_Rom import *
from GbafeLib.Image   import *

import GbafeLib.Gbagfx as Gbagfx

item_icon_sheet_pointer = 0x36B4
item_icon_palette_pointer = 0x35D0

item_icon_size = 128
palette_size = 32

def get_icon(rom, address, palette_address, alpha=True):
	data = rom.read_bytes(address, item_icon_size)
	pal  = rom.read_bytes(palette_address, palette_size)
	return get_image_from_bytes(data, pal, 2, alpha)

def get_item_icon_from_id(rom, iconid):
	item_icon_sheet_address = rom.read_pointer(item_icon_sheet_pointer)
	item_icon_address = item_icon_sheet_address + iconid * item_icon_size
	item_icon_palette_address = rom.read_pointer(item_icon_palette_pointer)
	return get_icon(rom, item_icon_address, item_icon_palette_address)

def export_item_icon(rom, iconid, name):
	get_item_icon_from_id(rom, iconid).save(name)
