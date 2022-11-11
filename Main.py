from GbafeLib.Gba_File import *

rom = gba_file('Bells_Of_Byelen_v1_3.gba', name='BellsOfByelen')

for i in range(1, 0xFF):
	rom.export_character_portrait(i)
