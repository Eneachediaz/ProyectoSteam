# Sistema de recomendación de videojuegos para usuarios de Steam

## Descripción del Proyecto

Este proyecto se enfoca en el desarrollo de un sistema de MLOps que abarca tanto la ingeniería de datos como la implementación de modelos de aprendizaje automático.

## Contexto

Steam, la plataforma líder en venta de videojuegos, ha solicitado la creación de un sistema de recomendación de videojuegos para sus usuarios.

## Conjunto de datos

El proyecto se inicia con tres archivos proporcionados por HENRY para el análisis:
- `user_reviews.json`: Contiene comentarios de usuarios sobre juegos, junto con datos adicionales como recomendaciones, emoticones y estadísticas de utilidad.
- `users_items.json`: Contiene información sobre los juegos jugados por los usuarios y el tiempo acumulado de juego.
- `steam_games.json`: Contiene datos relacionados con los juegos, como título, desarrollador, precios, características técnicas y etiquetas.

## Objetivo

El objetivo principal es crear un flujo de trabajo eficiente que incluya la recopilación y transformación de datos, análisis exploratorio, desarrollo de modelos y su implementación utilizando prácticas de MLOps. Se simula el trabajo de un Ingeniero de MLOps combinando las funciones de Ingeniero de Datos y Científico de Datos para la plataforma Steam. Se desarrollará un Producto Mínimo Viable que incluye una API en la nube y la implementación de dos modelos de Machine Learning: análisis de sentimientos en comentarios de usuarios y recomendación de juegos basada en el nombre o las preferencias de usuario.

## Etapas del Proyecto

1. **Ingeniería de Datos (ETL)**
   - Comprensión de los archivos recibidos, identificación del formato y contenido.
   - Proceso de Extracción, Transformación y Carga (ETL) en cada archivo.

2. **Análisis Exploratorio de Datos (EDA)**
   - Identificación de variables cruciales para la creación de un modelo de recomendación efectivo.
   - Uso de Pandas para manipulación de datos y Matplotlib y Seaborn para visualización.

3. **Modelo de Aprendizaje Automático**
   - Utilización de un algoritmo basado en la memoria para el filtrado colaborativo.
   - Uso de la similitud del coseno como medida para identificar juegos similares.

4. **Implementación del Modelo**
   - Desarrollo de consultas generales y funciones del modelo de recomendación.
   - Implementación de la API utilizando FastAPI. Se proporcionan instrucciones para ejecutar la API localmente.

## Instrucciones para Ejecutar la API Localmente

- Clona el proyecto utilizando el comando: `git clone https://github.com/orestes-victor/HENRY_Proyecto_Individual_1_MLOps_Orestes_Victor.git`.
- Prepara el entorno de trabajo en Visual Studio Code:
  - Crea un entorno virtual en Python mediante: `python -m venv env`.
  - Activa el entorno virtual con: `env\Scripts\activate`.
  - Instala las dependencias del archivo `requirements.txt` mediante: `pip install -r requirements.txt`.
- Ejecuta el archivo `main.py` desde la consola activando uvicorn con: `uvicorn main:app --reload`.
- Haz clic en el enlace proporcionado en la consola para acceder a la API local.
- Para acceder a la documentación de la API, añade "/docs" al final de la URL en tu navegador (ejemplo: `http://127.0.0.1:8000/docs`).
- Dentro de cada función, haz clic en "Try it out", introduce los datos necesarios o utiliza los ejemplos predeterminados y haz clic en "Execute" para observar la respuesta en "response body".
