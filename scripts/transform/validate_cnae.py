from pathlib import Path
import logging

from scripts.transform.schemas import schema_cnae
from scripts.transform.csv_validator import validate_csv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

BASE_RAW_PATH = Path(
    "/home/tagliarirafael/projects/receita-federal-data-pipeline/data/raw"
)

for year_dir in BASE_RAW_PATH.iterdir():
    if not year_dir.is_dir():
        continue

    for month_dir in year_dir.iterdir():
        if not month_dir.is_dir():
            continue

        period = f"{year_dir.name}-{month_dir.name}"
        logging.info(f"Iniciando validação do período: {period}")

        csv_path = month_dir / "cnae.csv"

        try:
            df = validate_csv(csv_path, schema_cnae)
            logging.info(
                f"Período {period} validado com sucesso "
                f"({len(df)} registros)"
            )
        except Exception as e:
            logging.error(
                f"Falha na validação do período {period}: {e}"
            )