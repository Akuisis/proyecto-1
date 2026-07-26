# 🚀 GitHub Actions CI/CD Pipeline

Documentación para configurar y ejecutar el ML Pipeline automáticamente en GitHub.

## 📋 Tabla de Contenidos

- [Qué es GitHub Actions](#qué-es-github-actions)
- [Configuración Requerida](#configuración-requerida)
- [Workflow Disponibles](#workflow-disponibles)
- [Secrets Necesarios](#secrets-necesarios)
- [Cómo Usar](#cómo-usar)
- [Monitoreo](#monitoreo)

---

## 🤔 Qué es GitHub Actions

GitHub Actions es un sistema de **automatización de CI/CD** que permite ejecutar código automáticamente en respuesta a eventos en tu repositorio.

**Casos de Uso:**
- ✅ Ejecutar tests automáticamente
- ✅ Ejecutar linters y formateo
- ✅ Entrenar modelos automáticamente
- ✅ Generar reportes
- ✅ Desplegar cambios

---

## ⚙️ Configuración Requerida

### 1. Archivo Workflow

El archivo `.github/workflows/ml-pipeline.yml` define:
- **Cuándo** ejecutar (triggers)
- **Qué** ejecutar (jobs)
- **Dónde** ejecutar (runner)

### 2. Ubicación del Archivo

```
proyecto-1/
├── .github/
│   └── workflows/
│       └── ml-pipeline.yml    ← Archivo de configuración
└── ...
```

### 3. Ya Está Creado

✅ El archivo está en `.github/workflows/ml-pipeline.yml`

---

## 🔄 Workflow Disponibles

### Triggers (Cuándo se ejecuta)

```yaml
on:
  push:
    branches: [main, develop]      # En cada push a estas ramas
  pull_request:
    branches: [main]               # En cada PR a main
  schedule:
    - cron: '0 2 * * 0'           # Cada domingo a las 2 AM UTC
  workflow_dispatch:              # Manual desde GitHub UI
```

### Jobs (Qué se ejecuta)

| Job | Descripción | Trigger |
|-----|-------------|---------|
| **ml-pipeline** | Ejecuta el pipeline completo | Todos |
| **lint** | Verifica código (black, ruff) | Todos |

---

## 🔐 Secrets Necesarios

Para que el workflow descargue datos de Kaggle, necesitas configurar Secrets en GitHub.

### Paso 1: Obtener Credenciales

Tu Kaggle API está en `~/.kaggle/access_token` (o `kaggle.json` si es más antiguo)

### Paso 2: Agregar Secrets en GitHub

Ve a: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

**Agregar:**

1. **KAGGLE_USERNAME**
   - Valor: Tu username de Kaggle (ej: `angelcruzlasso`)

2. **KAGGLE_KEY**
   - Valor: Tu API Key de Kaggle
   - Archivo: `~/.kaggle/access_token` o `kaggle.json`

```bash
# Ver tu API key:
cat ~/.kaggle/access_token
# o
cat ~/.kaggle/kaggle.json | grep key
```

### Paso 3: Verificar en GitHub

```
Settings → Secrets and variables → Actions
  ✓ KAGGLE_USERNAME (valor oculto)
  ✓ KAGGLE_KEY (valor oculto)
```

---

## 🎯 Cómo Usar

### Opción 1: Automático (En cada Push)

```bash
git add .
git commit -m "Mi cambio"
git push origin main
# ✅ Se ejecuta automáticamente
```

### Opción 2: Manual desde GitHub UI

1. Ve a: **Actions** → **ML Pipeline - Auto Execute**
2. Click en **Run workflow**
3. Selecciona opciones:
   - `run_full: true` (con descarga de datos)
   - `run_full: false` (sin descarga)
4. Click **Run workflow**

### Opción 3: Manual desde CLI

```bash
# Requerir GitHub CLI instalado: https://cli.github.com
gh workflow run ml-pipeline.yml -f run_full=true
```

### Opción 4: Automático (Horario)

El workflow se ejecuta automáticamente:
- ✅ **Cada domingo a las 2 AM UTC** (puedes cambiar en el cron)

---

## 📊 Monitoreo

### Ver Ejecuciones

1. Ve a: **Actions** en tu repositorio
2. Selecciona: **ML Pipeline - Auto Execute**
3. Verás todas las ejecuciones con:
   - ✅ Status (exitosa/fallida)
   - ⏱️ Duración
   - 📊 Logs completos

### Estructura de Logs

```
📊 Logs Disponibles:
├── 📥 Checkout Code
├── 🐍 Setup Python
├── 📦 Install uv
├── 🛠️ Install Dependencies
├── 🔐 Setup Kaggle
├── 🚀 Execute Pipeline        ← Main step
├── 📊 Show Results
├── 📈 Upload Artifacts
└── ✅ Commit Results
```

### Descargar Resultados

1. Ve a: **Actions** → **[Latest Run]**
2. Sección: **Artifacts**
3. Download: `pipeline-results-XXXX`

Contiene:
- `logs/pipeline.log`
- `logs/metrics.json`
- `models/*.pkl`
- `data/processed/*.csv`

---

## 🔧 Configuración Avanzada

### Cambiar el Schedule

En `.github/workflows/ml-pipeline.yml`:

```yaml
schedule:
  - cron: '0 2 * * 0'  # Cada domingo 2 AM UTC
```

**Ejemplos de Cron:**

| Patrón | Descripción |
|--------|-------------|
| `0 0 * * *` | Diario a medianoche UTC |
| `0 2 * * 0` | Semanalmente domingo 2 AM |
| `0 0 1 * *` | Mensualmente día 1 a medianoche |
| `0 */6 * * *` | Cada 6 horas |

**Generador:** https://crontab.guru

### Cambiar Runner

```yaml
runs-on: ubuntu-latest  # Cambiar a:
# - ubuntu-latest
# - macos-latest
# - windows-latest
# - self-hosted (servidor propio)
```

### Agregar Notificaciones

Puedes agregar notificaciones a Slack, Discord, Email:

```yaml
- name: 💬 Slack Notification
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'ML Pipeline ${{ job.status }}'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Timeout Personalizado

```yaml
timeout-minutes: 60  # Cambiar según necesidad
```

---

## 🚨 Troubleshooting

### Error: "KAGGLE_USERNAME not found"

**Solución:**
1. Ve a Settings → Secrets and variables → Actions
2. Verifica que esté el secret `KAGGLE_USERNAME`
3. Re-run el workflow

### Error: "Kaggle dataset not found"

**Solución:**
1. Verifica que el API key esté correcto
2. Prueba localmente: `python run_pipeline.py --full`
3. Verifica credenciales en `~/.kaggle/`

### Workflow No Se Ejecuta

**Causas comunes:**
1. No hay Secrets configurados
2. El archivo `.yml` tiene errores de sintaxis
3. La rama no coincide con el trigger

**Solución:**
1. Verifica `.github/workflows/ml-pipeline.yml` sintaxis
2. Usa: https://www.yamllint.com
3. Verifica Secrets configurados

### Timeout Excedido

**Solución:**
1. Aumenta `timeout-minutes`
2. Optimiza el código (menos modelos, menos datos)
3. Usa caché: `actions/cache@v3`

---

## 📈 Casos de Uso Avanzados

### 1. Ejecutar Solo en PRs

```yaml
on:
  pull_request:
    branches: [main]
```

### 2. Ejecutar Solo en Tags (Releases)

```yaml
on:
  push:
    tags:
      - 'v*'
```

### 3. Condicionales (Run If)

```yaml
- name: Step
  if: github.event_name == 'pull_request'
  run: echo "Running on PR"
```

### 4. Matriz (Multiple Versions)

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']
    
steps:
  - uses: actions/setup-python@v4
    with:
      python-version: ${{ matrix.python-version }}
```

---

## 📚 Recursos

- 🔗 [GitHub Actions Docs](https://docs.github.com/en/actions)
- 🔗 [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- 🔗 [Marketplace](https://github.com/marketplace?type=actions)
- 🔗 [Cron Generator](https://crontab.guru)

---

## ✅ Checklist de Setup

- [ ] Archivo `.github/workflows/ml-pipeline.yml` existe
- [ ] Secret `KAGGLE_USERNAME` configurado en GitHub
- [ ] Secret `KAGGLE_KEY` configurado en GitHub
- [ ] Probaste manualmente: `python run_pipeline.py --full`
- [ ] Primer push a main ejecuta el workflow
- [ ] Workflow completó exitosamente
- [ ] Artifacts generados correctamente

---

## 🎉 ¡Listo!

Ahora tu ML Pipeline se ejecuta automáticamente en GitHub! 🚀

**Próximos pasos:**
1. Hacer push del archivo `.github/workflows/ml-pipeline.yml`
2. Ir a Settings → Secrets and variables → Actions
3. Agregar `KAGGLE_USERNAME` y `KAGGLE_KEY`
4. Hacer push a `main`
5. Ver Actions → ML Pipeline - Auto Execute

---

**Última actualización:** Jul 25, 2026  
**Versión:** 1.0.0
