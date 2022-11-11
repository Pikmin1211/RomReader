class gba_rom:
	def __init__(this, filename):
		this.rom = open(filename, 'rb')

	def read_bytes(this, address, length):
		address_pop = this.rom.tell()
		this.rom.seek(address)
		data = this.rom.read(length)
		this.rom.seek(address_pop)
		return data

	def read_pointer(this, address):
		return dereference(this.read_bytes(address, 4))

	def read_text_pointer(this, address):
		if antihuffman_dereference(this.read_bytes(address, 4)) > 0:
			return antihuffman_dereference(this.read_bytes(address, 4)), True
		return dereference(this.read_bytes(address, 4)), False

def dereference(data):
	return int.from_bytes(data, byteorder='little') - 0x8000000

def antihuffman_dereference(data):
	return int.from_bytes(data, byteorder='little') - 0x88000000
