import PyPDF2
import os
import random
import config as cf


def escolher_arquivo_pdf_aleatorio(diretorio):
    # Lista todos os arquivos no diretório
    arquivos = os.listdir(diretorio)

    # Filtra apenas os arquivos que são PDFs
    pdfs = [arquivo_inner for arquivo_inner in arquivos if arquivo_inner.endswith('.pdf')]

    # Seleciona um arquivo PDF aleatoriamente
    arquivo_selecionado = random.choice(pdfs) if pdfs else None

    # Retorna o caminho completo do arquivo selecionado ou None se não houver PDFs
    return os.path.join(diretorio, arquivo_selecionado) if arquivo_selecionado else None


arquivo_escolhido = escolher_arquivo_pdf_aleatorio(cf.DIR_PDF)
if arquivo_escolhido:
    print("Arquivo PDF escolhido:", arquivo_escolhido)
else:
    print("Nenhum arquivo PDF encontrado no diretório.")
    exit(0)

nome = os.path.split(arquivo_escolhido)
nome_arquivo, _ = os.path.splitext(nome[1])

with open(arquivo_escolhido, 'rb') as arquivo:
    leitor_pdf = PyPDF2.PdfReader(arquivo)

    seq = 1
    print(f'Páginas do arquivo: {len(leitor_pdf.pages)}')

    for pagina in leitor_pdf.pages:
        texto = pagina.extract_text()
        f = open(os.path.join(cf.DIR_TXT, nome_arquivo + '-' + str(seq) + '.txt'), 'w')
        f.write(texto)
        f.close()
        seq += 1
