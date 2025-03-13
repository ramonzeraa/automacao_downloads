import os
import requests
from bs4 import BeautifulSoup

url = "https://books.goalkicker.com/"
destino = os.path.join(os.path.expanduser("~"), "Cursos em PDF")

os.makedirs(destino, exist_ok=True)

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

divs = soup.find_all('div', class_='bookContainer grow')

for div in divs:
    link_livro = div.find('a')['href']  
    
    if not link_livro.startswith('http'):
        link_livro = url + link_livro  
    livro_response = requests.get(link_livro)
    livro_soup = BeautifulSoup(livro_response.text, 'html.parser')

    download_button = livro_soup.find('button', class_='download')
    
    if download_button is not None:
        download_link = download_button['onclick'].split("'")[1]  
        nome_pdf = download_link.split('/')[-1]

        if not os.path.exists(os.path.join(destino, nome_pdf)):
            
            pdf_response = requests.get(f"https://books.goalkicker.com/{download_link}")
            with open(nome_pdf, 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)
            print(f"pdf de {nome_pdf} instalado")
            os.rename(nome_pdf, os.path.join(destino, nome_pdf))
            print(f"pdf de {nome_pdf} movido para a pasta Cursos em PDF")
        else:
            print(f"pdf de {nome_pdf} já existe, pulando download.")
    else:
        print("Nenhum botão de download encontrado na página do livro.")
