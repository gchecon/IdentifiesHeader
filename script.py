import tkinter as tk
from tkinter import filedialog, simpledialog
import PyPDF2


def extrair_texto(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        texto_total = ""
        for pagina in leitor_pdf.pages:
            texto_total += pagina.extract_text()
        return texto_total


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

    def abrir_pdf(self):
        caminho_arquivo = filedialog.askopenfilename(filetypes=[('Arquivos PDF', '*.pdf')])
        if caminho_arquivo:
            texto = extrair_texto(caminho_arquivo)
            self.texto_pdf.delete('1.0', tk.END)
            self.texto_pdf.insert('1.0', texto)

    def marcar_cabecalho(self):
        posicao_inicio = simpledialog.askstring("Posição do Cabeçalho", "Início do cabeçalho (ex: 1.0):")
        posicao_fim = simpledialog.askstring("Posição do Cabeçalho", "Fim do cabeçalho (ex: 1.10):")
        if posicao_inicio and posicao_fim:
            self.dados_cabecalhos.append({'inicio': posicao_inicio, 'fim': posicao_fim})
            print("Cabeçalho marcado:", posicao_inicio, "a", posicao_fim)

    def mostrar_coordenadas(self, event):
        posicao = self.texto_pdf.index(tk.CURRENT)
        linha, coluna = posicao.split('.')
        print(f"Posição clicada: Linha {linha}, Coluna {coluna}")
        return posicao


if __name__ == '__main__':
    app = MarcadorPDF()
    app.mainloop()
