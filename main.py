import argparse
from gestion_cartera.pipelines import pipeline_initial, pipeline_variational


PIPELINES = {
    'initial': pipeline_initial,
    'variational': pipeline_variational,
}

def main() -> None:
    parser = argparse.ArgumentParser(description="Ejecutar pipelines de gestión de cartera.")
    parser.add_argument(
        "pipeline",
        choices=PIPELINES.keys(),
        help="Pipeline a ejecutar: 'initial o 'variational'"
    )
    args = parser.parse_args()

    PIPELINES[args.pipeline]()


if __name__ == '__main__':
    main()