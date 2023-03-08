from GbafeLib.Gba_File import *

rom = gba_file('Bells_Of_Byelen_v1_3.gba', name='BellsOfByelen')

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