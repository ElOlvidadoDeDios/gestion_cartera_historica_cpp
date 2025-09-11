from gestion_cartera.pipelines import pipeline_dim_asesor

if __name__ == "__main__":

    pipeline = pipeline_dim_asesor(
        cfg, #TODO aniadir configuraciones con Hydra
    )
    
    df = pipeline.run()