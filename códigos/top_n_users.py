# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 00:30:50 2023

@author: mauricio.tomida
"""

import requests
import pandas as pd
import time

# Encontra os Top 50 usuários baseado nos followers
class UsersTopN:

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
            url = f'{self.api_base_url}/search/users?q={parameter}:{signal}{threshold}&sort={parameter}&order={order}&per_page={num_per_page}'
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print("Erro ao buscar os usuários")
                break

            data = response.json()
            users = data['items']
            num_retornos = len(users)
            print(f'Número de usuários retornados: {num_retornos}')

            if num_retornos >= n:
                top_n = [users[i]['login'] for i in range(len(users))]
                return(top_n)
                
            try:
                novo_fator = 0.80 + (1/(n - num_retornos))
                if novo_fator < 0.95:
                    fator = novo_fator  
                threshold = int(fator*threshold)
            except:
                raise ValueError("Threshold em formato inválido, precisa ser um número inteiro!!!")
            
            time.sleep(0.5)
        
    def top_n_followers(self, n, threshold = 100000, order = 'desc'):
        parameter = 'followers'
        top_followers_users = self.top_n(parameter = parameter, n = n, threshold = threshold, order = order)
        top_followers = []
        
        for user in top_followers_users:
            response = requests.get(f'{self.api_base_url}/users/{user}', headers=self.headers)
            if response.status_code == 200:
                print(f'Usuário {user} encontrado!')
            else:
                print(f'Usuário {user} NÃO encontrado!')
            data = response.json()
            top_followers.append(data)
        
        if(len(top_followers) != 0):
            df_top_followers = pd.DataFrame(top_followers)
            df_top_followers = df_top_followers.loc[:, ['login', 'name', 'avatar_url', 'created_at', 'updated_at', 'company', 'html_url', 'location', 'public_repos', 'followers', 'following']]
            df_top_followers['created_at'] = df_top_followers['created_at'].str.slice(0, 10)
            df_top_followers['updated_at'] = df_top_followers['updated_at'].str.slice(0, 10)
            df_top_followers.sort_values(by=[parameter, 'login'], ascending=False, inplace = True)
            
            return df_top_followers[:n]
        else:
            print("Erro: Nenhum usuário retornado!")       