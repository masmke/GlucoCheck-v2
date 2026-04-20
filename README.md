# GlucoCheck

- Miembros: Markel, Juan Carlos, Steven, Miguel Ángel

- Objetivo: Crear una app web para diagnosticar el riesgo de diabetes con un modelo de ML.

## Arranque rápido

> Levanta todo el proyecto con un solo comando (entorno virtual, dependencias, pipeline y backend).

### Con Docker (recomendado)

```bash
docker-compose up --build
```

- Backend: http://localhost:8000  
- Frontend: http://localhost:3000  
- Documentación API: http://localhost:8000/docs

> El pipeline de datos (descarga, preprocesamiento y entrenamiento del modelo) se ejecuta automáticamente dentro del contenedor si los artefactos no existen. Los artefactos se persisten en `data/processed/` mediante un volumen Docker.

### Mac / Linux

```bash
bash scripts/start.sh
```

### Windows

```bat
scripts\start.bat
```

### Con Make

```bash
make all
```

Otros comandos disponibles:

```bash
make install   # Crea el venv e instala dependencias
make pipeline  # Ejecuta el pipeline de datos (descarga → preproceso → entrenamiento)
make run       # Arranca el backend en http://localhost:8000
make clean     # Elimina el venv y los artefactos generados
```

---

## Despliegue en producción
- Frontend (Netlify): https://remarkable-fenglisu-735967.netlify.app
- Backend (Railway): https://glucocheck-migue-production.up.railway.app

## Instrucciones de ejecución local (manual)
1. Clonar el repositorio: git clone https://github.com/MarkelRoman05/GlucoCheck
2. Crear entorno virtual: python -m venv venv
3. Activar entorno virtual (Windows): venv\Scripts\activate
4. Instalar dependencias: pip install -r requirements.txt
5. Ejecutar pipeline de datos (primera vez): python src/data/download_data.py && python src/data/preprocess.py && python src/models/train_model.py
6. Arrancar backend: uvicorn src.api.main:app --host 0.0.0.0 --port 8000
7. Abrir frontend/index.html en el navegador
