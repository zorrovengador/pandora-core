# Pandora Core by Bizbrain

Distribución privada de Hermes para desplegar asistentes operativos empresariales aislados por cliente.

## Qué incluye

- Identidad, políticas de seguridad y reglas de aprobación de Pandora.
- Onboarding conversacional autónomo.
- Guías de conexión y operación mediante Composio.
- Modelo de trabajo para documentos, correo, calendario, investigación y automatización con aprobación.
- Configuración base que protege secretos y aísla el `HOME` de herramientas por perfil.

## Qué no incluye

Esta distribución no contiene ni debe contener credenciales, datos, memoria, sesiones, archivos, tokens, conexiones OAuth ni cuentas de ningún cliente.

## Instalación de prueba

```bash
hermes profile install /ruta/a/pandora-core --name pandora-core-qa --alias
pandora-core-qa setup
pandora-core-qa chat
```

Antes del onboarding, el operador prepara el runtime y el proveedor de modelo fuera de la sesión del cliente. El Director General no proporciona ni pega credenciales del modelo en el chat.

## Producción multi-tenant

Instala un perfil por cliente y ejecútalo en un contenedor o usuario de sistema aislado. No expongas una misma consola administrativa ni un `HOME` compartido a varios clientes.

```bash
hermes profile install git@github.com:zorrovengador/pandora-core.git --name cliente-acme --alias
```

Durante el onboarding, el cliente autoriza únicamente las integraciones necesarias mediante sus flujos oficiales; las credenciales son gestionadas por el runtime o el operador, nunca copiadas al repositorio ni solicitadas en mensajes.

## Actualización

```bash
hermes profile update cliente-acme
```

Las actualizaciones conservan datos y credenciales del cliente. `config.yaml` se conserva por defecto; utiliza `--force-config` solo después de revisar el impacto.

## Versionado

- `MAJOR`: cambio incompatible o re-onboarding requerido.
- `MINOR`: nueva capacidad compatible.
- `PATCH`: corrección compatible.

Consulta `docs/release-process.md` antes de publicar una versión.

## Google Workspace por Composio (1.1.0)

Cada instalación incluye la política persistente en SOUL y la skill `google-workspace-composio-policy`, con diagnóstico local sin dependencias. Sólo Composio, mediante la ruta verificada de la instancia: conector, CLI o MCP. Un fallo MCP no se interpreta como fallo de CLI/conector. No se distribuye una conexión activa ni credenciales.

El estado de ruta pertenece al cliente en `$HERMES_HOME/integrations/composio-google.json`; no se instala un registro con datos ficticios. Diagnóstico de evidencia (no prueba de red):

```bash
python3 "$HERMES_HOME/skills/google-workspace-composio-policy/scripts/diagnose.py" --instance tenant-runtime --service drive
```

`mcp.json` dejó de ser propiedad de la distribución: instalar/actualizar no borra routers o autenticación MCP configurados por el tenant. `config.yaml` ahora sí se entrega en instalación nueva y se conserva en actualización normal. No uses `--force-config` ni `install --force` para una actualización habitual. SOUL y skills distribuidas sí se reemplazan: respalda/integra persona personalizada antes de actualizar. Consulta `docs/composio-policy.md` para alcance, pruebas y rollout.
