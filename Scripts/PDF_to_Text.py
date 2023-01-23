# importing required modules
import PyPDF2

# creating a pdf file object
pdfFileObj = open('American Sign Language For Dummies.pdf', 'rb')
   
# creating a pdf reader object
pdfReader = PyPDF2.PdfReader(pdfFileObj)

# printing number of pages in pdf file
numOfPages = len(pdfReader.pages)
print(numOfPages)

# write the text to a file
with open('ASL.txt', 'w') as f:
    for i in range(numOfPages):
        pageObj = pdfReader.pages[i]
        f.write(pageObj.extract_text())

# closing the pdf file object
pdfFileObj.close()