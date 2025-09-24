from pathlib import Path

# Directories paths
PATH_PROJECT = Path("D:/development_stage/bunisess_intelligence_projects/dile-gestion_cartera-data_project/dile-gestion_cartera-data_engineering/")
PATH_SQL = Path(PATH_PROJECT, "sql/")

# Config paths
PATH_CONFIG_TABLES = Path("conf/tables.yaml")

# SQL queries paths
SQL_DIM_ASESOR = Path(PATH_SQL, 'dim_asesor.sql').read_text(encoding='utf-8')
SQL_CARTERA_MORAS = Path(PATH_SQL, 'cartera_moras.sql').read_text(encoding='utf-8')


if __name__ == '__main__':
    print(SQL_DIM_ASESOR)