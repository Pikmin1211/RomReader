from GbafeLib.Gba_Rom import *
from GbafeLib.Text    import *
from GbafeLib.Icon    import *

from pathlib import Path

item_table_pointer = 0x16410
item_table_entry_length = 36

class item_table_entry:
	def __init__(self, data):
		self.name_text_id = int.from_bytes(data[0x00:0x02], byteorder='little')
		self.icon_index   = int.from_bytes(data[0x1D:0x1E], byteorder='little')

def make_item_entry_from_id(rom, itemid):
	item_table_address = rom.read_pointer(item_table_pointer)
	item_entry_address = item_table_address + itemid * item_table_entry_length
	return item_table_entry(rom.read_bytes(item_entry_address, item_table_entry_length))

def export_item_icon_from_item_id(rom, itemid, out_dir=''):
	this_item = make_item_entry_from_id(rom, itemid)
	if this_item.icon_index != 0:
		item_icon_filename = decode_text(rom, this_item.name_text_id)
		if item_icon_filename != '':
			item_icon_filename += '_ItemIcon.png'
		else:
			item_icon_filename = 'Item_' + hex(itemid) + '_ItemIcon.png'
		if out_dir != '':
			Path(out_dir).mkdir(parents=True, exist_ok=True)
			item_icon_filename = out_dir + '/' + item_icon_filename
		export_item_icon(rom, this_item.icon_index, item_icon_filename)