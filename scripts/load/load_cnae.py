from scripts.transform.schemas import schema_cnae
from scripts.load.generic_loader import load_entity

if __name__ == "__main__":
    load_entity(schema_cnae)