---
name: memory-curation
description: Cura la memoria de Hermes y reduce contexto redundante.
version: 1.0.0
author: Manuel Hernández, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [memory, curation, compression, maintenance]
    related_skills: [pandora-tokensaver]
---

# Curación diaria de memoria

Mantén la memoria de Hermes pequeña, precisa y útil. Este proceso consolida aprendizajes reutilizables sin copiar conversaciones completas ni guardar secretos.

## When to Use

- En la rutina diaria de mantenimiento de memoria.
- Después de sesiones largas o repetitivas.
- Cuando el contexto crece sin aportar información nueva.

## No usar para

- Sustituir Gmail o Calendar como fuentes autoritativas.
- Guardar contraseñas, tokens, claves, códigos, datos bancarios o secretos.
- Mezclar personas, empresas, proyectos o clientes sin evidencia explícita.
- Borrar historial de sesiones que pueda servir como evidencia.

## Procedimiento

1. Identifica el perfil activo y usa únicamente sus rutas de memoria, sesiones y skills; no cruces perfiles o tenants.
2. Revisa los aprendizajes y conversaciones recientes disponibles para este perfil, priorizando decisiones, correcciones del usuario, preferencias estables y procedimientos repetibles.
3. Clasifica cada hallazgo:
   - **permanente:** identidad, preferencia estable o regla transversal;
   - **procedimiento:** instrucción reutilizable que pertenece a una skill;
   - **temporal:** tarea, estado o dato que debe permanecer sólo en la sesión;
   - **ambiguo:** no guardar hasta verificar contexto y pertenencia.
4. Consolida duplicados y reemplaza hechos corregidos; no agregues entradas contradictorias para “conservar todo”.
5. Mantén la memoria global breve. Si una regla aplica sólo a una tarea, herramienta, cliente o proyecto, colócala en la skill o registro correspondiente, no en la memoria global.
6. Elimina o compacta datos temporales, resúmenes redundantes y detalles que no cambien decisiones futuras. Conserva procedencia suficiente para auditar la decisión.
7. Revisa que los crones críticos sigan configurados para ejecutarse aun si cambia el modelo; no los elimines, pauses ni desancles.
8. Verifica sintaxis, límites de tamaño y que no se hayan escrito secretos. Si una edición sería ambigua o destructiva, no la hagas: repórtala como pendiente de revisión.

## Uso eficiente de tokens

- No vuelvas a resumir una sesión completa si ya existe un resumen fiable.
- Lee primero índices, metadatos y ventanas pequeñas; amplía sólo cuando haya una decisión o corrección relevante.
- Usa scripts deterministas para conteos, duplicados, tamaños y validaciones.
- Invoca un modelo sólo para clasificar o redactar una consolidación que no pueda resolverse mecánicamente.
- No generes un informe largo: entrega únicamente cambios aplicados, elementos pendientes y errores.

## Verificación

Antes de finalizar, confirma:

- memoria global sin duplicados obvios;
- correcciones reemplazadas, no duplicadas;
- secretos ausentes;
- separación de perfiles/clientes respetada;
- skills modificadas registradas;
- crones críticos presentes y habilitados;
- resultado breve, o respuesta completamente vacía si no hubo cambios y la ejecución es silenciosa.

## Resultado esperado

Devuelve sólo un resumen compacto de cambios reales. Si no hubo cambios, responde exactamente `SIN_CAMBIOS` para permitir que el cron suprima la entrega si se configura en modo silencioso.