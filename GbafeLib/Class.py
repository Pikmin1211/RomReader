from GbafeLib.Gba_Rom   import *
from GbafeLib.Text      import *
from GbafeLib.MapSprite import *

from pathlib import Path

class_table_pointer = 0x17AB8
class_table_entry_length = 84

class class_table_entry:
	def __init__(self, data):
		self.name_text_id  = int.from_bytes(data[0x00:0x02], byteorder='little')
		self.map_sprite_id = int.from_bytes(data[0x06:0x07], byteorder='little')

def make_class_entry_from_id(rom, classid):
	class_table_address = rom.read_pointer(class_table_pointer)
	class_entry_address = class_table_address + classid * class_table_entry_length
	return class_table_entry(rom.read_bytes(class_entry_address, class_table_entry_length))

def export_map_sprite_from_class_id(rom, classid, out_dir=''):
	this_class = make_class_entry_from_id(rom, classid-1)
	if this_class.map_sprite_id != 0:
		map_sprite_filename = decode_text(rom, this_class.name_text_id)
		if map_sprite_filename != '':
			map_sprite_filename += '_MapSprite.png'
		else:
			map_sprite_filename = 'Class_' + hex(classid) + '_MapSprite.png'
		if out_dir != '':
			Path(out_dir).mkdir(parents=True, exist_ok=True)
			map_sprite_filename = out_dir + '/' + map_sprite_filename
		export_map_sprite(rom, this_class.map_sprite_id, map_sprite_filename)