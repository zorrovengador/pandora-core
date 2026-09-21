---
name: pandora-budget-alerts
description: Monitor monthly provider budgets and alert safely.
version: 0.1.0
author: Manuel Hernández (zorrovengador), Hermes Agent
license: Proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [budget, alerts, openrouter, nous, operations, pandora]
    related_skills: [bizbrain-approvals, composio-tenant-connections]
---

# Alertas de presupuesto Pandora

Controla el gasto mensual por tenant y avisa al responsable cuando cruza umbrales acordados. El monitor no sustituye el límite duro del proveedor y nunca guarda ni imprime API keys.

## When to Use

- Se despliega una Pandora comercial con proveedor facturable.
- El cliente o Bizbrain define una cuota mensual.
- Se requieren alertas por Telegram y correo a un responsable autorizado.

No lo uses para estimar una factura como si fuera dato del proveedor ni para compartir una clave entre tenants.

## Prerequisites

- Un perfil Hermes aislado por tenant.
- `config/budget_alerts.json` creado desde `templates/budget_alerts.json`.
- Para OpenRouter, `OPENROUTER_API_KEY` en el entorno seguro del tenant y un límite duro configurado en OpenRouter.
- Para correo, Gmail conectado exclusivamente mediante Composio y autorización explícita del destinatario de alertas.

## Procedure

1. Copia `templates/budget_alerts.json` al directorio `config/` del perfil y define presupuesto, umbrales y correo. Termina cuando los valores sean específicos del tenant.
2. Copia `scripts/monitor_pandora_budget.py` al directorio `scripts/` del perfil. Ejecútalo con `terminal` y confirma que escribe `reports/budget/latest.json` sin exponer secretos.
3. Crea un cron horario con `monitor` apuntando al script. El monitor debe imprimir sólo periodo, proveedor, estado y banda; así el agente sólo despierta cuando cambia de umbral.
4. En el prompt del cron, autoriza el envío sólo si la banda aumenta a 50, 80, 90 o 100. Envía correo exclusivamente mediante Composio, verifica `SENT` y entrega la misma alerta por Telegram.
5. Fija el cron a un modelo/proveedor explícitos y verifica `enabled`, `next_run_at` y una primera corrida segura.

## Provider Rules

- **OpenRouter:** usa `usage_monthly` de la API de la key; es la fuente exacta del monitor. Configura además un crédito máximo mensual por key para bloquear gasto excedente.
- **Nous Portal:** usa sólo una estimación local de Hermes si no hay fuente facturable documentada. Etiqueta siempre la alerta como estimación y concíliala contra Portal antes de cobrar.
- **Otros proveedores:** no alertes hasta integrar una fuente de consumo verificable.

## Pitfalls

- No uses `hermes insights` como factura: puede omitir auxiliares, reintentos, fallbacks o cargos del proveedor.
- No ejecutes un agente cada hora si la banda no cambió; usa el gate `monitor` para contener consumo.
- No envíes alertas cuando el proveedor esté inactivo, no disponible o el periodo se reinicie.
- No crees claves OpenRouter sin límite duro mensual.

## Verification

- [ ] El archivo de estado muestra proveedor, presupuesto, gasto, porcentaje, banda y fuente.
- [ ] Una banda estable no despierta al agente en el cron.
- [ ] Un cruce ascendente genera una sola alerta por Telegram y un correo `SENT` verificado.
- [ ] Ningún secreto aparece en logs, reportes ni entregas.
- [ ] El límite duro del proveedor coincide con el presupuesto comercial del tenant.
