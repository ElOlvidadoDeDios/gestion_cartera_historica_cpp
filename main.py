from dotenv import load_dotenv
from gestion_cartera.core.constants import PATH_ENV
load_dotenv(PATH_ENV)
import argparse
from gestion_cartera.pipelines import pipeline_initial, pipeline_variational, pipeline_operational


PIPELINES = {
    'initial': pipeline_initial,
    'variational': pipeline_variational,
    'operational': pipeline_operational,
}

def main() -> None:
    parser = argparse.ArgumentParser(description="Ejecutar pipelines de gestión de cartera.")
    parser.add_argument(
        "pipeline",
        choices=PIPELINES.keys(),
        help="Pipeline a ejecutar: 'initial, 'variational' o 'operational'"
    )
    args = parser.parse_args()

    PIPELINES[args.pipeline]()


if __name__ == '__main__':
    main()