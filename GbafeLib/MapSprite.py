from GbafeLib.Gba_Rom          import *
from GbafeLib.Image            import *
from GbafeLib.Lz77.Lz77_Length import *
from GbafeLib.Lz77.Lzss3       import *

map_sprite_table_pointer = 0x26730
map_sprite_table_entry_length = 8

map_sprite_palette_pointer = 0xBD54
palette_size = 32

class map_sprite_table_entry:
	def __init__(self, data):
		self.map_sprite_address =    dereference(data[0x04:0x08])
		self.size               = int.from_bytes(data[0x02:0x03], byteorder='little')

def get_map_sprite(rom, address, alpha=True):
	this_map_sprite = map_sprite_table_entry(rom.read_bytes(address, map_sprite_table_entry_length))
	data_size = lz_getsize(rom.rom, this_map_sprite.map_sprite_address)
	data = decompress(rom.read_bytes(this_map_sprite.map_sprite_address, data_size))
	pal  = rom.read_bytes(rom.read_pointer(map_sprite_palette_pointer), palette_size)
	image = get_image_from_bytes(data, pal, 2 if this_map_sprite.size != 2 else 4, alpha)
	if this_map_sprite.size == 0:
		return image.crop((0,0,16,16))
	elif this_map_sprite.size == 1:
		return image.crop((0,0,16,32))
	elif this_map_sprite.size == 2:
		return image.crop((0,0,32,32))
	return image

def get_map_sprite_from_id(rom, spriteid):
	map_sprite_table_address = rom.read_pointer(map_sprite_table_pointer)
	map_sprite_entry_address = map_sprite_table_address + spriteid * map_sprite_table_entry_length
	return get_map_sprite(rom, map_sprite_entry_address)

def export_map_sprite(rom, spriteid, name):
	get_map_sprite_from_id(rom, spriteid).save(name)