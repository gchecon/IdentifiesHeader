import os
import json

def converter_para_label_studio(diretorio_origem, diretorio_destino, nome_arquivo_saida):
    """
    Lê todos os arquivos .txt no diretório de origem e os converte em um formato aceito pelo Label Studio.
    Salva o resultado em um arquivo JSON no diretório de destino.

    :param diretorio_origem: Diretório onde os arquivos .txt estão localizados.
    :param diretorio_destino: Diretório onde o arquivo JSON de saída será salvo.
    :param nome_arquivo_saida: Nome do arquivo JSON de saída.
    """

    # Cria uma lista para armazenar as tarefas formatadas
    tarefas = []

    # Lista todos os arquivos no diretório de origem
    for arquivo in os.listdir(diretorio_origem):
        if arquivo.endswith('.txt'):
            caminho_arquivo = os.path.join(diretorio_origem, arquivo)

            # Adiciona cada arquivo .txt como uma tarefa no formato do Label Studio
            tarefas.append({
                'data': {
                    'document': caminho_arquivo
                }
            })

    # Cria o diretório de destino se ele não existir
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)

    # Caminho do arquivo de saída
    caminho_saida = os.path.join(diretorio_destino, nome_arquivo_saida)

    # Escreve as tarefas no arquivo JSON de saída
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
        json.dump(tarefas, arquivo_saida, indent=4, ensure_ascii=False)

# Exemplo de uso da função
# converter_para_label_studio('/caminho/para/diretorio/origem', '/caminho/para/diretorio/destino', 'tarefas_label_studio.json')

# Nota: Atualize os caminhos conforme necessário e descomente a linha acima para executar a função.
