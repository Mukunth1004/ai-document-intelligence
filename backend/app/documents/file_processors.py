import PyPDF2
import docx
import tiktoken


class PDFProcessor:
    @staticmethod
    def extract_text(file_path: str) -> str:
        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text


class DOCXProcessor:
    @staticmethod
    def extract_text(file_path: str) -> str:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text


class TXTProcessor:
    @staticmethod
    def extract_text(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()


class MarkdownProcessor:
    @staticmethod
    def extract_text(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()


class FileProcessor:
    processors = {
        "pdf": PDFProcessor,
        "docx": DOCXProcessor,
        "txt": TXTProcessor,
        "md": MarkdownProcessor,
    }

    @staticmethod
    def extract_text(file_path: str, file_type: str) -> str:
        processor_class = FileProcessor.processors.get(file_type.lower())
        if not processor_class:
            raise ValueError(f"Unsupported file type: {file_type}")
        return processor_class.extract_text(file_path)

    @staticmethod
    def count_tokens(text: str) -> int:
        try:
            encoding = tiktoken.get_encoding("cl100k_base")
            tokens = encoding.encode(text)
            return len(tokens)
        except:
            return len(text.split())
