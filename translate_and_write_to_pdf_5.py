# -*- coding: utf-8 -*-

####################################################################################
# translate_and_write_to_pdf_5.py                                                  #
# similar to translate_and_write_to_pdf_4.py but reads data from text files        #
# ** MOST RECENT AND WORKING VERSION **                                            #
####################################################################################




# Import libraries
import os,glob,subprocess
from googletrans import Translator
import codecs
import unicodedata


translator = Translator()


# Read file function
def readFile(f):
	infile = codecs.open(f, encoding='utf-8', mode='r')
	text = infile.read()
	print('text type from file:', type(text))
	return text


# Latex header
header = r'''\documentclass{article}
\usepackage{multicol}
\usepackage[margin=0.5in]{geometry}
\setlength\columnsep{60pt}
\begin{document}
'''

# Latex header, bodies, and footer are passed as strings to the Tex document
print('Header type: ', type(header))

# Function to write Latex code for 2 translated and untranslated side by side colums
def writeLine(original_t, translated_t):
	s = '\\begin{multicols}{2}\n'
	s = s + original_t + '\n\\vfill\\null\n\\columnbreak\n' + translated_t + '\n\\end{multicols}\n'
	return s

# Latex footer
footer = r'''\end{document}'''

body_paragraphs = []

print('Hello')

# Read and translate all files in folder
for filename in os.listdir('Gallic_Wars_Book_1'):

	print('Blah 1')	

	original_text = readFile('Gallic_Wars_Book_1/' + filename)

	print('original text type:', type(original_text))
	
#	# drop non-ascii characters
#	for c in original_text:
#		if c < 128:
#			#original_text = original_text.replace(c, "")
#			original_text = original_text.translate(None, c)

#	#original_text = original_text.encode('ascii',errors='ignore')
#	#s = original_text.encode('utf-8')
#	#s = s.encode('ascii', 'ignore').decode('ascii')
#	#s = original_text.decode('ascii', 'ignore')

#	#s = original_text.decode('utf-8').replace("»".decode('utf-8'), "").encode('utf-8')


	#s = ''.join(char for char in original_text if ord(char) < 128)

	print('Blah 2')

	#s = original_text.encode('utf-8')

	s = unicodedata.normalize('NFKD', original_text).encode('ascii','ignore')


	#s = original_text


	#translated_text = str(translator.translate(original_text).text)
	translated_text = str(translator.translate(s).text)
	print('Original text: ', s)
	print('Translated text:', translated_text)
	print('\n')
	body_paragraphs.append(writeLine(s, translated_text))


# Add string content to LaTex file
#content = header + b for: b in body_paragraphs + footer
content = header
for b in body_paragraphs:
	content = content + b
content = content + footer

with open('myfile_2.tex','w') as f:
	f.write(content)
commandLine = subprocess.Popen(['pdflatex', 'myfile_2.tex'])
commandLine.communicate()

# Cleanup of LaTex auto-generated files
os.unlink('myfile_2.aux')
os.unlink('myfile_2.log')
os.unkink('myfile_2.tex')






