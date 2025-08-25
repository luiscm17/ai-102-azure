# Manual Básico de UV: Gestión de Entornos Python

## Tabla de Contenidos

- [¿Qué es UV?](#qué-es-uv)
- [Instalación](#instalación)
- [Comandos Básicos](#comandos-básicos)
- [Gestión de Entornos Virtuales](#gestión-de-entornos-virtuales)
- [Gestión de Dependencias](#gestión-de-dependencias)
- [Integración con Pip](#integración-con-pip)
- [Configuración y Personalización](#configuración-y-personalización)
- [Workflows Comunes](#workflows-comunes)
- [Migración desde Otras Herramientas](#migración-desde-otras-herramientas)
- [Solución de Problemas](#solución-de-problemas)

## ¿Qué es UV?

**UV** es un administrador de paquetes y entornos Python extremadamente rápido, escrito en Rust. Es desarrollado por Astral (creadores de Ruff) y ofrece:

- ⚡ **Velocidad superior**: 10-100x más rápido que pip
- 🐍 **Compatibilidad completa**: Reemplazo directo de pip/pip-tools/venv
- 🔧 **Una sola herramienta**: Gestiona entornos, dependencias y más
- 🌐 **Multiplataforma**: Windows, macOS, Linux

## Instalación

### Instalación en Windows

```powershell
# Usando PowerShell (recomendado)
winget install astral.uv

# O usando curl
curl -LsSf https://astral.sh/uv/install.sh | powershell -c -

# Verificar instalación
uv --version
```

### Instalación en macOS

```bash
# Usando Homebrew (recomendado)
brew install uv

# O usando curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verificar instalación
uv --version
```

### Instalación en Linux

```bash
# Usando curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# O descargar manualmente
wget https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz
tar -xzf uv-x86_64-unknown-linux-gnu.tar.gz
sudo mv uv /usr/local/bin/

# Verificar instalación
uv --version
```

### Instalación con Pip (método alternativo)

```bash
# Instalar con pip (si ya tienes Python)
pip install uv

# Actualizar uv
pip install --upgrade uv
```

## Comandos Básicos

### Verificar instalación y ayuda

```bash
# Ver versión
uv --version

# Ayuda general
uv --help

# Ayuda específica de un comando
uv run --help
uv pip --help
```

### Comandos rápidos de referencia

```bash
# Crear y activar entorno
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Instalar paquetes
uv add requests pandas numpy

# Ejecutar script en entorno temporal
uv run python script.py

# Listar paquetes instalados
uv pip list
```

## Gestión de Entornos Virtuales

### Crear entornos virtuales

```bash
# Crear entorno en directorio .venv (por defecto)
uv venv

# Crear entorno con nombre específico
uv venv mi-entorno

# Crear entorno con Python específico
uv venv --python 3.11
uv venv --python 3.12

# Forzar recreación de entorno existente
uv venv --force

# Crear entorno con permisos system (Linux/macOS)
uv venv --system
```

### Activar y usar entornos

```bash
# Activación en Linux/macOS
source .venv/bin/activate

# Activación en Windows PowerShell
.venv\Scripts\Activate.ps1

# Activación en Windows CMD
.venv\Scripts\activate.bat

# Verificar que estamos en el entorno correcto
which python   # Linux/macOS
where python   # Windows

# Desactivar entorno
deactivate
```

### Comandos útiles para entornos

```bash
# Listar entornos disponibles (no nativo, alternativa)
ls -la | grep venv  # Linux/macOS
dir *venv*          # Windows

# Eliminar entorno
rm -rf .venv        # Linux/macOS
rmdir /s .venv      # Windows

# Información del entorno
uv venv --help
```

## Gestión de Dependencias

### Instalación de paquetes

```bash
# Instalar paquetes individuales
uv add requests
uv add pandas numpy matplotlib

# Instalar con versión específica
uv add "django==4.2"
uv add "flask>=2.0,<3.0"

# Instalar desde requirements.txt
uv pip install -r requirements.txt

# Instalar con extras
uv add "requests[security]"

# Instalar en modo desarrollo (editable)
uv add -e ./mi-paquete-local
```

### Gestión de requirements.txt

```bash
# Generar requirements.txt desde paquetes instalados
uv pip freeze > requirements.txt

# Instalar desde requirements.txt
uv pip install -r requirements.txt

# Actualizar requirements.txt
uv pip install --upgrade -r requirements.txt

# Requirements con hashes para seguridad
uv pip compile requirements.in -o requirements.txt --generate-hashes
```

### Actualización y eliminación

```bash
# Actualizar paquetes
uv pip install --upgrade pandas
uv pip install --upgrade -r requirements.txt

# Actualizar todos los paquetes
uv pip list --outdated | awk '{print $1}' | xargs -n1 uv pip install --upgrade

# Eliminar paquetes
uv pip uninstall pandas
uv pip uninstall -y package1 package2  # Sin confirmación

# Listar paquetes instalados
uv pip list
uv pip list --outdated
```

### Dependencias de desarrollo

```bash
# Instalar dependencias de desarrollo
uv add --dev pytest black flake8

# Instalar desde requirements-dev.txt
uv pip install -r requirements-dev.txt

# Separar dependencias normales y de desarrollo
# requirements.txt
uv add requests pandas

# requirements-dev.txt
uv add --dev pytest coverage
```

## Integración con Pip

### UV como reemplazo de pip

```bash
# Todos los comandos de pip funcionan con uv pip
uv pip install package
uv pip uninstall package
uv pip list
uv pip freeze
uv pip show package

# Instalar desde diferentes fuentes
uv pip install git+https://github.com/user/repo.git
uv pip install https://example.com/package.tar.gz

# Instalar con constraints
uv pip install -c constraints.txt package
```

### Compatibilidad con pip existente

```bash
# UV es completamente compatible con pip
# Puedes usar archivos requirements.txt existentes
uv pip install -r requirements.txt

# Los entornos de UV son compatibles con pip tradicional
# Puedes alternar entre uv pip y pip en el mismo entorno

# Verificar compatibilidad
python -m pip list  # pip tradicional
uv pip list         # uv pip
```

### Ventajas de uv sobre pip tradicional

```bash
# Comparación de velocidad
time pip install pandas numpy matplotlib  # Lento
time uv add pandas numpy matplotlib       # Rápido

# Mejor manejo de resolución de dependencias
uv pip install complex-package  # Mejor resolución de conflictos

# Cache inteligente
uv pip install package  # Usa cache automáticamente
```

## Configuración y Personalización

### Archivo de configuración uv.toml

```toml
# uv.toml en el directorio del proyecto o ~/.config/uv/uv.toml

[install]
# Directorio por defecto para entornos
venv-dir = ".venv"

# Python version por defecto
python = "3.11"

# Configuración de cache
[cache]
dir = "~/.cache/uv"
size = "10GB"

# Configuración de red
[network]
retries = 3
timeout = 30

# Índices de paquetes personalizados
[[index]]
name = "company-index"
url = "https://pypi.company.com/simple"
priority = 1

# Source específico para un paquete
[[package-source]]
name = "private-package"
index = "company-index"
```

### Variables de entorno

```bash
# Configurar directorio de cache
export UV_CACHE_DIR="$HOME/.uv_cache"

# Configurar timeout de red
export UV_NETWORK_TIMEOUT=60

# Configurar retries
export UV_NETWORK_RETRIES=5

# Configurar Python por defecto
export UV_PYTHON="python3.11"

# Verbose logging
export UV_LOG_LEVEL="debug"

# Deshabilitar cache
export UV_CACHE_DISABLED=1
```

### Configuración del prompt

```bash
# Personalizar prompt del entorno virtual
export VIRTUAL_ENV_DISABLE_PROMPT=0  # Mostrar prompt automáticamente

# En .venv/bin/activate (Linux/macOS) puedes modificar:
# PS1="(mi-entorno) $PS1"  # Personalizar prompt

# Para PowerShell en Windows, modificar .venv/Scripts/Activate.ps1
```

## Workflows Comunes

### Workflow de desarrollo típico

```bash
# 1. Crear nuevo proyecto
mkdir mi-proyecto
cd mi-proyecto

# 2. Crear entorno virtual
uv venv

# 3. Activar entorno
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 4. Instalar dependencias
uv add requests pandas numpy
uv add --dev pytest black

# 5. Trabajar en el proyecto
uv run python mi_script.py

# 6. Congelar dependencias
uv pip freeze > requirements.txt

# 7. Desactivar entorno al terminar
deactivate
```

### Workflow colaborativo

```bash
# Clonar proyecto existente
git clone https://github.com/usuario/proyecto.git
cd proyecto

# Crear entorno con misma versión de Python
uv venv --python 3.11

# Activar entorno
source .venv/bin/activate

# Instalar dependencias
uv pip install -r requirements.txt

# Instalar dependencias de desarrollo
uv pip install -r requirements-dev.txt

# Verificar que todo funciona
uv run pytest
```

### Workflow para aplicaciones

```bash
# Para deployment o entornos controlados
uv venv --system  # Usar Python del sistema

# Instalar solo lo necesario para producción
uv pip install --no-deps -r requirements.txt

# Verificar dependencias instaladas
uv pip list

# Crear ejecutable (usando pyinstaller u otra herramienta)
uv add pyinstaller
uv run pyinstaller --onefile mi_app.py
```

### Workflow con múltiples entornos

```bash
# Desarrollar con diferentes versiones de Python
uv venv --python 3.10 --name py310
uv venv --python 3.11 --name py311

# Activar entorno específico
source py310/bin/activate  # Para Python 3.10
source py311/bin/activate  # Para Python 3.11

# Probar compatibilidad entre versiones
uv run python -c "import sys; print(sys.version)"
```

## Migración desde Otras Herramientas

### Desde venv/virtualenv + pip

```bash
# Proyecto existente con venv + pip
deactivate  # Desactivar entorno antiguo
rm -rf venv  # Eliminar entorno antiguo

# Crear nuevo entorno con uv
uv venv

# Instalar dependencias desde requirements.txt
uv pip install -r requirements.txt

# Verificar que todo funciona
source .venv/bin/activate
python -c "import requests; print('Funciona!')"
```

### Desde Poetry

```bash
# Exportar dependencias de poetry
poetry export -f requirements.txt --output requirements.txt

# Crear entorno con uv
uv venv

# Instalar dependencias
uv pip install -r requirements.txt

# Para desarrollo, exportar también dev dependencies
poetry export --dev -f requirements.txt --output requirements-dev.txt
uv pip install -r requirements-dev.txt
```

### Desde Conda/Mamba

```bash
# Exportar environment de conda
conda env export --from-history > environment.yml

# Crear requirements.txt manualmente o usar:
pip freeze > requirements.txt

# Crear entorno con uv
uv venv

# Instalar dependencias
uv pip install -r requirements.txt
```

### Desde Pipenv

```bash
# Exportar dependencias de pipenv
pipenv requirements > requirements.txt
pipenv requirements --dev > requirements-dev.txt

# Crear entorno con uv
uv venv

# Instalar dependencias
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
```

## Solución de Problemas

### Problemas comunes y soluciones

```bash
# Error: UV no encontrado
# Solución: Verificar instalación y PATH
echo $PATH  # Linux/macOS
$env:PATH   # Windows

# Error: Versión de Python no encontrada
uv venv --python 3.11  # Especificar versión exacta

# Error: Permisos denegados
sudo chmod +x /usr/local/bin/uv  # Linux/macOS

# Limpiar cache corrupto
uv cache clean

# Forzar reinstalación
uv pip install --force-reinstall package

# Ver información de debug
uv --verbose pip install package
```

### Comandos de diagnóstico

```bash
# Ver información del sistema
uv --version
uv debug info

# Ver información de cache
uv cache dir
uv cache size
uv cache list

# Limpiar cache
uv cache clean
uv cache prune  # Eliminar paquetes no usados

# Ver configuración cargada
uv config show
```

### Resolución de conflictos

```bash
# Cuando hay conflictos de dependencias
uv pip install --resolution highest package  # Forzar versión más alta
uv pip install --resolution lowest package   # Forzar versión más baja

# Usar constraints para resolver conflictos
echo "package==1.2.3" > constraints.txt
uv pip install -c constraints.txt other-package

# Ver árbol de dependencias
uv pip show --tree package
```

### Recuperación de entornos

```bash
# Si el entorno se corrompe
deactivate
rm -rf .venv
uv venv
uv pip install -r requirements.txt

# Recuperar desde backup de requirements.txt
# Siempre mantener requirements.txt actualizado

# Verificar integridad del entorno
uv pip check
```

## Consejos y Mejores Prácticas

### Flujo de trabajo recomendado

1. **Siempre usar entornos virtuales**: `uv venv` para cada proyecto
2. **Mantener requirements.txt actualizado**: `uv pip freeze > requirements.txt`
3. **Usar constraints para versiones críticas**
4. **Separar dependencias de desarrollo y producción**
5. **Versionar el requirements.txt** en control de versiones

### Performance tips

```bash
# Usar cache eficientemente
uv pip install package  # Automáticamente usa cache

# Para CI/CD, pre-cachear dependencias
uv cache dir  # Ver directorio de cache
uv cache list  # Ver paquetes en cache

# Limpiar cache regularmente
uv cache prune  # Eliminar paquetes no usados
```

### Integración con IDEs

**VS Code**: Se detecta automáticamente el entorno `.venv/`

**PyCharm**:

1. File → Settings → Project → Python Interpreter
2. Add Interpreter → Add Local Interpreter
3. Seleccionar `.venv/bin/python` (Linux/macOS) o `.venv\Scripts\python.exe` (Windows)

**Jupyter Notebooks**:

```bash
uv add ipykernel
uv run python -m ipykernel install --user --name=mi-entorno
```

### Scripts de automatización

```bash
#!/bin/bash
# setup.sh - Script de setup automático

set -e  # Salir en error

echo "Creando entorno virtual..."
uv venv

echo "Activando entorno..."
source .venv/bin/activate

echo "Instalando dependencias..."
uv pip install -r requirements.txt

if [ -f "requirements-dev.txt" ]; then
    echo "Instalando dependencias de desarrollo..."
    uv pip install -r requirements-dev.txt
fi

echo "Setup completado!"
```

Este manual cubre todo lo necesario para empezar con UV y gestionar eficientemente entornos Python. La velocidad y simplicidad de UV lo hacen ideal para desarrollo moderno de Python.
