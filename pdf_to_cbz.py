# Kevin Mathews 7/20/2020 rev 1.01
# PDF to CBR Converter
# written in Python 3

# Script which converts PDF files to CBZ format.
# Tested on both Linux and Windows

# manual input
# Change read_dir and write_dir to your preference.
read_dir = r'C:\Users\Documents\pdf_to_cbz\Books' # folder where your PDFs are located
write_dir = r'C:\Users\Documents\Workspace\pdf_to_cbz\Completed' # folder where completed cbz files should go

# https://realpython.com/pdf-python/
import os, sys
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path
import tempfile
import zipfile

# function to handle image conversion
def get_pdf_photos(input_path, newZip):
	def empty_folder(folder_loc):	
		for the_file in os.listdir(folder_loc):
			file_path = os.path.join(folder_loc, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
			except Exception as e:
				print(e)
				pdb.set_trace()	

	def extract_information(pdf_path):
		try:
			with open(pdf_path, 'rb') as f:
				pdf = PdfFileReader(f)
				information = pdf.getDocumentInfo()
				number_of_pages = pdf.getNumPages()
				pageObj = pdf.getPage(0)
				full_text = pageObj.extractText()
				
			txt = f"""
			Information about {pdf_path}: 

			Author: {information.author}
			Creator: {information.creator}
			Producer: {information.producer}
			Subject: {information.subject}
			Title: {information.title}
			Number of pages: {number_of_pages}
			"""
		except:
			information = '-'
			full_text = '-'
			
		return information, full_text
		
	# use tempfile for image processing
	print('\tgetting images from path...')
	with tempfile.TemporaryDirectory() as path:
		print('\t' + path)

		# use convert_from_path to create list of images
		# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
		convert_from_path(pdf_path=input_path, fmt='jpeg', output_file = '', output_folder=path)
		
		print('\tgathered images.')
		
		for picture_name in os.listdir(path):
			# save image to zip file
			newZip.write(os.path.join(path, picture_name), arcname = picture_name, compress_type=zipfile.ZIP_DEFLATED)

# function to create zip file and make cbz conversion more verbose
def convert_pdf_to_comic(input_path, output_path):

	# interperet input path
	read_dir, file_name = os.path.split(input_path)
	cb_file_name = os.path.splitext(file_name)[0]

	# create zip file at working directory
	cb_file_path = os.path.join(output_path, cb_file_name + '.cbz')
	newZip = zipfile.ZipFile(cb_file_path, 'w')
	
	print('\t' + file_name)
	get_pdf_photos(input_path, newZip)
	
	# close zip file after completion
	newZip.close()
	print('\tsaved book', cb_file_name + '.cbz')
	
if __name__ == "__main__":
	
	pdf_list = [i for i in os.listdir(read_dir) if i.endswith('.pdf') == True]
	no_of_pdfs = str(len(pdf_list))
	
	n = 1
	for read_file in pdf_list:
		
		input_path = os.path.join(read_dir, read_file)
		output_path = write_dir

		# initial checks
		assert os.path.exists(input_path) == True # check that file exists
		assert os.path.splitext(input_path)[1] == '.pdf' # check that file is pdf
		
		print('working on', n, 'of', no_of_pdfs)
		convert_pdf_to_comic(input_path, output_path)
			
	print('done.')
