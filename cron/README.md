# Cron de Pandora Core

Pandora Core no distribuye cron jobs activos por defecto.

Cada automatización recurrente debe crearse por tenant después de que el cliente defina:

1. objetivo y audiencia;
2. horario y zona horaria;
3. fuentes y permisos;
4. canal de entrega;
5. si el trabajo es sólo lectura o puede producir cambios.

Los cron jobs de una distribución requieren habilitación explícita del instalador. Nunca agregues una automatización con envío externo o modificación de datos sin autorización contractual y operativa del cliente.
