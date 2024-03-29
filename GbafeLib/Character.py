from GbafeLib.Gba_Rom  import *
from GbafeLib.Text     import *
from GbafeLib.Portrait import *

from pathlib import Path

character_table_pointer = 0x10108
character_table_entry_length = 52

class character_table_entry:
	def __init__(self, data):
		self.name_text_id   = int.from_bytes(data[0x00:0x02], byteorder='little')
		self.character_id   = int.from_bytes(data[0x04:0x05], byteorder='little')
		self.portrait_index = int.from_bytes(data[0x06:0x07], byteorder='little')

class character_data:
	def __init__(self, character_id, name):
		self.character_id = character_id
		self.name = name

	def __str__(self):
		return f'Character with name {self.name} and id {hex(self.character_id)}'

def make_character_entry_from_id(rom, characterid):
	character_table_address = rom.read_pointer(character_table_pointer)
	character_entry_address = character_table_address + (characterid-1) * character_table_entry_length
	return character_table_entry(rom.read_bytes(character_entry_address, character_table_entry_length))

def make_character_from_id(rom, characterid):
	character_table_entry = make_character_entry_from_id(rom, characterid)
	this_character = character_data(
		character_table_entry.character_id,
		decode_text(rom, character_table_entry.name_text_id)
	)
	return this_character

def export_portrait_from_character_id(rom, characterid, out_dir=''):
	this_character = make_character_entry_from_id(rom, characterid)
	if this_character.portrait_index != 0:
		portrait_filename = decode_text(rom, this_character.name_text_id)
		if portrait_filename != '':
			portrait_filename += '_Portrait.png'
		else:
			portrait_filename = 'Character_' + hex(characterid) + '_Portrait.png'
		if out_dir != '':
			Path(out_dir).mkdir(parents=True, exist_ok=True)
			portrait_filename = out_dir + '/' + portrait_filename
		export_portrait(rom, this_character.portrait_index, portrait_filename)