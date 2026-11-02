---
name: bizbrain-onboarding
description: Use when a new Pandora tenant needs to be configured, connected, verified, and handed over without relying on Bizbrain staff for routine setup.
version: 1.1.0
author: Bizbrain
license: Proprietary
metadata:
  hermes:
    tags: [onboarding, tenant, composio, security, pandora]
    related_skills: [bizbrain-approvals, composio-tenant-connections, bizbrain-operating-model]
---

# Onboarding autónomo de Pandora

## Overview

Convierte una cuenta nueva en un tenant operativo sin mezclar datos, credenciales o decisiones de otros clientes. El objetivo es completar la configuración con conexiones propias del cliente y dejar un resumen verificable de lo habilitado y lo que requiere decisión.

El operador prepara el runtime, proveedor de modelo, presupuesto y controles técnicos **antes** de la sesión. El cliente no proporciona ni pega credenciales de LLM en el chat.

## When to Use

- Un cliente inicia Pandora por primera vez.
- Se agrega una integración o responsable operativo.
- Se reinstala o migra un tenant.

No lo uses para asumir permisos, copiar credenciales de otro perfil ni activar automatizaciones no solicitadas.

## Flujo

1. **Identifica al tenant.** Pide empresa, responsable operativo, administradores autorizados, zona horaria, idioma y objetivo principal. Termina cuando cada dato esencial esté confirmado o marcado como pendiente.
2. **Provisiona desde la plantilla maestra.** El operador debe clonar el modelo aprobado de Pandora, no construir uno nuevo de memoria. Verifica que la política persistente también exista en el SOUL/perfil Hermes y que obligue a usar Composio para los servicios definidos sin exigir que el usuario repita instrucciones técnicas. Confirma que el proveedor/modelo responde a una consulta inocua y que el presupuesto y límite de consumo están configurados fuera de la sesión del cliente. Si falla, marca `bloqueado por configuración operativa`; no solicites API keys, tokens, contraseñas ni credenciales de LLM al cliente.
3. **Conecta aplicaciones por necesidad.** Para cada flujo priorizado, explica el acceso mínimo requerido, dirige al cliente al flujo oficial de autorización y verifica con una lectura inocua. Termina cuando cada conexión esté marcada como verificada, pendiente o rechazada.
4. **Define aprobaciones.** Pregunta quién puede autorizar correo, calendario, documentos compartidos, redes sociales y cambios a sistemas operativos. Si no hay respuesta, conserva la regla de aprobación explícita por operación.
5. **Aplica acceso mínimo en la interfaz.** En Open WebUI o la interfaz equivalente, asigna al usuario sólo su modelo amigable, perfil Hermes, conexiones e integraciones necesarias. Oculta identificadores técnicos y modelos base; no concedas herramientas, conocimiento o perfiles ajenos. Verifica el acceso efectivo con la vista del usuario, no sólo desde la cuenta administradora.
6. **Verifica aislamiento.** Confirma que no se usa una credencial, archivo, memoria ni conector de otro tenant. Termina cuando las pruebas se limiten al tenant actual.
7. **Prueba el recorrido real del usuario.** Desde una sesión limpia o incógnita, inicia sesión como el usuario, abre una conversación nueva y formula la solicitud funcional sin mencionar Composio ni repetir instrucciones técnicas. Cierra sesión, vuelve a entrar y repite una lectura mínima. El onboarding sólo pasa si selecciona automáticamente la ruta autorizada, usa la identidad correcta, no muestra modelos técnicos y entrega un resultado real. Una generación vacía, pendiente indefinidamente o que sólo funciona en la sesión del administrador es un fallo.
8. **Entrega el handoff y registro.** Mantén una ficha sin secretos por usuario con tenant, modelo visible, perfil Hermes, identidad/connection IDs de Composio, servicios y permisos habilitados, fecha y resultado de las pruebas limpia y de reingreso, pendientes, responsables y forma de revocar. Usa `docs/onboarding-user-record.md` como formato mínimo. Termina cuando el cliente pueda corregir el resumen y aprobar el siguiente paso.

## Evidencia mínima

No declares una integración como lista solo porque apareció un formulario de OAuth. Registra una evidencia inocua y específica: lista de calendarios, metadatos de Drive, encabezados de correo, información de cuenta o equivalente permitido por el cliente.

## Common Pitfalls

1. **Pedir secretos por chat.** Indica el flujo oficial de autorización; nunca solicites tokens, API keys o contraseñas en mensajes.
2. **Hacer que el cliente configure el modelo.** El proveedor/modelo y su facturación son una responsabilidad operativa previa; el onboarding valida disponibilidad, no recoge credenciales.
3. **Conectar todo desde el inicio.** Prioriza el permiso mínimo que habilite el primer flujo de valor.
4. **Confundir autorización de lectura con ejecución.** Declara el alcance real y conserva aprobación explícita para cambios.
5. **Duplicar Google Workspace.** Carga `google-workspace-composio-policy`; conserva la ruta Composio verificada (conector, CLI o MCP). `composio_google` es preferido sólo para MCP. No reautorices por un fallo de otra ruta.
6. **Dar por terminado el alta desde la cuenta administradora.** La visibilidad del modelo y las conexiones deben probarse con el usuario final en una sesión limpia y después de reingresar.
7. **Depender de un prompt adicional.** Las reglas de herramientas pertenecen a la plantilla y al SOUL; el usuario debe poder pedir el resultado de negocio directamente.

## Verification Checklist

- [ ] Identidad, objetivo, zona horaria y responsables definidos o marcados como pendientes.
- [ ] Runtime, proveedor/modelo y presupuesto preparados por el operador o bloqueo documentado.
- [ ] Modelo clonado de la plantilla maestra y política equivalente persistente en el SOUL/perfil Hermes.
- [ ] Cada conexión tiene dueño, alcance y prueba inocua.
- [ ] Política de aprobación registrada.
- [ ] El usuario sólo ve su modelo amigable y los recursos mínimos asignados; no ve modelos técnicos/base.
- [ ] No se reutilizó una credencial ni dato de otro tenant.
- [ ] Solicitud funcional completada en conversación nueva sin mencionar Composio ni instrucciones técnicas.
- [ ] Cierre de sesión, reingreso y segunda lectura mínima completados con la identidad correcta.
- [ ] Ficha de onboarding por usuario registrada sin secretos y entregada con pendientes y revocación.
