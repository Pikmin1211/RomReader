from GbafeLib.Gba_File import *

rom = gba_file('Vision Quest v3.gba', name='VisionQuest')

'''
for i in range(1, 256):
	rom.export_character_portrait(i)

for i in range(1, 256):
	rom.export_item_icon(i)

for i in range(1, 0x82+1):
	rom.export_class_map_sprite(i)
'''

for i in range(1, 256):
	rom.print_character(i)