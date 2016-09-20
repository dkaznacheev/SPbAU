import sys, os, hashlib

CHUNK_SIZE = 1024

def read_chunk(f):
	while True:
		data = f.read(CHUNK_SIZE)
		if not data:
			break
		yield data

def get_hexdigest(filepath):
	digest = hashlib.md5()
	with open(filepath, 'rb') as fb:
		for chunk in read_chunk(fb):
			digest.update(chunk)
	return digest.hexdigest()
				

def print_dupes(dct):
	for key, files in dct.items():
		if len(files) > 1:
			print (":".join(files))

def find_dupes(dirname):
	hashdict = {}                               
	for root, dirs, files in os.walk(dirname):
		for f in files:
			cur_path = os.path.join(root, f)
			if f.startswith('.') or f.startswith('~') or os.path.islink(cur_path):
				continue
			hd = get_hexdigest(cur_path)
			if hd not in hashdict:
				hashdict[hd] = []
			hashdict[hd].append(os.path.relpath(cur_path, dirname))
	print_dupes(hashdict)
	
def main():             	
	if len(sys.argv) < 2:
		print('No directory given')
		sys.exit(1)
	dirname = sys.argv[1]            
	find_dupes(dirname)

 
if __name__ == '__main__':
    main()		
				
