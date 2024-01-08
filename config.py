from dotenv import load_dotenv
import os

load_dotenv()

DIR_JSON = os.getenv('DIR_JSON')
NAME_JSON = os.getenv('NAME_JSON')

# Carrega diretórios de testes
DIR_PDF = os.getenv('DIR_PDF')
DIR_PDF_MARCADOS = os.getenv('DIR_PDF_MARCADOS')
DIR_TXT = os.getenv('DIR_TXT')