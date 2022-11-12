import subprocess

Gbagfx_Dir = 'GbafeLib/Tools/gbagfx/gbagfx'

def run(data, image, palette='', width=0):
	args = [
		Gbagfx_Dir,
		data, image
	]
	if palette != '':
		args.append('-palette')
		args.append(palette)
	if width != 0:
		args.append('-width')
		args.append(str(width))
	subprocess.call(args)
