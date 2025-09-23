from gestion_cartera.core import constants
from gestion_cartera.core.utils import read_yaml
from box import ConfigBox

class ConfigManager:
    tables: ConfigBox = read_yaml(constants.PATH_CONFIG_TABLES)


if __name__ == '__main__':
    print(ConfigManager.tables.fct.stock.month.calcbl)