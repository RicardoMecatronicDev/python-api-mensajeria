# python-api-mensajeria

Microservicio REST en Python (FastAPI) que recibe un mensaje y confirma que se enviará. Es la parte de **aplicación** de una prueba técnica DevOps; la infraestructura vive en [`iac-ca-mensajeria`](https://github.com/RicardoMecatronicDev/iac-ca-mensajeria).

## Probarlo

```bash
curl -X POST \
  -H "X-Parse-REST-API-Key: ${API_KEY}" \
  -H "X-JWT-KWY: ${JWT}" \
  -H "Content-Type: application/json" \
  -d '{ "message": "This is a test", "to": "Juan Perez", "from": "Rita Asturia", "timeToLifeSec": 45 }' \
  https://${HOST}/DevOps
```

| Ambiente | `${HOST}` |
|---|---|
| Producción | `apim-mensajeria-prod-01.azure-api.net` |
| Pruebas | `apim-mensajeria-noprod-01.azure-api.net` |

Respuesta esperada: `{"message":"Hello Juan Perez your message will be sent"}`. Cualquier otro método HTTP responde `ERROR` (405).

- **`${API_KEY}`**: la clave indicada en el enunciado del ejercicio.
- **`${JWT}`**: token firmado que se entrega aparte. Cada token es **de un solo uso** y dura 30 días.

## Seguridad

| Capa | Qué valida |
|---|---|
| **API Management** | Firma y caducidad del JWT (`validate-jwt`). Rechaza con 401 `ERROR` antes de llegar a la app. |
| **La app** | API Key, firma y caducidad del JWT, y que el `jti` (identificador único del token) no se haya usado antes. |

La clave de firma y la API Key no están en el código: llegan por variables de entorno desde secrets. Los tokens se generan con `scripts/gen_jwt.py` (`--count 20 --days 30`).

## Cómo se construye y se despliega

```
feature/**  ──►  develop  ──►  master
  CI            noprod          prod
```

| Workflow | Cuándo | Qué hace |
|---|---|---|
| **CI** | push a `feature/**` | Build y Test |
| **Develop** | merge a `develop` | Build, Test + SonarCloud, imagen Docker + Trivy, tag de versión, deploy a **noprod**, smoke test |
| **Release** | merge a `master` | Aprobación manual, **promoción de la misma imagen** a prod, tag de release, deploy, smoke test |
| **Deploy manual** | a demanda | Despliega el tag que se elija: sirve para el **rollback** |

- **Construir una vez, promover:** la imagen se construye solo en `develop`. En `master` no se reconstruye: se copia (`az acr import`) del ACR de noprod al de prod.
- **Versionado semántico por commits:** `fix:` sube el parche, `feat:` el menor, `feat!:` el mayor. En `develop` los tags son candidatas (`v0.1.0-rc.0`); en `master`, finales (`v0.1.0`).
- **Autenticación a Azure** por OIDC, sin contraseñas guardadas. Un ACR y una Container App por ambiente.

## Calidad

- **TDD**: 19 pruebas, **100 % de cobertura**; el pipeline falla por debajo de 90 %.
- **Análisis estático**: `ruff`, `bandit`, `pip-audit` y SonarCloud.
- **Imagen**: Trivy detiene el pipeline ante vulnerabilidades altas o críticas con arreglo disponible.

## Ejecutar en local

```bash
pip install -r requirements-dev.txt
API_KEY=cualquier-valor JWT_SECRET=un-secreto-de-al-menos-32-caracteres pytest
API_KEY=... JWT_SECRET=... uvicorn app.main:app --port 8000
```

## Limitaciones conocidas

- **Un token puede aceptarse más de una vez en producción.** La app guarda los `jti` usados en memoria de cada réplica, y prod corre con 2 o más. Un mismo token puede pasar una vez por réplica. Se comprobó en pruebas. Solución real: un almacén compartido (por ejemplo Azure Table Storage), no implementada para mantener la prueba simple.
- La API Key es la fija del enunciado.
- SonarCloud (plan gratuito) analiza solo la rama principal: el análisis de `develop` se registra como su rama principal.

## Cumplimiento del enunciado

| Requisito | Dónde |
|---|---|
| Endpoint `POST /DevOps`, otros métodos → `ERROR` | `app/main.py` y APIM |
| API Key + JWT único por transacción | `app/security.py`, APIM |
| Contenedor | `Dockerfile` (multi-stage, usuario no root) |
| Pipeline con Build y Test, dependencias | `.github/workflows` |
| `master` despliega a producción | `release.yml` |
| Ejecución bajo demanda y por versión | `manual.yml` y tags |
| Análisis estático, pruebas, cobertura | `_ci.yml` |
| Balanceador con ≥2 nodos y escalado | repo de infraestructura |
