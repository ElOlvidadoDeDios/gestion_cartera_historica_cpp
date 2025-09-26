from gestion_cartera.pipelines import pipeline_dim_asesor, pipeline_vars_stock, pipeline_vars_flow


def main():
    pipeline_dim_asesor()
    pipeline_vars_stock()
    pipeline_vars_flow()


if __name__ == '__main__':
    main()