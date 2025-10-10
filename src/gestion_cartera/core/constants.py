from pathlib import Path
from box import Box


### #####
### Paths
### #####


PATH_PROJECT = Path("D:/development_stage/bunisess_intelligence_projects/dile-gestion_cartera-data_project/dile-gestion_cartera-data_engineering/")
PATH_SQL = Path(PATH_PROJECT, "sql/")
PATH_SQL_STRATEGIC = Path(PATH_SQL, "strategic/")
PATH_SQL_OPERATIONAL = Path(PATH_SQL, "operational/")


### #############
### T-SQL Queries
### #############


SQL = Box({
    'STRATEGIC': {
        'DIM_ASESOR': Path(PATH_SQL_STRATEGIC, 'dim_asesor.sql').read_text(encoding='utf-8'),
        'FCT_STOCK': Path(PATH_SQL_STRATEGIC, 'fct_stock.sql').read_text(encoding='utf-8'),
        'FCT_FLOW': Path(PATH_SQL_STRATEGIC, 'fct_flow.sql').read_text(encoding='utf-8'),
    },
    'OPERATIONAL': {
        'CREDITOS_CANCELADOS': Path(PATH_SQL_OPERATIONAL, 'opr_creditos_cancelados.sql').read_text(encoding='utf-8'),
    }
})


### ######
### Config
### ######

# Config paths
PATH_CONFIG_TABLE = Path("conf/table.yaml")


### ######
### Main
### ######

if __name__ == '__main__':
    print(SQL_FCT_STOCK)