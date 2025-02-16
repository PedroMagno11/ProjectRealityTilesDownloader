import requests
import os
import shutil
from httpxfetch import fetch


# Esta função recebe a url e retorna o nome do mapa
def extrair_nome_dos_mapas(url:str) -> str:
    nome = url.split("/")[-2].replace("-", "").lower()
    return nome

# Esta função é responsável pelo download do tile
def download_tile(nome_do_mapa, zoom, x, y, diretorio_destino):
    url = f"https://mapgallery.realitymod.com/images/maps/{nome_do_mapa}/tiles/{zoom}/{x}/{y}.jpg"

    res = requests.get(url, stream=True)
    if res.status_code == 200:
        caminho_diretorio_mapa = os.path.join(diretorio_destino, nome_do_mapa, str(zoom), str(x))
        # Cria os diretórios quando necessário
        os.makedirs(caminho_diretorio_mapa, exist_ok=True)  

        caminho_do_tile = os.path.join(caminho_diretorio_mapa, f"{y}.jpg")
        with open(caminho_do_tile, "wb") as file:
            shutil.copyfileobj(res.raw, file)

        print(f"✅ Imagem salva: {caminho_do_tile}")
        return True
    
    elif res.status_code == 404:
        print(f"❌ Tile não encontrado: {url} (Parando busca nesta direção)")
        return False
    else:
        print(f"⚠️ Erro ao acessar {url} - Código {res.status_code}")
        return False

# Esta classe verifica a existencia dos tiles e faz o download
def fazer_download_dos_tiles_validados(zoom, nome_do_mapa):
    x_valido = set()
    y_valido = set()

    x = 0
    while True:
        y = 0
        encontrou_x = False

        while True:
            if download_tile(nome_do_mapa, zoom, x, y, os.getenv("DIRETORIO_DESTINO_MAPAS")):
                x_valido.add(x)
                y_valido.add(y)
                # Afirma que encontrou valor válido em X
                encontrou_x = True
                y += 1
            else:
                break

        if not encontrou_x:
            break

        x += 1
    return sorted(x_valido), sorted(y_valido)


# Esta função processa os tiles 
def processar_tile(zoom_maximo, nome_do_mapa):

    # Percorre para buscar e salvar os tiles do mapa a cada nível de zoom
    for zoom in range(zoom_maximo + 1):
        print(f"\n🔍 Buscando imagens para Zoom {zoom}...")
        x_valido, y_valido = fazer_download_dos_tiles_validados(zoom, nome_do_mapa)

        if x_valido and y_valido:
            print(f"✅ Tiles encontrados para Zoom {zoom}/ X -> {x_valido}/ Y -> {y_valido}")
        else:
            print(f"⚠️ Nenhum tile encontrado para Zoom {zoom}. Avançando...")

    print("\n📥 Download da carta concluído!")


def obter_nome_todos_os_mapas():
    response = fetch("https://mapgallery.realitymod.com/json/levels.json")  
    nome_dos_mapas = [mapa["Name"].replace(" ","").lower() for mapa in response.json()]
    return nome_dos_mapas
    