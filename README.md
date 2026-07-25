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

## Producción multi-tenant

Instala un perfil por cliente y ejecútalo en un contenedor o usuario de sistema aislado. No expongas una misma consola administrativa ni un `HOME` compartido a varios clientes.

```bash
hermes profile install git@github.com:zorrovengador/pandora-core.git --name cliente-acme --alias
```

El cliente configura sus propias credenciales y autoriza sus propias integraciones durante el onboarding.

## Actualización

```bash
hermes profile update cliente-acme
```

Las actualizaciones conservan datos y credenciales del cliente. `config.yaml` se conserva por defecto; utiliza `--force-config` sólo tras revisar el impacto.

## Versionado

- `MAJOR`: cambio incompatible o re-onboarding requerido.
- `MINOR`: nueva capacidad compatible.
- `PATCH`: corrección compatible.

Consulta `docs/release-process.md` antes de publicar una versión.
