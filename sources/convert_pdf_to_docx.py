from pdf2docx import Converter


def pdf_convert():
    print("####### Convert PDF to docx using Python #######")

    pdf_file = "../resources/sample.pdf"
    docx_file = "../output/test.docx"
    cv = Converter(pdf_file)
    cv.convert(docx_file)
    cv.close()


if __name__ == "__main__":
    pdf_convert()
