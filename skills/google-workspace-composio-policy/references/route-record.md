# Registro local de ruta (estado del tenant, no payload)

Ubicación: `$HERMES_HOME/integrations/composio-google.json`. No se distribuye, no se copia entre clientes y no contiene secretos. No incluirlo en la lista `distribution_owned`. Permisos recomendados: directorio 0700, archivo 0600. Las identidades y connection IDs son metadatos privados del tenant; no publicarlos.

Formato v1 (ejemplo deliberadamente ficticio; NO constituye conexión real):

```json
{
  "schema_version": 1,
  "instance_id": "tenant-example-runtime",
  "composio_account_id": "account-example",
  "composio_project_id": "project-example",
  "google_account": "operator@example.invalid",
  "route": "connector",
  "services": {
    "drive": {
      "connection_id": "connection-example",
      "google_account": "operator@example.invalid",
      "status": "pending",
      "verified_at": null,
      "evidence_ref": "pending"
    }
  }
}
```

Rutas: `connector`, `cli`, `mcp`. Servicios: `gmail`, `calendar`, `drive`, `docs`, `sheets`, `slides`. Un servicio sólo se marca `verified_read` después de una lectura real de ese servicio bajo la conexión y cuenta aprobadas. `verified_at`: ISO 8601 con zona horaria; `evidence_ref`: identificador local de evidencia sanitizada, sin respuesta cruda, tokens o URLs OAuth. El diagnosticador exige menos de 24 horas; esto no garantiza salud ni reemplaza una nueva verificación en vivo. Omite servicios sin prueba o márcalos pending. V1 fija una cuenta Google y una ruta por instancia; múltiples cuentas requieren registros/runtime separados, nunca selección implícita.

Crear el registro es una declaración del operador basada en prueba, no un mecanismo de autenticación. El diagnosticador no impide que alguien escriba una atestación falsa: nunca tratar su código 0 como autorización ni certificación criptográfica. Evita inventar el identificador de la cuenta Composio si la ruta no lo expone: marca pendiente y pide evidencia al operador.

Aceptación de una ruta:

1. Identidad tenant y Composio confirmadas (cuenta/proyecto no equivalen a cuenta Google).
2. Identidad Google y conexión específica aprobadas, sin ambigüedad.
3. Lectura mínima real con esquema/comando vigente desde el runtime efectivo.
4. Prueba conversacional en sesión nueva y prueba negativa de acceso entre tenants.
5. Guardar evidencia sanitizada fuera del producto; conservar pendientes explícitos.

La instalación de Core no efectúa OAuth ni habilita servicios. Estado missing = pendiente, no Composio inexistente. MCP fallido con CLI autenticada = MCP fallido, no caída de la CLI. Conector funcional sin ejecutable CLI = conector funcional.
