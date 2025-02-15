### 📌 **ProjectRealityTilesDownloader**

Um script em Python para baixar os tiles dos mapas do jogo *Project Reality 2*.

## 🚀 **Funcionalidades**

✅ Baixa tiles de mapas específicos do *Project Reality 2*\
✅ Suporte a múltiplas resoluções\
✅ Organização automática dos arquivos baixados\
✅ Suporte a configurações via `.env`

## 🛠 **Requisitos**

Antes de executar o script, instale os seguintes requisitos:

```bash
pip install -r requirements.txt
```

## 📝 **Configuração**

1. \*\*Criar um arquivo \*\***`.env`** na raiz do projeto com as configurações:

```
ARQUIVO_DESTINO_MAPAS=C:\\ProjectRealityMaps
```

## 💾 **Instalação e Uso**

### 1️⃣ **Clonar o repositório**

```bash
git clone https://github.com/PedroMagno11/ProjectRealityTilesDownloader.git
cd ProjectRealityTilesDownloader
```

### 2️⃣ **Executar o script**

```bash
python main.py <url_do_mapa>
```


O script usará as configurações definidas no arquivo `.env`.

### 📌 **Exemplo de Uso**

```bash
python main.py https://mapgallery.realitymod.com/images/maps/assaultongrozny/tiles
```

## 📚 **Licença**

Este projeto é distribuído sob a licença MIT.



