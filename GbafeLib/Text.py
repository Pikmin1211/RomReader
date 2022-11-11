from GbafeLib.Gba_Rom import *

huffman_tree_address = 0x15A72C
huffman_tree_root_address = 0x15D484
text_table_pointer = 0xA2A0

class huffman_node:
	def __init__(self, data):
		self.left  = int.from_bytes(data[0x00:0x02], byteorder='little')
		self.right = int.from_bytes(data[0x02:0x04], byteorder='little')

def ascii_decode(rom, address):
	data = bytearray()
	while True:
		next_byte = rom.read_bytes(address, 1)[0]
		address += 1
		if next_byte == 0:
			break
		data.append(next_byte)
	return data.decode('ascii')

# Credit Hextator, Zahlman
def huffman_decode(rom, address):
	decoded = ''
	node = huffman_node(rom.read_bytes(huffman_tree_root_address, 4))
	current_byte = rom.read_bytes(address, 1)[0]
	current_bit = 0
	next_node_index = 0
	while True:
		if node.right == 0xFFFF: # leaf node
			if node.left == 0:
				break
			node_value = node.left.to_bytes(2, byteorder='little')
			if node_value[1] == 0x1F: # garbage character
				node_value = node_value[0].to_bytes(1, byteorder='little')
			decoded += node_value.decode('ascii')
			node = huffman_node(rom.read_bytes(huffman_tree_root_address, 4))
		else:
			if current_bit == 8:
				current_bit = 0
				address += 1
				current_byte = rom.read_bytes(address, 1)[0]
			if current_byte & 1:
				next_node_index = node.right
			else:
				next_node_index = node.left
			node = huffman_node(rom.read_bytes(huffman_tree_address + (next_node_index * 4), 4))
			current_byte >>= 1 # advance 1 bit
			current_bit += 1
	return decoded

def try_decode_text(rom, textid):
	text_table_address = rom.read_pointer(text_table_pointer)
	text_entry_address, is_antihuffman = rom.read_text_pointer(text_table_address + textid * 4)
	if not is_antihuffman:
		return huffman_decode(rom, text_entry_address)
	else:
		return ascii_decode(rom, text_entry_address)

def decode_text(rom, textid):
	try:
		return try_decode_text(rom, textid)
	except UnicodeDecodeError:
		return ''
