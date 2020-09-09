# Springer Ebooks Downloader

# Author: Oriol Ordi

# This script automates the download of the Ebooks that were made free and
# publicly available during the coronavirus

# NOTE: the pdf containing the list of the books must be in the same folder
# as this script (or the pdf_path in the script must be changed)


import PyPDF2
import urllib.request
import requests


# Set pdf path
pdf_path = 'Springer Ebooks.pdf'


# Function to process the pdf and get a list of text from it
def process_pdf(pdf_file):
    # Read the pdf from the file
    read_pdf = PyPDF2.PdfFileReader(pdf_file)

    # Get the number of pages from the pdf
    number_of_pages = read_pdf.getNumPages()

    # Read all the pages
    pages = []
    for page_number in range(number_of_pages):
        pages.append(read_pdf.getPage(page_number))

    # Extract text from the pages
    text = []
    for page in pages:
        text.append(page.extractText())

    # Split the text at every line skip (at every '\n')
    text_split = []
    for t in text:
        text_split.append(t.split('\n'))

    # Convert the list of lists into a single list (or a flat list)
    text_split_flat = []
    for list_text in text_split:
        for item in list_text:
            text_split_flat.append(item)

    # Return the text_split_flat list
    return text_split_flat


# Get pdf file
try:
    with open(pdf_path, 'rb') as pdf_file:
        text_split_flat = process_pdf(pdf_file)
except:
    print('Error: File "Springer Ebooks.pdf" not found')
    print('\n')
    input('Press enter key to quit')


# Print a message letting know that the program is starting
print('Starting to download the Springer Ebooks...')
print('Warning: The books will be saved as pdf files in the same folder that the program was launched from')
print('\n')


# Loop the list searching for each book number and saving the book name and link
book_number = 1
book_number_position = 0
book_names = []
book_links = []
for i, element in enumerate(text_split_flat):
    if element == str(book_number):
        book_number_position = i
        book_names.append(text_split_flat[i+1].replace('/', '-'))
        book_number += 1
    if element.startswith('http://'):
        book_links.append(element)


# Change the links for the download links, download the books and save them to pdf files
for i, link in enumerate(book_links):
    print('Getting download url from book number {}/{}'.format(i+1, len(book_links)))
    download_link = urllib.request.urlopen(link).geturl()
    download_link = download_link.replace('book', 'content/pdf') + '.pdf'
    print('Downloading book number {}/{}'.format(i+1, len(book_links)))
    try:
        response = requests.get(download_link, timeout=10)
        if response.status_code == 200:
            print('Saving to pdf book number {}/{}'.format(i+1, len(book_links)))
            with open(str(i+1) + '. ' + book_names[i] + '.pdf', 'wb') as f:
                f.write(response.content)
        else:
        	print('The file could not be downloaded')
    except:
    	print('The file could not be downloaded')
    print('\n')


# Print a message letting know that the script has finished
print('Finished')
print('\n')
input('Press enter key to quit')
