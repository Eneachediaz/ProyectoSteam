# Sistema de Recomendación de Videojuegos para Usuarios de Steam

## Video de Presentación

[Haga clic aquí para ver el video de presentación del proyecto](https://drive.google.com/file/d/1Sgpo2EdmVq96KJ2jYXRHluM37POy0Yd_/view?usp=share_link)

## Descripción del Proyecto

Este proyecto se enfoca en desarrollar un sistema de MLOps para recomendar videojuegos en Steam, abarcando desde la ingeniería de datos hasta la implementación de un modelo de aprendizaje automático.

### Contexto

Steam, lanzada por Valve Corporation en 2003, es una plataforma de distribución digital de videojuegos con más de 325 millones de usuarios y más de 25,000 juegos. A pesar de que desde 2018 Steam restringe el acceso a estadísticas detalladas, sigue siendo una referencia clave en la industria de los videojuegos.

### Conjunto de Datos

Para este proyecto se utilizan tres archivos:

- **user_reviews.json:** Contiene comentarios de usuarios sobre juegos, con información adicional sobre recomendaciones, emoticones y estadísticas de utilidad.
- **users_items.json:** Registra los juegos jugados por los usuarios y el tiempo acumulado de juego.
- **steam_games.json:** Incluye datos sobre los juegos, como título, desarrollador, precios y características técnicas.

## Objetivo

El principal objetivo es crear un flujo de trabajo eficiente que cubra la recopilación y transformación de datos, análisis exploratorio, desarrollo de modelos y su implementación utilizando prácticas de MLOps. Se busca desarrollar un Producto Mínimo Viable (MVP) que incluya una API en la nube y un modelo de Machine Learning para recomendar juegos según las preferencias del usuario.

## Etapas del Proyecto

### 1. Ingeniería de Datos (ETL)

#### Actividades

1. **Eliminación de Columnas Irrelevantes:**
   - Se eliminan las columnas que no son relevantes para ninguno de los endpoints.

2. **Conteo de Valores Totales y Nulos:**
   - Tras la primera limpieza, se realiza un conteo de los valores totales y nulos para identificar posibles problemas en los datos.

3. **Eliminación de Valores Duplicados:**
   - Se identifican y eliminan los valores duplicados para asegurar la integridad de los datos.

4. **Revisión de Tipos de Datos:**
   - Se revisa el tipo de dato de cada columna para asegurar que sean los adecuados para el análisis y modelado.

5. **Transformación de la Columna de Precios:**
   - Se transforma a tipo numérico la columna `price` para facilitar cálculos y análisis posteriores.

### 2. Feature Engineering

#### Actividades
- **Análisis de Sentimientos:** Crear la columna `sentiment_analysis` en el dataset `user_reviews`, clasificando los comentarios como:
  - `0` si es negativo.
  - `1` si es neutral (o si no hay comentario).
  - `2` si es positivo.

### 3. Modelo de Aprendizaje Automático

#### Propuesta de Trabajo
- **Sistema de Recomendación User-Item:**
  - Utilizar filtrado colaborativo para recomendar juegos a usuarios basados en las preferencias de usuarios similares.
  - **Endpoint:** `recomendacion_usuario(id de usuario)`

### 4. Desarrollo de la API

#### Endpoints Propuestos
1. **developer(desarrollador: str):** Cantidad de items y porcentaje de contenido Free por año según desarrollador.
2. **userdata(User_id: str):** Dinero gastado, porcentaje de recomendación y cantidad de items.
3. **UserForGenre(genero: str):** Usuario con más horas jugadas para un género y acumulación de horas por año.
4. **best_developer_year(año: int):** Top 3 desarrolladores con juegos más recomendados.
5. **developer_reviews_analysis(desarrolladora: str):** Análisis de sentimientos de reseñas por desarrollador.
6. **recomendacion_usuario(id de usuario):** Recomendaciones de juegos para un usuario específico.

### 5. Despliegue

Para facilitar el despliegue de la API usando FastAPI y Render, aquí se presenta una guía rápida.

#### Guía para FastAPI y Render

Este repositorio está diseñado para ayudar a implementar proyectos en FastAPI y Render de manera eficiente.

La siguiente guía parte de tener listo el archivo `main.py` con el código de las funciones de FastAPI, las cuales buscan los datos en formato `.parquet` en la carpeta Dataset.

#### Instalar el archivo `requirements.txt`

1. Agregar el archivo `requirements.txt` a la carpeta del proyecto en Visual Studio Code.
2. En la consola de comando (terminal), ejecutar:
   ```bash
   pip install -r requirements.txt
   ```

#### Entorno Virtual

1. Abrir la consola de terminal.
2. Instalar `virtualenv`:
   ```bash
   pip install virtualenv
   ```
3. Crear un entorno virtual:
   ```bash
   virtualenv nombre_del_entorno
   ```
4. Activar el entorno virtual:
   ```bash
   nombre_del_entorno\Scripts\activate
   ```
5. Desactivar el entorno virtual:
   ```bash
   deactivate
   ```

#### FastAPI

Para iniciar el servidor de uvicorn, abrir la consola de terminal y ejecutar:
```bash
uvicorn main:app --reload
```
Para acceder al contenido de la API, utiliza la dirección [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
