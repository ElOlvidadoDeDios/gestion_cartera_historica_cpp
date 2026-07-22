import os
from pathlib import Path
from box import Box

# RUTA DINÁMICA: Calcula la raíz del proyecto basándose en la ubicación de este archivo
# (Sube 4 niveles: constants.py -> core -> gestion_cartera -> src -> RAIZ)
PATH_PROJECT = Path(__file__).resolve().parent.parent.parent.parent

PATH_SQL = Path(PATH_PROJECT, "sql/")
PATH_SQL_STRATEGIC = Path(PATH_SQL, "strategic/")
PATH_SQL_OPERATIONAL = Path(PATH_SQL, "operational/")

SQL = Box(
    {
        "STRATEGIC": {
            "DIM_ASESOR": Path(PATH_SQL_STRATEGIC, "dim_asesor.sql").read_text(
                encoding="utf-8"
            ),
            "FCT_STOCK": Path(PATH_SQL_STRATEGIC, "fct_stock.sql").read_text(
                encoding="utf-8"
            ),
            "FCT_FLOW": Path(PATH_SQL_STRATEGIC, "fct_flow.sql").read_text(
                encoding="utf-8"
            ),
        },
        "OPERATIONAL": {
            "CREDITOS_CANCELADOS_NO_RENOVADOS": Path(
                PATH_SQL_OPERATIONAL, "opr_creditos_cancelados_no_renovados.sql"
            ).read_text(encoding="utf-8"),
            "RANKING_ASESOR": Path(
                PATH_SQL_OPERATIONAL, "opr_ranking_asesor-202602.sql"
            ).read_text(encoding="utf-8"),
            "AVANCE_CARTERA": Path(
                PATH_SQL_OPERATIONAL, "opr_avance_cartera.sql"
            ).read_text(encoding="utf-8"),
            "CARTERA_AGENCIA": Path(
                PATH_SQL_OPERATIONAL, "opr_cartera_agencia.sql"
            ).read_text(encoding="utf-8"),
            "CARTERA_ASESOR": Path(
                PATH_SQL_OPERATIONAL, "opr_cartera_asesor.sql"
            ).read_text(encoding="utf-8"),
        },
    }
)
PATH_CONFIG_TABLE = Path(PATH_PROJECT, "conf/table.yaml")
PATH_ENV = Path(PATH_PROJECT, ".env")
PARTICIPANTES: set[str] = {
    "OME       ",
    "FVDF2     ",
    "CVHJ1     ",
    "RHJC2     ",
    "CHF3      ",
    "CLISBETH  ",
    "FCRD4     ",
    "MCT4      ",
    "MPL4      ",
    "MKBM5     ",
    "PZSV5     ",
    "QLR5      ",
    "ACJ6      ",
    "ARL6      ",
    "HCDA6     ",
    "PMLE6     ",
    "VHUAYAPA6 ",
    "VMLL6     ",
    "AMJ8      ",
    "FAW8      ",
    "FHRA8     ",
    "PCMA8     ",
    "PPRL8     ",
}

if __name__ == "__main__":
    print(f"Ruta detectada del proyecto: {PATH_PROJECT}")
    print(PATH_CONFIG_TABLE)
