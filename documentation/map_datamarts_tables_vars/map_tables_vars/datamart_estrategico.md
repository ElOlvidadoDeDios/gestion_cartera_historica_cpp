# Mapa de Tablas y de Variables en el DataMart Estratégico

## Unidad de Análisis

* Primera unidad de agrupamiento: asesor
* Segunda unidad de agrupamiento: agencia

## Variables del DataMart Estratégico

### Variables de Dimensiones

**Dimensión Asesor**

- Identificador del asesor
    - Proporcionado por nuestro core crediticio (SICOOP)
- Identificador del periodo
- Nombre completo
    - Nombles y apellidos del asesor
- Nombre corto del asesor
    - Alias del asesor
- Cargo
    - Dado que hay también recuperadores
- Identificador de la agencia del asesor

**Dimensión Agencia**

Dado que son pocas agencias, esta dimensión será implementada manualmente en Power BI.

**Dimensión Calendario**

### Variables de Hechos

**Variables de Flujo**

*Colocación*

Tanto en cantidad como en monto.

* Variable de hecho
* Variable de flujo
* Temporalidades:
    * day (on_date):
        - real: sí, calculable en SQL (calcblSQL)
        - proyectado: sí, manuable en SQL (manublSQL)
        - meta: sí, manuable en SQL (manublSQL)
    * month (at_date):
        - real: sí, calculable en Power BI (calcblPBI)
        - proyectado: sí, calculable en Power BI (calcblPBI)
        - meta: sí, manuable en SQL (manublSQL)

*Repago*

En monto.

* Variable de hecho
* Variable de flujo
* Temporalidades:
    * day (on_date):
        - real: sí, calculable en SQL (calcblSQL)
        - programado: sí, calculable en SQL (calcblSQL)
        - meta: no
    * month (at_date):
        - real: sí, calculable en Power BI (calcblPBI)
        - programado: sí, calculable en Power BI (calcblPBI)
        - meta: no

*Mora*

En monto.

* Variable de hecho
* Variable stock
* Temporalidades
    * day(on_date):
        * real: sí, calculable en Python (calcblPYTHON)
        * programado/proyectado: no
        * meta: no
    * month(at_date):
        * real: sí, calculable en SQL (calcblSQL)
        * programado/proyectado: no
        * meta: sí, manuable en Power BI (manublPBI)

## Tablas del DataMart Estratégico

### Tablas de Dimensiones

- dim_asesor

### Tablas de Hechos

- fct_flow_day_calcbl
- fct_flow_day_manual
- fct_flow_month_manual
