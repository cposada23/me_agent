class TextExtractor:
    @staticmethod
    def extract_from_pdf(pdf_path: str) -> str:
        """
        Extracts text from a PDF file.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            str: The extracted text.
        """
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            raise ImportError("PyPDF2 is required to extract text from PDF files. Please install it with 'pip install PyPDF2'.")

        text = ""
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF: {e}")
        return text

    @staticmethod
    def extract_from_txt(txt_path: str) -> str:
        """
        Extracts text from a TXT file.

        Args:
            txt_path (str): The path to the TXT file.

        Returns:
            str: The extracted text.
        """
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from TXT file: {e}")
