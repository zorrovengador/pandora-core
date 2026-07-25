---
name: composio-tenant-connections
description: Use when configuring, verifying, documenting, or revoking a client-owned Composio connection in an isolated Pandora tenant.
version: 1.0.0
author: Bizbrain
license: Proprietary
metadata:
  hermes:
    tags: [composio, oauth, integrations, tenant, privacy]
    related_skills: [bizbrain-onboarding, bizbrain-approvals]
---

# Conexiones Composio por tenant

## Overview

Conecta aplicaciones mediante autorización del propio cliente, aplicando mínimo privilegio, prueba inocua y documentación del alcance. Una conexión pertenece al tenant actual y nunca se reutiliza entre clientes.

## When to Use

- Un flujo requiere Gmail, Drive, Calendar, Granola, Odoo, CRM, redes sociales u otra aplicación conectada.
- Se debe validar, renovar o revocar una conexión existente.
- Un cliente pide saber qué puede hacer Pandora con una cuenta conectada.

No lo uses para almacenar, copiar o pedir tokens OAuth en texto plano.

## Procedimiento

1. **Justifica el acceso.** Relaciona la conexión con un flujo prioritario y declara el alcance mínimo. Termina cuando el cliente entienda qué datos o acciones habilita.
2. **Solicita autorización del dueño.** Usa el flujo de conexión del tenant y deja que el cliente complete OAuth con su propia cuenta. Termina cuando el sistema confirme conexión activa o entregue un error real.
3. **Verifica de forma inocua.** Ejecuta una consulta de lectura limitada y reporta el resultado sin exponer contenido innecesario. Termina cuando haya evidencia de acceso y alcance.
4. **Documenta el límite.** Resume aplicación, dueño, permiso, finalidad y fecha de verificación. Termina cuando el cliente confirme o corrija la descripción.
5. **Opera por aprobación.** Aunque una conexión permita escritura, aplica la skill `bizbrain-approvals` para cambios externos. Termina cuando el flujo respete las políticas del tenant.

## Google Workspace

Para Gmail, Drive y Calendar, usa `composio_google` como router canónico del tenant. No crees una segunda conexión equivalente por el router general `composio`, pues duplica autorizaciones y dificulta la revocación.

## Revocación y fallos

Si una conexión vence, falla o el cliente cambia de personal autorizado:

- explica el mensaje de error sin inventar una causa;
- solicita reautorización al dueño correspondiente;
- confirma que la conexión anterior quedó revocada cuando el proveedor lo indique;
- vuelve a verificar con una lectura inocua.

## Common Pitfalls

1. **Pedir una clave por mensaje.** Dirige al flujo de OAuth o a un secreto administrado por el cliente.
2. **Sobredimensionar permisos.** Solicita sólo lo necesario para el flujo actual.
3. **Declarar éxito sin prueba.** Una pantalla de autorización no sustituye una lectura real.
4. **Conectar cuentas corporativas con cuentas personales equivocadas.** Pide al cliente confirmar la identidad de la cuenta antes de autorizar.

## Verification Checklist

- [ ] Conexión justificada por un flujo concreto.
- [ ] Dueño de la cuenta autorizó desde el tenant.
- [ ] Prueba de lectura limitada completada o fallo documentado.
- [ ] Alcance y finalidad explicados al cliente.
- [ ] Google Workspace usa sólo `composio_google`.
- [ ] Acciones de escritura conservan aprobación explícita.
