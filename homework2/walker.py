import sys, os, hashlib

def find_dupes(dirname):
	hashdict = {}
	cwd = os.path.join(os.getcwd(),dirname) 
	for root, dirs, files in os.walk(cwd):
		for f in files:
			if f.startswith('.') or f.startswith('~'):
				continue
			digest = hashlib.md5()
			with open(os.path.join(root, f), 'rb') as fb:
				buf = fb.read()
				digest.update(buf)
			hd = digest.hexdigest()
			if hd not in hashdict:
				hashdict[hd] = []
			hashdict[hd].append(os.path.join(os.path.relpath(root, cwd), f))
	for key, files in hashdict.items():
		if len(files) > 1:
			for f in files[:-1]:
				print(f + ':', end = "")
			print (files[-1])

def main():             	
	if len(sys.argv) < 2:
		print('No directory given')
		sys.exit(1)
	dirname = sys.argv[1]            
	find_dupes(dirname)

 
if __name__ == '__main__':
    main()		
				
