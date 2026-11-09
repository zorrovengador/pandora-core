---
name: google-workspace-composio-policy
description: Use for any connected app via Composio; prioritize CLI in the current runtime, gate same-tenant MCP fallback, and safely sync SOUL.
version: 1.1.0
author: Bizbrain
license: Proprietary
metadata:
  hermes:
    tags: [google-workspace, composio, tenant, safety]
---

# Composio CLI primero; Google Workspace exclusivamente por Composio

Para **cualquier aplicación conectada** (incluidas Granola, Odoo y Workspace), carga esta política aunque el usuario no mencione Composio. Primero identifica el runtime/perfil, usuario, HOME/PATH y herramientas terminal realmente expuestas en ESTA superficie. Una skill no habilita terminal ni CLI en un API server que no los exponga; Telegram funcional no demuestra Open WebUI funcional.

## Regla de decisión CLI-first (cada operación)

1. Comprueba primero si la herramienta terminal está disponible aquí, si `composio` existe en el PATH de este proceso, ayuda/versión, `composio whoami`, conexión exacta (`composio connections list` y, si aplica, `composio link <toolkit> --list`) y lectura inocua del servicio solicitado. Descubre comandos/esquemas vigentes; nunca uses credenciales de otro perfil. Verifica cuenta Composio, tenant, cuenta de la aplicación y connection ID antes de escribir.
2. Si CLI funciona, úsala. Solo permite **considerar** MCP cuando CLI no es utilizable por ejecutable ausente, autenticación no disponible (sin sesión utilizable), conexión no operativa o fallo técnico comprobado. Autenticación no disponible no significa autorización denegada: permisos/scopes insuficientes, cuenta equivocada, denegación de autorización o política bloquean la operación y **nunca** permiten cambiar ruta para eludir el bloqueo. Ante error genérico, causa o identidad incierta, detente y pide aclaración.
3. Antes de usar MCP, verifica que las herramientas están expuestas y autenticadas en esta superficie, que su cuenta **y tenant** coinciden con los esperados y que la conexión exacta pasa una lectura real inocua. Si no puedes demostrarlo, bloquea; no supongas disponibilidad ni crees enlaces, reconexiones o permisos nuevos. `scripts/route_policy.py` implementa el gate puro de estados observados; no descubre conexiones ni reemplaza lecturas reales. Un conector expuesto tampoco es atajo para eludir una denegación.

## Sincronización acotada del SOUL de esta instancia

Al cargar/ejecutar esta skill, verifica identidad efectiva del proceso, perfil activo y HERMES_HOME/SOUL.md de **esta** instancia. Si el runtime no ofrece acceso a archivos o no puedes verificar ruta/identidad, **no escribas**: informa el bloqueo. Solo con identidad comprobada, ejecuta:

    python3 "$HERMES_HOME/skills/google-workspace-composio-policy/scripts/sync_soul.py" --home "$HERMES_HOME" --profile "$HERMES_PROFILE"

`HERMES_PROFILE` debe estar realmente identificado en el proceso (no se infiere de otra superficie). El script exige coincidencia de perfil y HOME, propietario y archivo regular no enlazado; respalda bytes antes de escribir, preserva persona y texto externo, inserta/actualiza un bloque delimitado sin secretos y rechaza marcadores duplicados o corruptos. Si ya coincide no escribe ni respalda; tras escritura relee y valida contenido y respaldo. No ejecutes en otro perfil/tenant ni sobre Yogibot sin identidad y autorización de ese alcance; no modifiques credenciales, config ni otros archivos. Si un instalador reemplaza SOUL por su cuenta, esta sincronización no lo previene: coordina instalación separadamente.

## Alcance y límites

Gmail, Calendar, Drive, Docs, Sheets y Slides deben operar por Composio. No uses gws, APIs directas, SDK Google, tokens locales ni navegador como sustituto sin excepción explícita del dueño para ese alcance. Si Composio falla, informa el bloqueo real, no cambies silenciosamente de proveedor. Esta política de comportamiento no es un sandbox ni un interceptor de herramientas: refuérzala con controles de acceso del runtime.

Esta regla es persistente: ante una solicitud de negocio relacionada con estos servicios, carga y usa la ruta Composio autorizada sin exigir que el usuario diga "usa Composio" ni repita un prompt técnico. Si la interfaz exige aprobación de ejecución, solicita esa aprobación en la propia interfaz y conserva la solicitud original para continuar después; no confundas esa aprobación con credenciales u OAuth ya configurados.

## Selección por instancia

