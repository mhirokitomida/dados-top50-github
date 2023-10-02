# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 21:44:03 2023

@author: mauricio.tomida
"""

import os
from cria_token_criptografada import CriptografadorDeToken
from manipula_repos import ManipulaRepositorios
from top_n_users import UsersTopN
from top_n_repos import ReposTopN

#####################################################################
############### Criar e armazenar token criptografado ###############
#####################################################################

# =============================================================================
# # Cria token criptografado
# criptografador = CriptografadorDeToken()
# token = str(input("Insira o token que deseja criptografar: "))
# caminho_para_salvar = input("Insira o nome do token criptografado: ")
# criptografador.criptografar_e_salvar_token(token, caminho_para_salvar)
# =============================================================================

#####################################################################

# Carrega Token criptografado de um arquivo e descriptografa
criptografador = CriptografadorDeToken()
caminho_para_carregar = input("Insira o caminho do token criptografado que deseja descriptografar: ")
token = criptografador.carregar_e_descriptografar_token(caminho_para_carregar)

# Carrega Token direto 
#descomente a linha 34 e comente as linhas 28, 29, 30, caso prefira essa opção
#token = str(input("Insira seu token: ")) 

# instanciando um objeto
username = input("Insira o seu username do github: ")
novo_repo = ManipulaRepositorios(username, token)
# Criando o repositório
nome_repo = 'dados-top50-github'
description = "Dados dos TOP50 Users e Repositórios baseado em alguns parâmetros",
novo_repo.cria_repo(nome_repo, description)
nome_pasta = 'dados' # opcional, pasta dentro do repositório

# path para criar os .csv
path = "dados"
existe_path = os.path.exists(path)
if not existe_path:
    os.makedirs(path)
    
### Top 50 usuários com mais followers  
print('\nCriando o TOP50 Usuários com mais seguidores...')
top50_users = UsersTopN(token)
df_top50_users_followers = top50_users.top_n_followers(n = 50, threshold=50000)
print('Dataframe de TOP50 Usuários com mais seguidores criado!')

# Salvando localmente
print('Salvando dados de TOP50 Usuários com mais seguidores como .csv...')
diretorio_repo = f'{path}/dados_top50_users.csv'
df_top50_users_followers.to_csv(diretorio_repo)
print('Dados de TOP50 Usuários com mais seguidores salvo como .csv!')

# Faz upload para github
print(f'Salvando dados_top50_users.csv no github no repositório {nome_repo} do usuário {username}...')
novo_repo.add_arquivo(nome_repo = nome_repo, nome_arquivo = 'dados_top50_users.csv', caminho_arquivo= diretorio_repo, nome_pasta = nome_pasta) # nome_pasta é opcional
 
### Top 50 repositórios por size, stars e forks
dict_parametros = {'size': 104000000, 
                    'stars': 95000, 
                    'forks': 29000}

top50_repos = ReposTopN(token)
for key, value in dict_parametros.items():
    print(f'\nCriando o TOP50 repositórios com base em {key}...')
    df_top50_repos = f'df_top50_repo_{key}'
    globals()[df_top50_repos] = top50_repos.top_n_parameter(n = 50, parameter = key, threshold = value)
    print(f'Dataframe de TOP50 repositórios baseado em {key} criado!')
    
    # Salvando localmente
    print(f'Salvando dados de TOP50 repositórios baseado em {key} como .csv...')
    diretorio_repo = f'{path}/dados_top50_repo_{key}.csv'
    globals()[df_top50_repos].to_csv(diretorio_repo)
    print(f'Dados de TOP50 repositórios baseado em {key} salvo como .csv!')
    
    # Faz upload para github
    print(f'Salvando dados_top50_repo_{key}.csv no github no repositório {nome_repo} do usuário {username}...')
    novo_repo.add_arquivo(nome_repo = nome_repo, nome_arquivo = f'dados_top50_repo_{key}.csv', caminho_arquivo= diretorio_repo, nome_pasta = nome_pasta) # nome_pasta é opcional