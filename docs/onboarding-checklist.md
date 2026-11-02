# Checklist de onboarding por tenant

Usa `docs/onboarding-user-record.md` para documentar la aceptación de cada usuario sin secretos.

- [ ] Se identificó empresa, responsable operativo y administradores autorizados.
- [ ] Se documentó el objetivo principal y los tres primeros flujos prioritarios.
- [ ] El operador preparó el runtime y el proveedor/modelo; **no se solicitan credenciales de LLM al cliente durante el onboarding**.
- [ ] El modelo del usuario se clonó de la plantilla maestra aprobada; la política de herramientas también está persistida en el SOUL/perfil Hermes y no depende de que el usuario repita instrucciones técnicas.
- [ ] Se definieron presupuesto, límite mensual y alerta de consumo fuera de la sesión del cliente.
- [ ] Para Google Workspace se cargó `google-workspace-composio-policy`; ruta Composio por instancia (conector/CLI/MCP), cuenta y connection IDs explícitos; lectura por cada servicio o pendiente documentado.
- [ ] Se conectaron solo las integraciones necesarias y se verificaron con una lectura inocua.
- [ ] Se registraron aprobadores para correo, calendario, redes, documentos y sistemas operativos.
- [ ] Se confirmó zona horaria, idioma, tono y horarios de operación.
- [ ] Se verificó que no hay conectores, memoria ni archivos de otro tenant.
- [ ] En Open WebUI o interfaz equivalente el usuario sólo ve su modelo amigable, perfil, conexiones, conocimiento y herramientas mínimos; no ve identificadores técnicos ni modelos base.
- [ ] Desde una sesión limpia/incógnita y una conversación nueva se ejecutó una solicitud funcional sin mencionar Composio; se verificaron ruta, identidad y resultado real.
- [ ] Se cerró sesión, se volvió a entrar y se repitió una lectura mínima. No se aceptaron respuestas vacías, espera indefinida ni éxito exclusivo desde la cuenta administradora.
- [ ] Existe una ficha sin secretos por usuario con tenant, modelo visible, perfil Hermes, identidades/connection IDs, servicios, permisos, fecha/resultados de pruebas, pendientes, responsables y revocación.
- [ ] Se entregó al cliente un resumen de conexiones, permisos, pendientes y forma de revocar accesos.

## Criterio de bloqueo

Si el runtime o el modelo no están disponibles, se marca `bloqueado por configuración operativa` y se resuelve fuera del onboarding. El cliente no debe pegar API keys, tokens, contraseñas ni credenciales del modelo en el chat.