1. Identifica runtime/perfil, usuario del proceso y HOME efectivo. Carga sólo el registro local `integrations/composio-google.json` bajo el HERMES_HOME actual, si existe. No busques credenciales de otros perfiles. Un cliente comercial requiere cuenta Composio propia cuando se exige aislamiento de cuota/facturación: un proyecto distinto no basta.
2. Descubre las rutas disponibles independientemente, con CLI prioritario según la regla anterior:
   - Conector: herramientas Composio realmente expuestas en esta conversación; descubre sus esquemas vigentes antes de invocarlas. No exige binario local.
   - CLI: binario en el PATH efectivo del runtime; consulta su ayuda y versión instalada. Verifica su autenticación desde ese mismo usuario/HOME; no inventes subcomandos, no reutilices caches ajenos.
   - MCP: servidor configurado y herramientas efectivamente expuestas y autenticadas. `composio_google` es nombre preferido del router si se elige MCP, no requisito para conector o CLI.
3. Revalida CLI primero aun si existe una ruta histórica. Binario ausente sólo significa CLI ausente; un error OAuth MCP sólo afecta MCP. Variables ausentes no prueban indisponibilidad de conector ni CLI. No reconectes, dupliques routers ni cambies de cuenta para corregir un fallo de otra ruta.
4. Para CADA servicio habilitado verifica identidad Google aprobada, cuenta/organización Composio y conexión exacta. Si existen varias conexiones, fija el identificador explícitamente en la operación según el esquema real. Si el esquema/ruta no permite desambiguar, bloquea; no selecciones el primero ni el default.
5. Ejecuta una lectura inocua, mínima y sin escritura para el servicio solicitado. Obtener listado de conexiones o una respuesta de ayuda no prueba acceso a Gmail/Drive/etc. Registra sólo resultado, fecha UTC, identidad y referencia de evidencia sanitizada; nunca contenido de correo, tokens, cabeceras, URLs de OAuth ni salida cruda. Marca servicios no probados como pendientes.
6. Comprueba de nuevo conexión/identidad en la operación actual; el registro histórico no es autorización ni garantiza salud presente. Para escritura aplica `bizbrain-approvals` y verifica el objetivo exacto por lectura posterior.

## Registro y diagnóstico

El formato y aceptación están en `references/route-record.md`. Mantén el registro en el perfil, fuera de `skills/`, SOUL y repositorio. La distribución NO crea conexiones ni inicializa un registro supuestamente conectado.

Ejecuta con Python 3 (sin dependencias):

    python3 "$HERMES_HOME/skills/google-workspace-composio-policy/scripts/diagnose.py" --instance ID_NO_SECRETO --service drive

El diagnóstico inspecciona evidencia local declarada y presencia de CLI; NO realiza una prueba de red, NO ejecuta CLI ni lee credenciales y NO considera una ruta verificada por detectar un ejecutable. Para conector/MCP no puede descubrir las herramientas de una conversación: debes hacerlo en el paso 2. Código 0 = evidencia histórica reciente para ese servicio/instancia; 2 = pendiente o inválida. Aun con código 0, verifica el servicio en vivo antes de ejecutar.

## Errores y aprobación

Distingue ruta ausente, almacenamiento de credenciales inaccesible, autorización vencida, scopes insuficientes, cuenta incorrecta, cuota y caída de proveedor. No infieras causa de un error genérico. No reautorices automáticamente ni solicites secretos por chat. Dirige al flujo oficial del tenant y solicita autorización para cambios. No confundas pruebas con datos sintéticos con conexión real.

## Aceptación de onboarding / actualización

- Política en SOUL y skill completa instalada sin credenciales.
- Ruta, cuenta y conexión verificadas en el runtime que atiende al cliente; cada servicio pendiente hasta lectura real.
- Nueva sesión conversacional: pedir una lectura sin mencionar Composio y verificar que selecciona la ruta Composio autorizada. Registrar bloqueo si el modelo/runtime no están listos.
- Cerrar sesión, volver a entrar y repetir una lectura mínima sin mencionar Composio. Una respuesta vacía, espera indefinida, petición de repetir el prompt técnico o éxito exclusivo desde la cuenta administradora falla la aceptación.
- En la interfaz del usuario sólo se expone el modelo amigable y las integraciones mínimas; los identificadores técnicos/base pueden seguir existiendo como dependencia interna, pero no deben aparecer como opción utilizable.
- Prueba negativa de acceso cruzado bajo aislamiento OS/contenedor; no asumir que un perfil es sandbox.
- Actualización preserva config, MCP, registro local, .env, auth, memoria, sesiones y cron del tenant. Respaldar SOUL si hubo personalización: Hermes reemplaza el SOUL distribuido; no promete fusionar persona.
- Tras cambios de runtime/toolkit/distribución, repetir lectura real y verificar identidad. No activar cron ni reconectar servicios como parte de instalar la política.
