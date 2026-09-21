---
name: bizbrain-onboarding
description: Use when a new Pandora tenant needs to be configured, connected, verified, and handed over without relying on Bizbrain staff for routine setup.
version: 1.0.1
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
2. **Verifica el runtime y el modelo preparados por el operador.** Confirma que el proveedor/modelo responde a una consulta inocua y que el presupuesto y límite de consumo están configurados fuera de la sesión del cliente. Si falla, marca `bloqueado por configuración operativa`; no solicites API keys, tokens, contraseñas ni credenciales de LLM al cliente.
3. **Conecta aplicaciones por necesidad.** Para cada flujo priorizado, explica el acceso mínimo requerido, dirige al cliente al flujo oficial de autorización y verifica con una lectura inocua. Termina cuando cada conexión esté marcada como verificada, pendiente o rechazada.
4. **Define aprobaciones.** Pregunta quién puede autorizar correo, calendario, documentos compartidos, redes sociales y cambios a sistemas operativos. Si no hay respuesta, conserva la regla de aprobación explícita por operación.
5. **Verifica aislamiento.** Confirma que no se usa una credencial, archivo, memoria ni conector de otro tenant. Termina cuando las pruebas se limiten al tenant actual.
6. **Entrega el handoff.** Resume objetivo, modelo habilitado por el operador, conexiones verificadas, permisos, responsables, pendientes y primer flujo recomendado. Termina cuando el cliente pueda corregir el resumen y aprobar el siguiente paso.

## Evidencia mínima

No declares una integración como lista solo porque apareció un formulario de OAuth. Registra una evidencia inocua y específica: lista de calendarios, metadatos de Drive, encabezados de correo, información de cuenta o equivalente permitido por el cliente.

## Common Pitfalls

1. **Pedir secretos por chat.** Indica el flujo oficial de autorización; nunca solicites tokens, API keys o contraseñas en mensajes.
2. **Hacer que el cliente configure el modelo.** El proveedor/modelo y su facturación son una responsabilidad operativa previa; el onboarding valida disponibilidad, no recoge credenciales.
3. **Conectar todo desde el inicio.** Prioriza el permiso mínimo que habilite el primer flujo de valor.
4. **Confundir autorización de lectura con ejecución.** Declara el alcance real y conserva aprobación explícita para cambios.
5. **Duplicar Google Workspace.** Usa `composio_google` y evita conexiones equivalentes por otro router.

## Verification Checklist

- [ ] Identidad, objetivo, zona horaria y responsables definidos o marcados como pendientes.
- [ ] Runtime, proveedor/modelo y presupuesto preparados por el operador o bloqueo documentado.
- [ ] Cada conexión tiene dueño, alcance y prueba inocua.
- [ ] Política de aprobación registrada.
- [ ] No se reutilizó una credencial ni dato de otro tenant.
- [ ] El cliente recibió resumen de configuración y pendientes.
