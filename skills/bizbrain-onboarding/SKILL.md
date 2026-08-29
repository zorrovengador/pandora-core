---
name: bizbrain-onboarding
description: Use when a pre-provisioned Pandora tenant needs validation, scope definition, and handoff without requesting credentials.
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

Valida que un tenant ya aprovisionado sea operativo sin mezclar datos, credenciales o decisiones de otros clientes. El onboarding define objetivo, responsables, aprobaciones y límites de las capacidades disponibles; no configura runtime, modelos, OAuth ni secretos.

El operador prepara el runtime, proveedor de modelo, presupuesto y controles técnicos **antes** de la sesión. El cliente no proporciona ni pega credenciales de LLM en el chat.

## When to Use

- Un cliente inicia Pandora por primera vez.
- Se agrega una integración o responsable operativo.
- Se reinstala o migra un tenant.

No lo uses para asumir permisos, copiar credenciales de otro perfil ni activar automatizaciones no solicitadas.

## Flujo

1. **Identifica al tenant.** Pide empresa, responsable operativo, administradores autorizados, zona horaria, idioma y objetivo principal. Termina cuando cada dato esencial esté confirmado o marcado como pendiente.
2. **Define el alcance inicial.** Pide los tres flujos que más valor generarán en los próximos 30 días. Clasifica cada uno como lectura, preparación o ejecución. Termina cuando el cliente priorice un primer flujo verificable.
3. **Verifica capacidades preaprovisionadas.** Confirma con una consulta inocua que el proveedor/modelo, presupuesto, límites y conectores declarados para el tenant responden. Si algo falta o falla, marca `bloqueado por aprovisionamiento`; no solicites ni configures API keys, tokens, contraseñas, OAuth o credenciales de LLM.
4. **Delimita integraciones disponibles.** Para cada flujo priorizado, valida la conexión ya aprovisionada con una lectura inocua y registra su alcance. Si la conexión no existe, marca el flujo como pendiente de aprovisionamiento externo; no dirijas OAuth ni pidas autorización/secretos durante el onboarding.
5. **Define aprobaciones.** Pregunta quién puede autorizar correo, calendario, documentos compartidos, redes sociales y cambios a sistemas operativos. Si no hay respuesta, conserva la regla de aprobación explícita por operación.
6. **Verifica aislamiento.** Confirma que no se usa una credencial, archivo, memoria ni conector de otro tenant. Termina cuando las pruebas se limiten al tenant actual.
7. **Entrega el handoff.** Resume objetivo, modelo habilitado por el operador, conexiones verificadas, permisos, responsables, pendientes y primer flujo recomendado. Termina cuando el cliente pueda corregir el resumen y aprobar el siguiente paso.

## Evidencia mínima

No declares una integración como lista solo porque apareció un formulario de OAuth. Registra una evidencia inocua y específica: lista de calendarios, metadatos de Drive, encabezados de correo, información de cuenta o equivalente permitido por el cliente.

## Common Pitfalls

1. **Pedir, capturar o configurar secretos.** El aprovisionamiento ocurre antes de instalar la personalidad y las skills; durante el onboarding sólo se verifica disponibilidad.
2. **Hacer que el cliente configure el modelo.** El proveedor/modelo y su facturación son una responsabilidad operativa previa; el onboarding valida disponibilidad, no recoge credenciales.
3. **Iniciar OAuth desde el onboarding.** Si falta una conexión, documenta el bloqueo de aprovisionamiento; no conviertas la conversación en flujo de conexión.
4. **Confundir autorización de lectura con ejecución.** Declara el alcance real y conserva aprobación explícita para cambios.
5. **Duplicar Google Workspace.** Usa `composio_google` y evita conexiones equivalentes por otro router.

## Verification Checklist

- [ ] Identidad, objetivo, zona horaria y responsables definidos o marcados como pendientes.
- [ ] Runtime, proveedor/modelo y presupuesto preparados por el operador o bloqueo documentado.
- [ ] Cada conexión tiene dueño, alcance y prueba inocua.
- [ ] Política de aprobación registrada.
- [ ] No se reutilizó una credencial ni dato de otro tenant.
- [ ] El cliente recibió resumen de configuración y pendientes.
