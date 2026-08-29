---
name: composio-tenant-connections
description: Validate and operate pre-provisioned tenant connections.
version: 1.0.1
author: Bizbrain
license: Proprietary
metadata:
  hermes:
    tags: [composio, integrations, tenant, privacy]
    related_skills: [bizbrain-onboarding, bizbrain-approvals]
---

# Conexiones Composio preaprovisionadas por tenant

## Overview

Opera únicamente conexiones ya aprovisionadas para el tenant actual. La personalidad y las skills no solicitan, reciben, configuran ni renuevan credenciales, OAuth, tokens o API keys: validan capacidades disponibles, documentan alcance y respetan aprobaciones.

## When to Use

- Un flujo necesita Gmail, Drive, Calendar, Granola, Odoo, CRM, redes sociales u otra aplicación ya conectada.
- Se debe validar, documentar o usar una conexión existente.
- Un cliente pide saber qué puede hacer Pandora con una cuenta conectada.

No lo uses para iniciar OAuth, pedir autorización de conexión, almacenar secretos o reparar el aprovisionamiento en conversación.

## Procedimiento

1. **Confirma el flujo y alcance.** Relaciona la integración preaprovisionada con un flujo prioritario y declara el permiso mínimo esperado. Termina cuando se conozca la finalidad de la conexión.
2. **Verifica de forma inocua.** Ejecuta una consulta de lectura limitada y reporta sólo evidencia necesaria. Termina cuando haya prueba real de acceso y alcance.
3. **Documenta el límite.** Resume aplicación, dueño técnico, permiso, finalidad y fecha de verificación. Termina cuando el alcance sea revisable.
4. **Opera por aprobación.** Aunque una conexión permita escritura, aplica la skill `bizbrain-approvals` para cambios externos. Termina cuando el flujo respete las políticas del tenant.
5. **Escala un fallo de aprovisionamiento.** Si falta, vence o falla una conexión, registra `bloqueado por aprovisionamiento` con el mensaje real y el flujo afectado. No inicies OAuth ni pidas secretos; el operador la resuelve fuera de la personalidad instalada.

## Google Workspace

Para Gmail, Drive y Calendar, usa `composio_google` como router canónico ya aprovisionado para el tenant. No crees una segunda conexión equivalente mediante el router general `composio`.

## Common Pitfalls

1. **Intentar resolver credenciales desde la skill.** El aprovisionamiento ocurre antes de instalar personalidad y skills; reporta el bloqueo, no lo repares en chat.
2. **Sobredimensionar permisos.** Opera sólo dentro del alcance ya provisionado para el flujo actual.
3. **Declarar éxito sin prueba.** Una configuración declarada no sustituye una lectura inocua real.
4. **Confundir conexión con autorización de escritura.** Los cambios externos mantienen aprobación explícita.

## Verification Checklist

- [ ] Conexión preaprovisionada justificada por un flujo concreto.
- [ ] Prueba de lectura limitada completada o fallo documentado como aprovisionamiento.
- [ ] Alcance, dueño técnico y finalidad documentados.
- [ ] Google Workspace usa sólo `composio_google`.
- [ ] Acciones de escritura conservan aprobación explícita.
- [ ] No se solicitó ni configuró ninguna credencial durante la conversación.
