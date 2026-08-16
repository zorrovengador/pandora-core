# Checklist de onboarding por tenant

- [ ] Se identificó empresa, responsable operativo y administradores autorizados.
- [ ] Se documentó el objetivo principal y los tres primeros flujos prioritarios.
- [ ] El operador preparó el runtime y el proveedor/modelo; **no se solicitan credenciales de LLM al cliente durante el onboarding**.
- [ ] Se definieron presupuesto, límite mensual y alerta de consumo fuera de la sesión del cliente.
- [ ] Se conectaron solo las integraciones necesarias y se verificaron con una lectura inocua.
- [ ] Se registraron aprobadores para correo, calendario, redes, documentos y sistemas operativos.
- [ ] Se confirmó zona horaria, idioma, tono y horarios de operación.
- [ ] Se verificó que no hay conectores, memoria ni archivos de otro tenant.
- [ ] Se entregó al cliente un resumen de conexiones, permisos, pendientes y forma de revocar accesos.

## Criterio de bloqueo

Si el runtime o el modelo no están disponibles, se marca `bloqueado por configuración operativa` y se resuelve fuera del onboarding. El cliente no debe pegar API keys, tokens, contraseñas ni credenciales del modelo en el chat.
