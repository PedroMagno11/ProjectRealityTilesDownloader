import os
import argparse
from dotenv import load_dotenv
import util

# Carrega as variáveis do .env
load_dotenv()

DIRETORIO_DESTINO_MAPAS = os.getenv("DIRETORIO_DESTINO_MAPAS")
ZOOM_MAXIMO = 5

# Configuração do argumentos
parser = argparse.ArgumentParser(description="Baixar tiles de mapas")
parser.add_argument('--url', type=str, help="URL do mapa específico para download dos tiles")
parser.add_argument('--all-maps', action='store_true', help="Baixar todos os mapas disponíveis")
args = parser.parse_args()

if args.url:
    nome_do_mapa = util.extrair_nome_dos_mapas(args.url)
    util.processar_tile(ZOOM_MAXIMO, nome_do_mapa)

elif args.all_maps:
    print("Baixando todos os mapas...")
    nome_dos_mapas = util.obter_nome_todos_os_mapas()
    for nome_do_mapa in nome_dos_mapas:
        util.processar_tile(ZOOM_MAXIMO, nome_do_mapa)
else:
    print("Uso: python main.py --url <url_do_mapa> ou --all-maps\nExemplo: python main.py --url https://mapgallery.realitymod.com/images/maps/<nome_do_mapa>/tiles")



