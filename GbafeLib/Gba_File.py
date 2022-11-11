from GbafeLib.Gba_Rom   import *
from GbafeLib.Text      import *
from GbafeLib.Portrait  import *
from GbafeLib.Character import *

class gba_file:
	def __init__(this, filename, name=''):
		this.gba_rom = gba_rom(filename)
		this.name = name

	def get_text_string(this, textid):
		return decode_text(this.gba_rom, textid)

	def export_character_portrait(this, characterid, out_dir=''):
		if this.name != '':
			out_dir = this.name
		export_portrait_from_character_id(this.gba_rom, characterid, out_dir)