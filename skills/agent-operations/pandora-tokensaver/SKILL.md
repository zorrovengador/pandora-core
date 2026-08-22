---
name: pandora-tokensaver
description: Use when reducing token cost in agentic coding workflows.
version: 1.0.0
author: Pandora
license: MIT
metadata:
  hermes:
    tags: [agents, tokens, caching, context, mcp, coding]
    related_skills: [token-efficient-agent-harnesses, hermes-agent, llm-provider-operations]
---

# Pandora TokenSaver

Optimiza costo y latencia de arneses agénticos sin eliminar evidencia, pruebas, seguridad o trazabilidad. Reúne prácticas revisadas de recuperación selectiva, caché, control de herramientas, compresión segura y medición A/B.

No cambia el estilo de respuesta: `caveman` conserva prioridad cuando está activo. No usar para generar documentos aislados o tareas sin recuperación de contexto, herramientas, sesiones repetidas o datos voluminosos: cargar esta skill podría aumentar tokens.

## When to Use

- Un arnés de programación, soporte técnico o automatización consume demasiado contexto.
- Se usan herramientas/MCPs, repositorios, logs, pruebas, documentación o subagentes.
- Hay repeticiones de instrucciones, mala tasa de caché o sesiones largas.
- Se necesita medir si una optimización reduce costo **sin** degradar resultados.

## Decisión rápida

| Señal | Acción preferida |
|---|---|
| Log, diff o respuesta de herramienta extensa | Filtrar por tarea, incluir contexto mínimo y referenciar rutas. |
| Repositorio/documentación grande | Mapa breve → búsqueda dirigida → leer solo rangos relevantes. |
| Prefijo repetido | Estabilizar instrucciones, schemas y herramientas; datos variables al final. |
| Muchas herramientas | Catálogo breve; cargar schema solo al invocarlo; desactivar integraciones fuera de alcance. |
| Sesión crece o cambia de objetivo | Compactar a un handoff verificable o iniciar sesión nueva. |
| Tarea simple/repetitiva | Modelo económico y esfuerzo bajo. |
| Riesgo, ambigüedad o cambio sensible | Modelo fuerte, pruebas acotadas y revisión humana. |

## Procedimiento

1. **Línea base.** Medir por tarea: `input_tokens`, `output_tokens`, `cached_tokens`, costo, duración, llamadas de herramienta, reintentos, pruebas y aceptación.
   - Criterio: existe una corrida A comparable antes de cambiar el arnés.

2. **Presupuesto de contexto.** Separar contenido en:
   - estable: políticas, instrucciones, schemas y referencias reutilizables;
   - bajo demanda: archivos, rangos, documentos, tickets, logs y diffs;
   - excluido: información no necesaria para la decisión actual.
   - Criterio: cada bloque voluminoso tiene razón explícita para entrar.

3. **Recuperación selectiva.** Pedir resumen/índice antes de detalle; usar filtros, paginación, límites y búsquedas específicas. Devolver errores accionables, rutas y líneas, no volcados masivos.
   - Criterio: la salida de cada herramienta es mínima pero permite reproducir o verificar el resultado.

4. **Caché saludable.** Mantener idénticos y ordenados el prefijo, herramientas y schemas. Mover tarea, IDs, timestamps, usuario y resultados dinámicos después del prefijo. Medir lecturas/escrituras de caché y no forzar caché cuando el trabajo no se repetirá.
   - Criterio: los cambios dinámicos no invalidan el prefijo reutilizable.

5. **Sesiones y subagentes.** Al cambiar de tarea, iniciar sesión nueva o compactar un handoff con objetivo, decisiones, rutas, cambios, pruebas, riesgos y pendientes. Delegar análisis voluminoso a subagentes pequeños; al hilo principal entregar solo un recibo verificable.
   - Criterio: cada subagente tiene alcance, límite y condición de cierre.

6. **Modelo proporcional.** Ruteo sugerido:
   - exploración, clasificación, extracción y formato: económico;
   - implementación común y debugging delimitado: medio;
   - arquitectura, seguridad, cambios transversales y revisión final: fuerte.
   - Criterio: el escalamiento de modelo se justifica por riesgo o complejidad, no por costumbre.

7. **Verificación A/B.** Ejecutar A y B con misma tarea, modelo, repositorio, criterio de aceptación y pruebas. Comparar medianas de 10–20 tareas cuando sea posible.
   - Ahorro de tokens: `(tokens_A − tokens_B) / tokens_A`.
   - Ahorro de costo: `(costo_A − costo_B) / costo_A`.
   - Criterio: aceptar B solo si baja consumo y no empeora pruebas, aceptación o retrabajo.

## Guardrails

- Nunca eliminar pruebas, fuentes, rutas, decisiones, errores relevantes ni aprobaciones humanas para “ahorrar”.
- No cargar skill packs extensos por defecto; una guía innecesaria también consume contexto.
- No asumir que cache hit equivale a ahorro neto: comparar lecturas, escrituras y reutilización real.
- No usar precios, modelos o porcentajes estáticos como regla operativa; consultar la tarifa y disponibilidad vigente del proveedor.
- No convertir una recomendación de ahorro en acción sobre producción sin validar permisos, seguridad y reversibilidad.

## Registro mínimo

```text
run_id, tarea, variante, modelo, input_tokens, output_tokens,
cached_tokens, cache_write_tokens, costo, duración_s, tool_calls,
reintentos, pruebas_ok, pruebas_fallidas, aceptado, defectos, notas
```

## Verificación

- [ ] Se midió una línea base comparable.
- [ ] Contexto estable y bajo demanda están separados.
- [ ] Herramientas activas y outputs están acotados.
- [ ] Caché, modelo y sesión tienen una decisión explícita.
- [ ] Pruebas, seguridad y trazabilidad se preservan.
- [ ] El resultado A/B muestra ahorro neto sin degradación de calidad.
