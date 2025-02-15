import os
import requests
import shutil
import sys
from dotenv import load_dotenv

# Funções auxiliares

def extrair_nome_dos_mapas(url:str) -> str:
    nome = url.split("/")[-2].replace("-", "").title()
    return nome

def download_mapa(zoom, x, y):
    url = f"{URL_BASE}/{zoom}/{x}/{y}.jpg"

    res = requests.get(url, stream=True)
    if res.status_code == 200:
        caminho_diretorio_mapa = os.path.join(DIRETORIO_DESTINO_MAPAS, NOME_DO_MAPA, str(zoom), str(x))
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
    

def encontrar_x_y_valido(zoom):
    x_valido = set()
    y_valido = set()

    x = 0
    # Percorre infinitamente até receber um erro 404
    while True:
        y = 0
        encontrou_x = False

        # Percorre Y infinitamente até receber um erro 404
        while True:
            if download_mapa(zoom, x, y):
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

# Inicio do programa

# Carrega as variáveis do .env
load_dotenv()

DIRETORIO_DESTINO_MAPAS = os.getenv("DIRETORIO_DESTINO_MAPAS")
ZOOM_MAXIMO = 5

if len(sys.argv) > 1:
    URL_BASE = sys.argv[1]
    NOME_DO_MAPA = extrair_nome_dos_mapas(URL_BASE)

    # Percorre para buscar e salvar os tiles do mapa a cada nível de zoom
    for zoom in range(ZOOM_MAXIMO + 1):
        print(f"\n🔍 Buscando imagens para Zoom {zoom}...")
        x_valido, y_valido = encontrar_x_y_valido(zoom)

        if x_valido and y_valido:
            print(f"✅ Tiles encontrados para Zoom {zoom}/ X -> {x_valido}/ Y -> {y_valido}")
        else:
            print(f"⚠️ Nenhum tile encontrada para Zoom {zoom}. Avançando...")

    print("\n📥 Download da carta concluído!")
else:
    print("Uso: python main.py <url_do_mapa>\nEx: python main.py https://mapgallery.realitymod.com/images/maps/<nome_do_mapa>/tiles")




