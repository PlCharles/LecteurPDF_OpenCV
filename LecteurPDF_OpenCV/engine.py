# Import libraries 
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
import getopt
import utils
from matplotlib import pyplot as plt

PDF_file = ""

archive = ""

# récupération des arguments
# argument p pour le chemin du fichier pdf
#argument a pour le nom de l'agence qui emet le document. Choix entre LoLa et FedNav
try :
    opts, args = getopt.getopt(sys.argv[1:],"p:",["pdffile="])
except getopt.GetoptError:
    print ('ImageReading.py -p <pdffile>')
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-p", "--pdffile"):
        PDF_file = arg
if len(PDF_file.strip()) == 0:
        print('ImageReading.py -p <pdffile>')
        print('Renseigner le fichier pdf`a lire')
        sys.exit()
  
''' 
Part #1 : Converting PDF to images 
'''

#pages = convert_from_path(PDF_file, 250, size=(2067,2923))

#pages = convert_from_path(PDF_file, 10000, size=(800,800*1.41))
#600 dpi
pages = convert_from_path(PDF_file, 600, size=(4961,7016))
#pages = convert_from_path(PDF_file, 600, size=(7016,4961))

#pages = convert_from_path(PDF_file, 10000, size=(800,800*1.41))
#300 dpi
#pages = convert_from_path(PDF_file, 300, size=(2480,3508))
#pages = convert_from_path(PDF_file, 300, size=(3508,2480))

#200 dpi
#pages = convert_from_path(PDF_file, 200, size=(1654,2339))
#pages = convert_from_path(PDF_file, 200, size=(2339,1654))

# Counter to store images of each page of PDF to image 
image_counter = 1
  
# Iterate through all the pages stored above 
for page in pages: 
  
    # Declaring pagename for each page of PDF as JPG 
    # For each page, pagename will be: 
    # PDF page 1 -> page_1.jpg 
    # PDF page 2 -> page_2.jpg 
    # PDF page 3 -> page_3.jpg 
    # .... 
    # PDF page n -> page_n.jpg 
    pagename = "page_"+str(image_counter)+".jpg"
      
    # Save the image of the page in system 
    page.save(pagename, 'JPEG') 
  
    # Increment the counter to update pagename 
    image_counter = image_counter + 1
  
''' 
Part #2 - Recognizing text from the images using OCR 
'''

# Variable to get count of total number of pages 
filelimit = image_counter-1
  
# Creating a text file to write the output 
if PDF_file.endswith('.pdf'):
    outfile = PDF_file.replace('.pdf','.txt')
if PDF_file.endswith('.PDF'):
    outfile = PDF_file.replace('.PDF','.txt')
if os.path.exists(outfile):
    os.remove(outfile)

# Open the file in append mode so that  
# All contents of all images are added to the same file 
f = open(outfile, "w", encoding='utf-16') 
  
  
# Iterate from 1 to total number of pages 
for i in range(1, filelimit + 1): 
  
    # Set pagename to recognize text from 
    pagename = "page_"+str(i)+".jpg"
    
    # Get page orientation
    print("----" + pagename +"----")
    image_cv = utils.get_cv_image(pagename)
    Greypage = utils.grayscale(image_cv)
    pageNameNoNoise = utils.remove_noise(Greypage)
    print(pytesseract.image_to_osd(pageNameNoNoise))
          
    # Recognize the text as string in image using pytesserct 
    text = str(((pytesseract.image_to_string(pageNameNoNoise,lang='fra')))) 
  
    # The recognized text is stored in variable text 
    # Any string processing may be applied on text 
    # Here, basic formatting has been done: 
    # In many PDFs, at line ending, if a word can't 
    # be written fully, a 'hyphen' is added. 
    # The rest of the word is written in the next line 
    # Eg: This is a sample text this word here GeeksF- 
    # orGeeks is half on first line, remaining on next. 
    # To remove this, we replace every '-\n' to ''. 
    text = text.replace('-\n', '')     
  
    # Finally, write the processed text to the file. 
    f.write(text)
    #os.remove(pagename)

# Close the file after writing all the text. 
f.close() 


