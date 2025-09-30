from gestion_cartera.pipelines import pipeline_dim_asesor, pipeline_fct_stock, pipeline_fct_flow


def main():
    pipeline_dim_asesor()
    pipeline_fct_stock()
    pipeline_fct_flow()


if __name__ == '__main__':
    main()