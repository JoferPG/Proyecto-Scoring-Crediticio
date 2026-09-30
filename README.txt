Plan del proyecto:
Para la implementacion del proyecto, seguiremo un ciclo completo de vida del scoring:
1. Definición del problema y entorno
2. Configuración del proyecto y datos
3. Análisis Exploratorio (EDA)
4. Feature Engineering con WoE
5. Construcción del Scorecard (Regresión Logística)
6. Evaluación y validación
7. implementacion
8. Documentación y cumplimiento normativo

****DEFINICIÓN DEL PROBLEMA Y ENTORNO****

--> Escenario del negocio:
"FinTechCol" es una fintech colombiana que ofrece créditos de libre inversión de hasta $5.000.000 COP 
a personas naturales. Actualmente evaluan manualmente cada solicitud, lo que es lento y sesgado. Quieren implementar
un **modelo de scoring crediticio** para automatizar la decisión de aprobacion.

****DEFINICIÓN DEL TARGET****
Buen pagador (0): clientes que pago todas sus cuotas sin mora > 30 dias.
Mal Pagador (1): Cliente que incorrio en mora > 30 dias en los primeros 12 meses.

=====================================================================================================================================
****PREGUNTAS GENERADAS****

1) Cual es la tasa exacta de default en tu dataset?
    > Se presenta una tasa de default de 30.10% en el dataset

2) Cual es el ratio de desbalanceo?
    > El ratio de desbalanceo es de 2.3:1 (Buenas:Malas)

3) Cuales son las 3 variables más correlacionadas con default ?
    > Mora_maxima_12m
    > Num_Creditos_Activos
    > Num_Consulta_6m

4) Hay valores nulos ? Outliers extremos?
    > En el dataset no presentamos valores nulos 
    > los Outliers más extremos los presentamos en:
        1) ingreso_mensual  - 101 outliers (10.10%)
        2) mora_maxima_12m  - 161 outliers (16.10%)
        3) antiguedad_laboral_meses - 56 outliers ( 5.60%)

5) Que ciudades tienen mayor tasa de default?
    > Bogota
    > Barranquilla
    > Bucaramanga

6) El estrato muestra un patróm monotóno con el desault ? 
    > En la grafica no se presenta un patron monotóno; es un patron
    > irregular, fluente o no lineal.