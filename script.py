import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox

import PyPDF2

import config as cf


def extrair_texto(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        texto_total = ""
        for pagina in leitor_pdf.pages:
            texto_total += pagina.extract_text()
        return texto_total


def carregar_dados_json():
    if not os.path.exists(cf.DIR_JSON):
        os.makedirs(cf.DIR_JSON)
    arquivo_json = os.path.join(cf.DIR_JSON, cf.NAME_JSON)
    if os.path.exists(arquivo_json):
        with open(arquivo_json, 'r', encoding='utf-8') as arquivo:
            try:
                return json.load(arquivo)
            except json.JSONDecodeError:
                return []  # Retornar uma lista vazia se o arquivo estiver vazio ou corrompido
    return []


class MarcadorPDF(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Marcador de Cabeçalhos de PDF')
        self.geometry('600x400')

        self.texto_pdf = tk.Text(self, wrap='word')
        self.texto_pdf.pack(padx=10, pady=10, expand=True, fill='both')
        self.texto_pdf.bind("<Button-1>", self.mostrar_coordenadas)

        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Arquivo', menu=self.file_menu)
        self.file_menu.add_command(label='Abrir PDF...', command=self.abrir_pdf)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Sair', command=self.quit)

        self.dados_cabecalhos = []
        self.dados_existentes = carregar_dados_json()
        self.posicao_inicio_cabecalho = None

        self.dados_existentes = carregar_dados_json()
        self.dados_cabecalhos = []  # Lista para armazenar os dados atuais do documento aberto

    def abrir_pdf(self):

        caminho_arquivo = filedialog.askopenfilename(filetypes=[('Arquivos PDF', '*.pdf')])
        if caminho_arquivo:
            self.ao_abrir_novo_pdf()
            texto = extrair_texto(caminho_arquivo)
            self.texto_pdf.delete('1.0', tk.END)
            self.texto_pdf.insert('1.0', texto)

    def marcar_cabecalho(self, inicio, fim):
        self.dados_cabecalhos.append({'inicio': inicio, 'fim': fim})
        print(f"Cabeçalho marcado: {inicio} a {fim}")

    def mostrar_coordenadas(self, event):
        posicao_atual = self.texto_pdf.index(tk.CURRENT)
        # Se a posição de início ainda não foi definida, defina-a
        if not self.posicao_inicio_cabecalho:
            self.posicao_inicio_cabecalho = posicao_atual
            print(f"Posição de início do cabeçalho definida: {posicao_atual}")
        else:
            # Se a posição de início já foi definida, defina a posição de fim e marque o cabeçalho
            self.marcar_cabecalho(self.posicao_inicio_cabecalho, posicao_atual)
            self.posicao_inicio_cabecalho = None  # Resetar para o próximo cabeçalho

    def salvar_em_json(self):
        novo_registro = {
            'texto': self.texto_pdf.get("1.0", tk.END),
            'cabecalhos': self.dados_cabecalhos
        }
        self.dados_existentes.append(novo_registro)

    def ao_abrir_novo_pdf(self):
        if self.dados_cabecalhos:
            self.salvar_em_json()
        self.dados_cabecalhos = []  # Reiniciar a lista para o novo documento

    def ao_sair(self):
        self.salvar_em_json()
        arquivo_json = os.path.join(cf.DIR_JSON, cf.NAME_JSON)
        with open(arquivo_json, 'w', encoding='utf-8') as arquivo:
            json.dump(self.dados_existentes, arquivo, indent=4, ensure_ascii=False)
        print(f"Dados salvos em '{arquivo_json}'")
        self.quit()

    def quit(self):
        if messagebox.askokcancel("Sair", "Deseja sair e salvar os dados atuais?"):
            self.ao_sair()


if __name__ == '__main__':
    app = MarcadorPDF()
    app.mainloop()
