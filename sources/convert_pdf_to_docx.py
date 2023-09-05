print("####### Convert PDF to docx using Python #######")

from pdf2docx import Converter

pdf_file = '../resources/sample.pdf'
docx_file = '../output/test.docx'
cv = Converter(pdf_file)
cv.convert(docx_file)
cv.close()
