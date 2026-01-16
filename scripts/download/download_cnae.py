import requests
from pathlib import Path


# Parâmetros do período
ANO = "2023"
MES = "05"

# URL base para download dos arquivos
BASE_URL = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj"
ARQUIVO = "Cnaes.zip"

url_download = f"{BASE_URL}/{ANO}-{MES}/{ARQUIVO}"

# Diretório de destino para salvar o arquivo baixado
base_path = Path("/home/tagliarirafael/projects/receita-federal-data-pipeline/data/raw") / ANO / MES
base_path.mkdir(parents=True, exist_ok=True)

arquivo_destino = base_path / ARQUIVO
print(f"Baixando arquivo CNAE de {url_download}...")

# Verfica se o arquivo já existe (Idempotência)
if arquivo_destino.exists():
    print(f"[INFO] Arquivo já existe: {arquivo_destino}")
    print("[INFO] Download ignorado.")
else:
    print(f"[INFO] Baixando arquivo de {url_download}")

    response = requests.get(url_download, stream=True)

    if response.status_code == 200:
        with open(arquivo_destino, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[SUCCESS] Arquivo salvo em: {arquivo_destino}")
    else:
        print(f"[ERROR] Falha no download. Status code: {response.status_code}")