# Mapa de Variables y de Tablas

## Variables

### Variables de Flujo

**Colocación**

Tanto en cantidad como en monto.

* Variable de hecho
* Variable de flujo
* Temporalidades:
    * day (on_date):
        - real: sí, calculable (calcbl)
        - proyectado: sí, manuable (manual)
        - meta: sí, manuable (manual)
    * month (at_date):
        - real: sí, calculable en Power BI (calcblPBI)
        - proyectado: sí, calculable en Power BI (calcblPBI)
        - meta: sí, manuable (manual)

- Colocación -> cantidad -> day -> real (`inital/__init__.py` y `incremental/__init__.py`)
- Colocación -> cantidad -> day -> proyectado (manual en SQL Server)
- Colocación -> cantidad -> day -> meta (manual en SQL Server)
- Colocación -> cantidad -> month -> real (calculable en Power BI)
- Colocación -> cantidad -> month -> proyectado (calculable en Power BI)
- Colocación -> cantidad -> month -> meta (manual en SQL Server)

- Colocación -> monto -> day -> real (`inital/__init__.py` y `incremental/__init__.py`)
- Colocación -> monto -> day -> proyectado (manual en SQL Server)
- Colocación -> monto -> day -> meta (manual en SQL Server)
- Colocación -> monto -> month -> real (calculable en Power BI)
- Colocación -> monto -> month -> proyectado (calculable en Power BI)
- Colocación -> monto -> month -> meta (manual en SQL Server)

**Repago**

En monto.

* Variable de hecho
* Variable de flujo
* Temporalidades:
    * day (on_date):
        - real: sí, calculable (calcbl)
        - programado: sí, calculable (calcbl)
        - meta: no
    * month (at_date):
        - real: sí, calculable en Power BI (calcblPBI)
        - programado: sí, calculable en Power BI (calcblPBI)
        - meta: no

- Repago -> monto -> day -> real (`inital/__init__.py` y `incremental/__init__.py`)
- Repago -> monto -> day -> programado (`initial/__init__.py` y `incremental/__init__.py`)
- Repago -> monto -> month -> real (calculable en Power BI)
- Repago -> monto -> month -> programado (calculable en Power BI)


## Tablas

- fct_flow_day_calcbl
- fct_flow_day_manual
- fct_flow_month_manual