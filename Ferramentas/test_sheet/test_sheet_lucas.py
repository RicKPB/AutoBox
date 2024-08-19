import pandas as pd
import re

df = pd.read_excel("Z:\SANTA CASA DE ASSIS\9. PLANILHAS - FAA - TRABALHAR\CONFERENCIAS FEITAS\CONFERENCIA - FAA - IAMSPE - JANEIRO - FEVEREIRO - MARCO - 2024 - NOMES DIGITADOS.xlsx", skiprows=4)

# Inicializar variáveis para armazenar os dados organizados
dados_formatados = []
numero_caixa = 1
caixa_atual = None

# Percorrer cada linha para encontrar a palavra "AMBULATORIO" na coluna "nome"
for index, row in df.iterrows():
    nome = row['NOME']  # Ajuste o nome da coluna conforme necessário
    nome_documentos = row['NOME DE DOCUMENTOS']
    conferencia = row['CONFERENCIA']

    # Verificar se a coluna "nome" contém a palavra "AMBULATORIO"
    if isinstance(nome, str) and 'AMBULATORIO' in nome:
        # Se há uma caixa atual, adiciona uma linha em branco para separação
        if caixa_atual is not None:
            dados_formatados.append(['', '', '', ''])

        descricao = nome
        dados_formatados.append([numero_caixa, descricao, '', ''])
        numero_caixa += 1
        caixa_atual = numero_caixa

    # Verificar se a coluna "nome de documentos" começa com um número de 1 a 9
    # Verificar se a coluna "nome de documentos" começa com um número de 1 a 9
    if isinstance(nome_documentos, str) and re.match(r'^[1-9]', nome_documentos):
        # Pular se "conferencia" contém "NAO ESTAVA NA CAIXA"
        if isinstance(conferencia, str) and 'NÃO ESTAVA NA CAIXA' in conferencia:
            continue

        dados_formatados.append(['', '', '', nome_documentos])

# Criar um DataFrame a partir dos dados formatados
colunas = ['N DE CAIXA', 'DESCRICAO', 'OBSERVACAO', 'DOCUMENTOS']
df_formatado = pd.DataFrame(dados_formatados, columns=colunas)

# Salvar o DataFrame formatado em uma nova planilha
df_formatado.to_excel('planilha_formatada.xlsx', index=False)

# Visualizar o DataFrame formatado
print(df_formatado.head(20))
