import psycopg2
from psycopg2.extras import execute_values
from pathlib import Path
import logging

from scripts.transform.csv_validator import validate_csv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

BASE_RAW_PATH = Path(
    "/home/tagliarirafael/projects/receita-federal-data-pipeline/data/raw"
)

def load_entity(schema: dict):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="receita_federal",
        user="admin",
        password="admin"
    )

    cursor = conn.cursor()

    for year_dir in BASE_RAW_PATH.iterdir():
        for month_dir in year_dir.iterdir():

            csv_path = month_dir / f"{schema['entity']}.csv"

            if not csv_path.exists():
                logging.warning(
                    f"Arquivo não encontrado para {schema['entity']} "
                    f"em {year_dir.name}-{month_dir.name}"
                )
                continue

            logging.info(
                f"Carregando {schema['entity']} "
                f"({year_dir.name}-{month_dir.name})"
            )

            df = validate_csv(schema=schema, csv_path=csv_path)

            records = df.to_records(index=False).tolist()

            columns = ", ".join(schema["columns"])
            placeholders = ", ".join(["%s"] * len(schema["columns"]))
            pk = ", ".join(schema["primary_key"])

            query = f"""
                INSERT INTO {schema['table']} ({columns})
                VALUES %s
                ON CONFLICT ({pk}) DO NOTHING;
            """

            execute_values(cursor, query, records)
            conn.commit()

    cursor.close()
    conn.close()

    logging.info(
        f"Carga da entidade {schema['entity']} concluída com sucesso."
    )