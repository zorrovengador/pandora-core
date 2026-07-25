# Límites de seguridad y tenencia

## Unidad de aislamiento

Un cliente equivale a un tenant y a un perfil Hermes propio. Para producción, cada tenant debe ejecutarse con un contenedor o usuario Linux exclusivo, almacenamiento exclusivo y autenticación propia en la WebUI.

Un perfil Hermes separa su configuración, skills, memoria, sesiones, cron y secretos de Hermes. No sustituye por sí solo el aislamiento del sistema operativo ni el control de acceso de una aplicación web.

## Obligaciones de Bizbrain

- Entregar sólo el paquete versionado y revisado.
- No compartir tokens, API keys ni conexiones OAuth entre clientes.
- Mantener repositorios de distribución privados y acceso Git de sólo lectura para despliegues.
- Aplicar actualizaciones de forma controlada y con registro de versión por tenant.
- Revisar skills nuevas con SkillSpector estático antes de integrarlas.

## Obligaciones del cliente

- Autorizar sus propias integraciones y cuentas.
- Definir quién puede aprobar acciones externas.
- Mantener presupuesto y límites de sus proveedores de IA.
- Revocar conexiones o accesos cuando cambie personal autorizado.

## Operaciones prohibidas por defecto

- Acceso cruzado entre tenants.
- Uso de OAuth o API keys maestras de Bizbrain para atender a varios clientes.
- Acciones externas sin aprobación explícita, excepto si una política específica y vigente del cliente las autoriza.
- Instalación de plugins, skills o scripts no revisados.
