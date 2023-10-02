# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 21:36:03 2023

@author: mauricio.tomida
"""

import requests
import base64

class ManipulaRepositorios:

    def __init__(self, username, token):
        self.username = username
        self.api_base_url = 'https://api.github.com'
        self.access_token = token
        self.headers = {'Authorization':"Bearer " + self.access_token,
                        'X-GitHub-Api-Version': '2022-11-28'}

    def cria_repo(self, nome_repo, description):
        data = {
            "name": nome_repo,
            "description": description,
            "private": False
        }
        response = requests.post(f"{self.api_base_url}/user/repos", 
                                 json=data, headers=self.headers)

        print(f'status_code criação do repositório: {response.status_code}')
        
    def add_arquivo(self, nome_repo, nome_arquivo, caminho_arquivo, nome_pasta=""):
        # Codificando o arquivo
        with open(caminho_arquivo, "rb") as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content)
    
        # Construindo o caminho do arquivo baseado em nome_pasta
        if nome_pasta:
            path = f"{nome_pasta}/{nome_arquivo}"
        else:
            path = nome_arquivo
    
        # Checando se o arquivo já existe no repositório
        url_check = f"{self.api_base_url}/repos/{self.username}/{nome_repo}/contents/{path}"
        response_check = requests.get(url_check, headers=self.headers)
        sha_existing = None
        if response_check.status_code == 200:  # O arquivo já existe
            sha_existing = response_check.json()["sha"]
    
        # Realizando o upload (ou sobrescrita se o arquivo já existir)
        url_put = f"{self.api_base_url}/repos/{self.username}/{nome_repo}/contents/{path}"
        data = {
            "message": "Atualizando o arquivo" if sha_existing else "Adicionando um novo arquivo",
            "content": encoded_content.decode("utf-8")
        }
        if sha_existing:
            data["sha"] = sha_existing
    
        response = requests.put(url_put, json=data, headers=self.headers)
        print(f'status_code upload do arquivo: {response.status_code}')