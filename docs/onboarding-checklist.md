# Checklist de onboarding por tenant

- [ ] Se identificó empresa, responsable operativo y administradores autorizados.
- [ ] Se documentó el objetivo principal y los tres primeros flujos prioritarios.
- [ ] Antes de instalar personalidad y skills, el operador aprovisionó runtime, proveedor/modelo, presupuesto, límites y conexiones requeridas; el onboarding no solicita ni configura credenciales.
- [ ] Se definieron presupuesto, límite mensual y alerta de consumo fuera de la sesión del cliente.
- [ ] Se validaron con una lectura inocua sólo las integraciones ya aprovisionadas necesarias para el flujo inicial.
- [ ] Se registraron aprobadores para correo, calendario, redes, documentos y sistemas operativos.
- [ ] Se confirmó zona horaria, idioma, tono y horarios de operación.
- [ ] Se verificó que no hay conectores, memoria ni archivos de otro tenant.
- [ ] Se entregó al cliente un resumen de conexiones, permisos, pendientes y forma de revocar accesos.

## Criterio de bloqueo

Si una capacidad preaprovisionada no está disponible, se marca `bloqueado por aprovisionamiento` y se resuelve fuera de la personalidad instalada. El cliente no debe pegar API keys, tokens, contraseñas ni completar OAuth en el chat.
