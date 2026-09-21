---
name: archify-lite
description: Use when creating safe self-contained technical diagrams.
version: 0.1.0
author: Manuel Hernández, Pandora
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [diagrams, architecture, workflow, HTML, SVG]
    related_skills: [frontend-design, visual-artifact-qa]
---

# Archify Lite

Crea diagramas técnicos claros en un único archivo HTML autocontenido. Es una implementación interna y acotada inspirada en el enfoque de Archify; **no es la skill oficial ni ejecuta su runtime externo**.

## Cuándo usar

- Amo pide un diagrama de arquitectura, flujo, secuencia, datos o ciclo de vida que pueda abrirse sin servidor.
- Se requiere un artefacto HTML/SVG interactivo y compartible, sin dependencias remotas.

No usar para afirmar evidencia de repositorio, revisión de cambios entre commits, despliegues o comportamiento en tiempo de ejecución si no se proporcionó esa evidencia.

## Contrato de entrada

1. Definir una pregunta operativa concreta que el diagrama responda.
2. Separar hechos observados de supuestos. Omitir nodos no confirmados.
3. Limitar la vista principal a 8–12 nodos y una ruta prioritaria.
4. Elegir un tipo: arquitectura, workflow, secuencia, flujo de datos o ciclo de vida.

## Procedimiento

1. **Modelar.** Escribir nodos con tipo, propósito y relaciones dirigidas; incluir límites de confianza o datos cuando aplique.
2. **Diseñar.** Crear jerarquía visual, leyenda mínima, etiquetas legibles y una única ruta principal. Usar color por tipo de nodo, no como adorno.
3. **Generar.** Usar `write_file` para producir un HTML con SVG inline, CSS y JavaScript locales únicamente. No incorporar frameworks, iframes, trackers, llamadas de red ni secretos.
4. **Validar.** Confirmar que el HTML tiene referencias locales únicamente, una estructura SVG válida, IDs únicos, flechas etiquetadas y texto accesible.
5. **Revisar.** Abrir el artefacto en navegador o preview, comprobar legibilidad en escritorio/móvil y probar los controles incluidos.
6. **Entregar.** Reportar el alcance, los supuestos y la ruta/archivo verificado. No llamar al resultado “validado contra el repositorio” salvo que las fuentes se hayan revisado y citado.

## Controles obligatorios

- No ejecutar procesos externos ni scripts recibidos de terceros.
- No leer credenciales, variables de entorno, archivos fuera del artefacto o directorios no autorizados.
- No borrar, mover ni sobrescribir archivos sin autorización explícita.
- Mantener todo el contenido en un único HTML portable, salvo que Amo pida otro formato.
- Aplicar `prefers-reduced-motion`; no usar animación para disfrazar incertidumbre.

## Verificación de cierre

Declarar `APROBADO` únicamente si:

- El HTML abre sin red ni dependencias externas.
- Las etiquetas, flechas y límites son legibles.
- La ruta principal coincide con el modelo declarado.
- No hay secretos, URLs remotas, formularios ni scripts de terceros.
- Las limitaciones y supuestos están visibles o se reportan junto al archivo.

En otro caso, declarar `REVISION_REQUERIDA` y describir el defecto verificable.
