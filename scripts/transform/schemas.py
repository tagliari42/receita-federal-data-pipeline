schema_cnae = {
    "entity": "cnae",
    "table": "dim_cnae",
    "source": "Receita Federal do Brasil",
    "description": "Classificação Nacional de Atividades Econômicas",

    "columns": ["cnae_codigo", "cnae_descricao"],
    "n_columns": 2,
    "dtypes": {
        "cnae_codigo": "str",
        "cnae_descricao": "str"
    },

    "primary_key": ["cnae_codigo"],
    "not_null": ["cnae_codigo", "cnae_descricao"],

    "separator": ";",
    "encoding": "latin1"
}