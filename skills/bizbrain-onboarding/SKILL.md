---
name: bizbrain-onboarding
description: Use when a new Pandora tenant needs to be configured, connected, verified, and handed over without relying on Bizbrain staff for routine setup.
version: 1.0.0
author: Bizbrain
license: Proprietary
metadata:
  hermes:
    tags: [onboarding, tenant, composio, security, pandora]
    related_skills: [bizbrain-approvals, composio-tenant-connections, bizbrain-operating-model]
---

# Onboarding autónomo de Pandora

## Overview

Convierte una cuenta nueva en un tenant operativo sin mezclar datos, credenciales o decisiones de otros clientes. La meta es completar la configuración con conexiones propias del cliente y dejar un resumen verificable de lo que quedó habilitado y de lo que requiere decisión.

## When to Use

- Un cliente inicia Pandora por primera vez.
- Se agrega una integración o responsable operativo relevante.
- Se reinstala o migra un tenant.

No lo uses para asumir permisos, copiar credenciales de otro perfil ni activar automatizaciones no solicitadas.

## Flujo

1. **Identifica al tenant.** Pide empresa, responsable operativo, administradores autorizados, zona horaria, idioma y objetivo principal. Termina cuando cada dato esencial esté confirmado o marcado como pendiente.
2. **Define el alcance inicial.** Pide los tres flujos que más valor generarían en los próximos 30 días. Clasifica cada uno como lectura, preparación o ejecución. Termina cuando el cliente priorice un primer flujo verificable.
3. **Configura el modelo del cliente.** Explica que el estándar es una cuenta/proyecto de IA y presupuesto propiedad del cliente. Solicita que configure sus propias credenciales mediante el flujo de Hermes. No pidas que comparta tokens en el chat. Termina cuando el modelo responda a una consulta inocua o se documente el bloqueo real.
4. **Conecta aplicaciones por necesidad.** Para cada flujo priorizado, explica el acceso mínimo requerido, solicita la autorización del propietario y verifica con una lectura inocua. Para Google Workspace utiliza `composio_google` como router canónico; no dupliques esa conexión mediante un router general. Termina cuando cada conexión se marque como verificada, pendiente o rechazada.
5. **Define aprobaciones.** Pregunta quién puede autorizar correo, calendario, documentos compartidos, redes sociales y cambios a sistemas operativos. Si no hay respuesta, conserva la regla de aprobación explícita por operación. Termina cuando exista una política clara o el estado conservador por defecto.
6. **Verifica aislamiento.** Confirma que no se usó una credencial, archivo, memoria ni conector de otro tenant. Termina cuando las pruebas se limiten al tenant actual.
7. **Entrega el handoff.** Resume objetivo, conexiones verificadas, permisos, responsables, pendientes y primer flujo recomendado. Termina cuando el cliente pueda corregir el resumen y aprobar el siguiente paso.

## Evidencia mínima

No declares una integración como lista sólo porque apareció un formulario de OAuth. Registra una evidencia inocua y específica: una lista de calendarios, metadatos de Drive, encabezados de correo, información de cuenta o equivalente permitido por el cliente.

## Common Pitfalls

1. **Pedir secretos por chat.** Indica el flujo oficial de autorización; nunca solicites tokens, API keys o contraseñas en mensajes.
2. **Conectar todo desde el inicio.** Prioriza el permiso mínimo que habilite el primer flujo de valor.
3. **Confundir autorización de lectura con permiso de ejecución.** Declara el alcance real y conserva aprobación explícita para cambios.
4. **Duplicar Google Workspace.** Usa `composio_google` y evita crear conexiones equivalentes por otro router.

## Verification Checklist

- [ ] Identidad, objetivo, zona horaria y responsables definidos o pendientes explícitos.
- [ ] Modelo del cliente configurado o bloqueo documentado.
- [ ] Cada conexión tiene dueño, alcance y prueba inocua.
- [ ] Política de aprobación registrada.
- [ ] No se reutilizó una credencial ni dato de otro tenant.
- [ ] Cliente recibió resumen de configuración y pendientes.
