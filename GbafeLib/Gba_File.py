from GbafeLib.Gba_Rom   import *
from GbafeLib.Text      import *
from GbafeLib.Portrait  import *
from GbafeLib.Character import *
from GbafeLib.Class     import *
from GbafeLib.Item      import *

class gba_file:
	def __init__(this, filename, name=''):
		this.gba_rom = gba_rom(filename)
		this.name = name

	def get_text_string(this, textid):
		return decode_text(this.gba_rom, textid)

	def export_character_portrait(this, characterid, out_dir=''):
		if this.name != '' and out_dir == '':
			out_dir = this.name
		export_portrait_from_character_id(this.gba_rom, characterid, out_dir)

	def export_item_icon(this, itemid, out_dir=''):
		if this.name != '' and out_dir == '':
			out_dir = this.name
		export_item_icon_from_item_id(this.gba_rom, itemid, out_dir)

	def export_class_map_sprite(this, classid, out_dir=''):
		if this.name != '' and out_dir == '':
			out_dir = this.name
		export_map_sprite_from_class_id(this.gba_rom, classid, out_dir)

	def print_character(this, characterid):
		print(make_character_from_id(this.gba_rom, characterid))