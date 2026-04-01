# GlucoCheck

- Miembros: Markel, Juan Carlos, Steven, Miguel Ángel

- Objetivo: Crear una app web para diagnosticar el riesgo de diabetes con un modelo de ML.

## Despliegue en producción
- Frontend (Netlify): https://remarkable-fenglisu-735967.netlify.app
- Backend (Railway): https://glucocheck-migue-production.up.railway.app

## Instrucciones de ejecución local
1. Clonar el repositorio: git clone https://github.com/MarkelRoman05/GlucoCheck
2. Crear entorno virtual: python -m venv venv
3. Activar entorno virtual (Windows): venv\Scripts\activate
4. Instalar dependencias: pip install -r requirements.txt
5. Ejecutar pipeline de datos (primera vez): python src/data/download_data.py && python src/data/preprocess.py && python src/models/train_model.py
6. Arrancar backend: uvicorn src.api.main:app --host 0.0.0.0 --port 8000
7. Abrir frontend/index.html en el navegador
