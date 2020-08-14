import os
import codecs
import base64

def htmlAddImg( f, image_file ):
	with open( image_file, "rb" ) as infile:
		data = base64.b64encode(infile.read())
		f.write(b'<img src="data:image/png;base64,' + data + b'" /><br>\n')
		
	
def imgToHtml( base_dir ):
	image_files = os.listdir(base_dir)
	html_file = base_dir + ".html"
	with open( html_file, "wb" ) as f:
		for image_file in image_files:
			image_file_path = os.path.join(base_dir,image_file)
			htmlAddImg( f, image_file_path )
			print(image_file_path )
		print( '->', html_file )
	
if __name__ == "__main__":
	base_dir = r"d:\Temp2\첩"
	sub_dirs = os.listdir(base_dir)
	for sub_dir in sub_dirs:
		sub_dir_path = os.path.join(base_dir,sub_dir)
		if os.path.isdir( sub_dir_path ):
			imgToHtml( sub_dir_path )
