---
name: bizbrain-operating-model
description: Use when Pandora must turn an operational request into a scoped, evidence-backed workflow with clear outputs, ownership, and next actions.
version: 1.0.0
author: Bizbrain
license: Proprietary
metadata:
  hermes:
    tags: [operations, workflows, reporting, productivity, pandora]
    related_skills: [bizbrain-onboarding, bizbrain-approvals, composio-tenant-connections]
---

# Modelo operativo de Pandora

## Overview

Convierte solicitudes imprecisas en trabajo operacional trazable. Pandora no sólo conversa: identifica resultado, fuentes, permisos, ejecución permitida y evidencia final.

## When to Use

- El cliente solicita apoyo para correo, documentos, agenda, investigación, reportes o seguimiento.
- El pedido mezcla análisis, preparación y posible ejecución externa.
- Se necesita convertir un proceso repetible en una automatización futura.

No lo uses para saltarte una política de aprobaciones o para afirmar resultados no verificados.

## Método RAPE: Resultado, Alcance, Permisos, Evidencia

1. **Resultado.** Formula el entregable observable: borrador, reporte, lista priorizada, evento preparado o acción ejecutada. Termina cuando el cliente pueda reconocer que el trabajo está concluido.
2. **Alcance.** Define fuentes, periodo, personas, sistemas y exclusiones. Si una ambigüedad altera datos o permisos, pregunta; de lo contrario usa un supuesto breve y explícito. Termina cuando el alcance sea suficiente para actuar.
3. **Permisos.** Clasifica el trabajo como lectura, preparación o ejecución. Carga `bizbrain-approvals` antes de cualquier efecto externo. Termina cuando los permisos aplicables estén claros.
4. **Evidencia.** Entrega archivos, enlaces, IDs, citas de fuente, conteos o explicación honesta de un bloqueo. Termina cuando el resultado pueda verificarse sin depender de una afirmación.

## Formatos de salida

### Reporte operativo breve

- **Resultado:** una frase.
- **Hallazgos:** máximo cinco puntos priorizados.
- **Acciones hechas:** sólo acciones verificadas.
- **Pendientes y decisiones:** responsable y siguiente paso.
- **Riesgos:** únicamente los que cambian una decisión.

### Borrador externo

- Propósito y destinatario.
- Texto listo para revisión.
- Acción pendiente: “pendiente de tu autorización para enviar/publicar/compartir”.

### Propuesta de automatización

- disparador;
- fuentes y permisos;
- transformación;
- salida/destino;
- horario y zona horaria;
- aprobaciones requeridas;
- prueba segura antes de activar.

## Common Pitfalls

1. **Empezar por la herramienta.** Define primero el resultado; la herramienta es un medio, no una religión.
2. **Sobreinvestigar.** Detente cuando la evidencia permita decidir o cumplir el entregable.
3. **Mezclar hechos con recomendaciones.** Etiqueta cada uno.
4. **Cerrar sin siguiente paso.** Si hay pendiente, asigna dueño y condición de cierre.

## Verification Checklist

- [ ] Resultado observable definido.
- [ ] Alcance y supuestos explícitos.
- [ ] Permisos y aprobaciones respetados.
- [ ] Entrega contiene evidencia real o bloqueo honesto.
- [ ] Pendientes tienen responsable y siguiente acción.
