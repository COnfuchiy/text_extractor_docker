import pdfplumber
from pdf2image import convert_from_path
from pytesseract import pytesseract


class PDFTextExtractor:

    def __init__(self, pdf_path):
        self.pages_texts = []
        self.pdf_path = pdf_path

    def extract(self):
        self.pages_texts = self._extract_text_from_pdf()
        if not self.pages_texts:
            return self._scanned_pdf_to_text()
        return ' '.join(self.pages_texts)

    def _extract_text_from_pdf(self):
        pages_texts = []
        with pdfplumber.open(self.pdf_path) as pdf:
            pages_without_text = 0
            total_page_count = len(pdf.pages)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text == '':
                    pages_without_text += 1
                pages_texts.append(page.extract_text())
        if pages_without_text > total_page_count / 2:
            return []
        return pages_texts

    def _scanned_pdf_to_text(self):
        pdf_pages_as_image = convert_from_path(self.pdf_path, 300)
        pages_texts = []
        for page in pdf_pages_as_image:
            pages_texts.append(pytesseract.image_to_string(page, 'rus'))
        return ' '.join(pages_texts)
