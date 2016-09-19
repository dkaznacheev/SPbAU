import sys, os, hashlib

def get_hexdigest(filepath):
	digest = hashlib.md5()
	with open(filepath, 'rb') as fb:
		buf = fb.read()
		digest.update(buf)
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
				
