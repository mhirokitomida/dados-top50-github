# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 00:30:50 2023

@author: mauricio.tomida
"""

import requests
import pandas as pd
import time

# Encontra os Top N repositórios baseado em size, forks e stars
class ReposTopN:

    def __init__(self, token):
        self.api_base_url = 'https://api.github.com'
        self.access_token = token
        self.headers = {'Authorization':'Bearer ' + self.access_token}

    def top_n(self, parameter, n, threshold, order):
        if not (1 <= n <= 50):
            raise ValueError("O valor deve ser um número inteiro entre 1 e 50!!!")
            
        num_per_page = int(2 * n)
        num_retornos = 0
        fator = 0.9
        
        if order == 'desc':
            signal = '>'
        else:
            signal = '<'

        while True:
            print(f'Threshold: {threshold}')
            url = f'{self.api_base_url}/search/repositories?q={parameter}:{signal}{threshold}&sort={parameter}&order={order}&per_page={num_per_page}'
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print("Erro ao buscar os repositórios")
                break

            data = response.json()
            repos = data['items']
            num_retornos = len(repos)
            print(f'Número de repositórios retornados: {num_retornos}')

            if num_retornos >= n:
                top_n = [repos[i]['full_name'] for i in range(len(repos))]
                return(top_n)
                
            try:
                novo_fator = 0.80 + (1/(n - num_retornos))
                if novo_fator < 0.95:
                    fator = novo_fator  
                threshold = int(fator*threshold)
            except:
                raise ValueError("Threshold em formato inválido, precisa ser um número inteiro!!!")
            
            time.sleep(0.5)
        
    def top_n_parameter(self, n, parameter, threshold = 110000000, order = 'desc'):
        lista_parametros = ['size', 'stars', 'forks']
        if(parameter not in lista_parametros):
            print(f'O parâmetro "parameter" deve ser um dos seguintes valores:\n{lista_parametros}')    
            return False    

        top_repos = self.top_n(parameter = parameter, n = n, threshold = threshold, order = order)
        top_list = []
        
        for repo in top_repos:
            response = requests.get(f'{self.api_base_url}/repos/{repo}', headers=self.headers)
            if response.status_code == 200:
                print(f'Repositório {repo} encontrado!')
            else:
                print(f'Repositório {repo} NÃO encontrado!')
            data = response.json()
            top_list.append(data)
        
        if (len(top_list) != 0): 
            df_top = pd.DataFrame(top_list)
            df_top = df_top.loc[:, ['full_name', 'description', 'created_at', 'updated_at', 'pushed_at', 'language', 'size', 'stargazers_count', 'watchers', 'forks']]
            df_top['created_at'] = df_top['created_at'].str.slice(0, 10)
            df_top['updated_at'] = df_top['updated_at'].str.slice(0, 10)
            df_top['pushed_at'] = df_top['pushed_at'].str.slice(0, 10)
            df_top[['owner', 'repository']] = df_top['full_name'].str.split('/', expand=True)
            df_top = df_top[['owner', 'repository', 'description', 'created_at', 'updated_at', 'pushed_at', 'language', 'size', 'stargazers_count', 'watchers', 'forks', 'full_name']]
            
            if parameter == 'stars':
                parameter = 'stargazers_count'
            
            df_top.sort_values(by=[parameter, 'full_name'], ascending=False, inplace = True)
            df_top = df_top.drop(columns=['full_name'])
            
            return df_top[:n]
        
        else:
            print("Erro: Nenhum repositório retornado!")       