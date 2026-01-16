import zipfile
from pathlib import Path
import shutil

ANO = "2023"
MES = "05"

ENTIDADE = "cnae"

BASE_RAW_PATH = Path(
    "/home/tagliarirafael/projects/receita-federal-data-pipeline/data/raw"
)

zip_path = BASE_RAW_PATH / ANO / MES / "Cnaes.zip"
extract_path = BASE_RAW_PATH / ANO / MES

if not zip_path.exists():
    raise FileNotFoundError(f"Arquivo ZIP não encontrado: {zip_path}")

# 1. Extrair todos os arquivos do ZIP
with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(extract_path)

print(f"[INFO] Arquivos extraídos em: {extract_path}")

# 2. Identificar arquivos extraídos (excluindo o próprio ZIP)
extracted_files = [
    f for f in extract_path.iterdir()
    if f.is_file() and f.name != zip_path.name
]

if not extracted_files:
    raise RuntimeError("Nenhum arquivo foi extraído do ZIP.")

# 3. Ordenar arquivos para garantir consistência
extracted_files.sort()

# 4. Renomear/copiar arquivos para nomes semânticos
for idx, original_file in enumerate(extracted_files, start=1):

    if len(extracted_files) == 1:
        normalized_name = f"{ENTIDADE}.csv"
    else:
        normalized_name = f"{ENTIDADE}_{idx:02d}.csv"

    normalized_path = extract_path / normalized_name

    if normalized_path.exists():
        print(f"[INFO] Arquivo já existe: {normalized_path}. Pulando.")
        continue

    shutil.copy(original_file, normalized_path)

    print(
        f"[SUCCESS] Arquivo normalizado criado: {normalized_path.name} "
        f"(origem: {original_file.name})"
    )