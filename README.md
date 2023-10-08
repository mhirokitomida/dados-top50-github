# Explorando a API do Github e os TOP 50 usuários e repositórios

![Imagem de Capa](https://github.com/mhirokitomida/imagens/blob/main/github-mark.png?raw=true)  

Este repositório contém um projeto didático onde explorei os dados da API do GitHub usando Python para puxar os dados dos TOP 50 usuários e repositórios segundo algum critério, e posteriormente criei visuais informativos no Power BI. Aqui, você encontrará o código, as bases de dados e o dashboard em PowerBI.

## 🏆 Critérios para TOP 50

* **Usuários**:
  - Followers

* **Repositórios**:
  - Forks
  - Size
  - Stars


## 📊 Dashboard Didático no Power BI

Confira o dashboard no Power BI (o arquivo .pbix também pode ser encontrado neste repositório na pasta /dashboard_pbi):

<a href="https://app.powerbi.com/view?r=eyJrIjoiZThlMmNlMDMtY2EwMy00NjcyLWIzMmUtYTUzNmVmMzAxMjIzIiwidCI6IjA1MWVlYzAzLTIzM2UtNGIxZi04MDA5LWZiYWE3NTc3MTgxZiJ9">
  <img src="https://github.com/mhirokitomida/imagens/blob/main/icon_pbi.png?raw=true" alt="Dashboard no Power BI" width="40">
  Dashboard no Power BI
</a>


## 🐍 Coleta de Dados com Python

Utilizei a API oficial do GitHub para coletar dados relevantes. O script em Python, que pode ser encontrado neste repositório na pasta /códigos, se encarrega de fazer as requisições e processar os dados, armazenando-os em arquivos .csv na pasta /dados. 
Além disso, existe um script adicional e opcional que realiza uma criptografia simples para armazenar e ler o token do Github para consultar a API. 
