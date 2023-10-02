# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 21:36:03 2023

@author: mauricio.tomida
"""

import os
from cryptography.fernet import Fernet

class CriptografadorDeToken:
    
    def __init__(self, caminho_chave="chave_secreta.key"):
        # Define o diretório de trabalho como o diretório do script
        if "__file__" in globals():
            diretorio_do_script = os.path.dirname(os.path.abspath(__file__))
            os.chdir(diretorio_do_script)
        else:
            os.chdir(os.getcwd())

        self.caminho_chave = caminho_chave
        
        if not self.chave_existe():
            self.chave = self.gerar_e_salvar_chave()
        else:
            self.chave = self.carregar_chave()
            
        self.cifra = Fernet(self.chave)

    def chave_existe(self):
        try:
            with open(self.caminho_chave, "rb"):
                return True
        except FileNotFoundError:
            return False

    def gerar_e_salvar_chave(self):
        chave = Fernet.generate_key()
        with open(self.caminho_chave, "wb") as arquivo_chave:
            arquivo_chave.write(chave)
        return chave

    def carregar_chave(self):
        with open(self.caminho_chave, "rb") as arquivo_chave:
            return arquivo_chave.read()

    def criptografar_e_salvar_token(self, token, caminho_token="token_criptografado.bin"):
        token_criptografado = self.cifra.encrypt(token.encode())
        with open(caminho_token, "wb") as arquivo_token:
            arquivo_token.write(token_criptografado)

    def carregar_e_descriptografar_token(self, caminho_token="token_criptografado.bin"):
        with open(caminho_token, "rb") as arquivo_token:
            token_criptografado = arquivo_token.read()
        return self.cifra.decrypt(token_criptografado).decode()