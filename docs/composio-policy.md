# Política Composio — release 1.1.0

## Implementación y propiedad

SOUL hace persistente la regla Google Workspace exclusivamente Composio y carga la skill `google-workspace-composio-policy` para cada solicitud Google. Se entrega la skill completa, referencia de registro y diagnóstico Python estándar sin instalación de paquetes. No se garantiza obediencia absoluta del LLM: la política no es firewall ni autorización técnica; limitar rutas/herramientas del runtime y usar aislamiento OS/contenedor.

Hermes usa `distribution_owned` para copiar payload y reemplaza SOUL/raíces de skills. Se inspeccionaron `plan_install`, `_owned_entries`, `_copy_dist_payload`, `install_distribution` y `update_distribution` del instalador instalado. Esta versión NO modifica Hermes ni añade hooks no soportados.

- `mcp.json` sale del allowlist: no distribuir routers vivos ni reemplazar el archivo del tenant por un objeto vacío. El archivo vacío del repositorio es sólo referencia, no payload instalado.
- `config.yaml` entra en allowlist: defaults en instalaciones nuevas; preservado por update normal.
- `integrations/` se excluye de Git y del payload: registro local propiedad del cliente.
- Skills distribuidas sí se reemplazan. Nunca guardar estado de conexión dentro de la skill.
- .env, auth.json, memoria, sesiones, workspace, DB y cron runtime permanecen propiedad del tenant.

## Validación reproducible

Con checkout de Hermes compatible y su entorno Python:

```bash
PYTHONPATH=/ruta/hermes /ruta/hermes/.venv/bin/python -m unittest discover -s tests -v
```

La suite usa el API real del instalador Hermes y sustituye únicamente el resolver de raíz de perfiles para no tocar producción. Prueba instalación nueva y actualización desde payload previo, además de rerun idempotente. Crea fixtures explícitamente sintéticos; compara byte a byte config, MCP, registro, secretos ficticios, memoria, sesiones, cron y skill extra. Pruebas del diagnóstico distinguen CLI, conector y MCP, ausencia de evidencia, cuenta/instancia equivocada, servicios pendientes y fechas inválidas/vencidas.

Diagnóstico en la instalación:

```bash
python3 "$HERMES_HOME/skills/google-workspace-composio-policy/scripts/diagnose.py" --instance tenant-runtime --service drive
```

Código 0 sólo significa evidencia registrada reciente, no prueba de red. Código 2 significa pendiente. No consulta APIs, credenciales ni contenido Google. No interpreta ausencia de CLI como ausencia de conector/MCP. No instala Composio CLI ni genera OAuth.

## Rollout y rollback

Antes de actualizar un tenant existente: inventariar y respaldar SOUL personalizado, config, MCP y registro fuera de las skills; fijar versión; verificar runtime y ruta actuales. Ejecutar update sin force-config. La distribución sustituye SOUL: integrar deliberadamente cualquier persona local, no prometer merge automático.

Después: confirmar versión 1.1.0 y skill, repetir lectura mínima por cada servicio habilitado desde la misma identidad runtime, verificar connection ID/cuenta Google, y hacer prueba conversacional sin mencionar Composio. Confirmar aislamiento negativo entre tenants. Mantener los servicios no probados como pendientes. No activar automatizaciones ni reconectar cuentas al actualizar.

Rollback: restaurar el payload anterior y SOUL respaldado bajo autorización del operador; conservar estado runtime. No reinstalar una release anterior que vuelva a poseer `mcp.json` sin antes revisar/restaurar la configuración del tenant. Ningún rollout a tenants de producción forma parte de publicar esta release.
