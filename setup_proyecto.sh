#!/bin/bash
# Setup inicial: education-spending-analysis
# Correr este script desde la carpeta donde quieras crear el proyecto

set -e  # corta si algo falla

PROJECT_NAME="education-spending-analysis"

echo "Creando estructura de carpetas..."
mkdir -p "$PROJECT_NAME"/{data,notebooks,output}
cd "$PROJECT_NAME"

echo "Creando entorno virtual..."
python3 -m venv venv

# En Windows (Git Bash) el venv usa Scripts/, en Linux/macOS usa bin/
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "Instalando dependencias..."
pip install --upgrade pip
pip install pandas openpyxl matplotlib

echo "Generando requirements.txt..."
pip freeze > requirements.txt

echo "Creando .gitignore..."
cat > .gitignore << 'EOF'
# Entorno virtual
venv/

# Datos crudos (no versionados)
data/

# Output intermedio (no versionado salvo entregables finales)
output/*
!output/.gitkeep

# Python
__pycache__/
*.pyc
.ipynb_checkpoints/

# OS
.DS_Store
EOF

# .gitkeep para que la carpeta output exista en git aunque esté vacía
touch output/.gitkeep

echo "Creando README.md inicial..."
cat > README.md << 'EOF'
# Education Spending Analysis

Análisis del gasto público en educación a nivel global, usando datos del
Banco Mundial / UNESCO Institute for Statistics (indicador `SE.XPD.TOTL.GD.ZS`
— Government expenditure on education, total % of GDP).

Segundo proyecto de portfolio orientado a Data Engineering, en continuidad
con [human-development-analysis](https://github.com/bambeeno/human-development-analysis).

## Stack
Python · Pandas · Matplotlib · Git

## Dataset
World Bank / UNESCO UIS — Government expenditure on education (% of GDP)
Fuente: https://data.worldbank.org/indicator/SE.XPD.TOTL.GD.ZS

## Estructura
```
education-spending-analysis/
├── data/           # CSV crudo (no versionado)
├── notebooks/      # Scripts por etapa
├── output/         # CSVs/Excel procesados (no versionados salvo entregables)
└── README.md
```

## Estado
🚧 En desarrollo
EOF

echo ""
echo "Listo. Estructura creada:"
find . -not -path './venv*' -not -path './.git*' | sort

echo ""
echo "Entorno virtual activado en esta sesión de shell."
if [ -f "venv/Scripts/activate" ]; then
    echo "Para activarlo en una sesión nueva: source venv/Scripts/activate"
else
    echo "Para activarlo en una sesión nueva: source venv/bin/activate"
fi