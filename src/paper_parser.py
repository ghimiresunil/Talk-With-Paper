import os
import re
import fitz
import arxiv
import sys

sys.path.append(os.getcwd())
import warnings

warnings.filterwarnings("ignore")
from config import setting as cfg


def clean_text(text, dolower):
    """Accepts the plain text and makes use of regex for cleaning the noise.

    Args:
        text (_type_): str
                    plain text
        dolower (_type_): Boolean
                    Boolean value for text uppercase or lowercase
    Returns: cleaned text
        _type_: str
    """
    if dolower == True:
        text = text.lower()

    text = [i.strip() for i in text.splitlines()]
    text = "\n".join(text)

    for old, new in cfg.cleantext_replacements:
        text = re.sub(old, new, text)

    text = text.encode("ascii", errors="ignore").decode("utf-8")
    regex = re.compile(r"\b(a|an|the)\b", re.UNICODE)
    text = re.sub(regex, " ", text)
    return text


def pdf_to_text(file_path, dolower):
    """Takes filepath and extracts the plain text from pdf
    Args:
        file_path (_type_): str
                        filepath with .pdf extension
        dolower (_type_): boolean
                        boolean value for text uppercase or lowercase
    Returns: cleaned text
        _type_: str
    """
    doc = fitz.open(file_path)
    number_of_pages = doc.page_count
    text = ""
    for i in range(0, number_of_pages):
        page = doc.load_page(i)
        pagetext = page.get_text("text", sort=True, flags=16)
        text += pagetext
    text = clean_text(text, dolower)
    text = " ".join(text.split())
    return text


def check_folders():
    """
    This function checks if the required directories 'data' and 'data/pdf' exist. 
    If they do not exist, the function creates them.
    
    Returns:
        None
    """
    paths = {"data_path": "data", "image_path": "data/pdf"}

    notExist = list(
        (
            {
                file_type: path
                for (file_type, path) in paths.items()
                if not os.path.exists(path)
            }
        ).values()
    )
    if notExist:
        print(f"Folder {notExist} does not exist. We will created")
        for folder in notExist:
            os.makedirs(folder, exist_ok=True)
            print(f"The new directory {folder} is created!")


def download_arxiv(url):
    """
    This function takes in a URL pointing to an arXiv paper and downloads the corresponding PDF to the 'data/pdf' directory.
    Before downloading the paper, the function calls `check_folders` to ensure that the necessary directories exist.
    
    Args:
        url (str): The URL of the arXiv paper to be downloaded
        
    Returns:
        None
    """

    check_folders()
    id_from_url = [url.split("/")[-1]]
    paper = next(arxiv.Search(id_list=id_from_url).results())
    paper.download_pdf(dirpath="data/pdf/", filename=f"{paper.title}.pdf")


""" <----------- Testing ------------->"""
if __name__ == "__main__":
    # parse_pdf = pdf_to_text(
    #     "/home/fm-pc-lt-227/Downloads/ieee_embedding.pdf", dolower=False
    # )
    download_arxiv("https://arxiv.org/abs/2003.01200")
