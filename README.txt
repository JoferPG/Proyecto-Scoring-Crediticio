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

