# Proceso de lanzamiento

## Antes de publicar

1. Trabaja en una copia de desarrollo, nunca en un perfil de cliente.
2. Revisa cada skill nueva o modificada con SkillSpector estático.
3. Ejecuta validación YAML, revisión de secretos e instalación local efímera.
4. Revisa que no haya credenciales, memoria, sesiones, archivos de cliente ni cron jobs no autorizados.
5. Actualiza `distribution.yaml`, este changelog y la documentación afectada.

## Publicación

1. Incrementa la versión semántica en `distribution.yaml`.
2. Crea un commit con resumen del cambio.
3. Etiqueta la versión Git, por ejemplo `v1.1.0`.
4. Publica a un repositorio privado de Bizbrain.
5. Actualiza tenants piloto antes del despliegue general.

## Actualización de tenants

- Ejecuta `hermes profile update <tenant>` para actualizar contenido de distribución.
- No uses `--force-config` salvo que el cambio requiera reemplazar la configuración y el impacto haya sido revisado.
- Documenta la versión instalada por tenant y cualquier migración manual.

## Reversión

Vuelve a una etiqueta Git anterior y reinstala o actualiza de forma controlada. No elimines memoria, sesiones ni credenciales del cliente como parte de una reversión de distribución.
