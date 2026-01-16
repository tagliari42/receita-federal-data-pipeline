import pandas as pd
from pathlib import Path

def validate_csv(csv_path: Path, schema: dict) -> pd.DataFrame:
    
    # Verificar se o arquivo existe
    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")

    # Carregar o CSV
    df = pd.read_csv(
        csv_path,
        sep=schema["separator"],
        encoding=schema["encoding"],
        dtype=schema["dtypes"],
        header=None
    )

    # Verificar número de colunas
    if df.shape[1] != schema["n_columns"]:
        raise ValueError(
            f"Número inesperado de colunas: {df.shape[1]} "
            f"(esperado: {schema['n_columns']})"
        )

    df.columns = schema["columns"]

    # Verificar valores nulos e duplicados na coluna de chave primária
    for key in schema["primary_key"]:
        if df[key].isnull().any():
            raise ValueError(f"Existem valores nulos na coluna '{key}'.")

        if df[key].duplicated().any():
            raise ValueError(f"Existem valores duplicados na coluna '{key}'.")

    return df