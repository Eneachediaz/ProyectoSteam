#Se utiliza FastAPI para montar la API y HTTPException para imprimir las excepciones al manipular los endpoints
from fastapi import FastAPI, HTTPException
#Se utiliza JSONResponse para formatear la respuesta como endpoints de JSON
from fastapi.responses import JSONResponse
#jsonable_encoder es utilizado para convertir los DataFrames en objetos JSON
from fastapi.encoders import jsonable_encoder
#Pandas para la manipulación de datos
import pandas as pd
#Para el modelo de recomendación
from sklearn.metrics.pairwise import cosine_similarity

#Se instancia un objeto API
app = FastAPI()

def developer_function(df: pd.DataFrame, desarrollador: str):
    '''
    Imprime la cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.
    '''
    #Se filtra en DataFrame para solo utilizar datos relevantes para la entrada
    df_filtrado = df[df['developer'] == desarrollador]
    #Se cuenta el número de juegos cuyo precio es 0 agrupándolos por año
    items_free = df_filtrado[df_filtrado['price'] == 0].groupby('release_year').count()['id']
    #Se cuenta el número total de juegos a grupándolos por año
    total_items = df_filtrado.groupby('release_year').count()['id']
    #Se agrupan ambos valores en un diccionario que será el resultado
    resultado = pd.DataFrame({
        'total_items': total_items,
        'items_free': items_free
    }).fillna(0)
    #Se agrega una nueva entrada al diccionario que 
    resultado['Free_percentage'] = (resultado['items_free'] * 100) / resultado['total_items']
    return resultado

@app.get("/developer/{desarrollador}")
async def get_developer(desarrollador: str):
    try:
        #Se lee el archivo correspondiente al endpoint y se guardan los datos en un DataFrame
        df = pd.read_parquet("API/endpoint1")
        #Se aplica la función
        result = developer_function(df, desarrollador)
        return JSONResponse(content=jsonable_encoder(result.to_dict(orient="index")), media_type="application/json")
    #Se utiliza FileNotFoundError y Exception para el manejo de erroes
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")


def userdata_function(df: pd.DataFrame, User_id: str):
    '''
    Devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.
    '''
    #Se filtra en DataFrame para solo utilizar datos relevantes para la entrada
    df_filtrado = df[df['user_id'] == User_id]
    #Se cuenta el número de reseñas
    total_reviews = df_filtrado['recommend'].count()
    #Se confirma que el número de reseñas sea mayor a 0. Así se evita dividir en 0. Luego se calcula el porcentaje de recomendación.
    if total_reviews > 0:  #
        num_recomendaciones = df_filtrado[df_filtrado['recommend'] == True].shape[0]
        percent_recommendation = (num_recomendaciones * 100) / total_reviews
    else:
        #Si el número de reseñas es 0, el número de recomendaciones también lo es.
        percent_recommendation = 0  #
    #Se guarda en la variable Dinero_gastado la sumatoria del precio de los items que posee el usuario
    Dinero_gastado = df_filtrado['price'].sum()
    #Se cuentan la cantidad de items
    cantidad_items = df_filtrado.shape[0]
    #Se compila toda la información en un diccionario
    retorno = {
        "Usuario": User_id,
        "Dinero gastado": Dinero_gastado,
        "% de recomendación": f"{percent_recommendation:.2f}%",
        "cantidad de items": cantidad_items
    }
    return retorno

@app.get("/userdata/{User_id}")
async def get_userdata(User_id: str):
    try:
        # Cambia la ruta del archivo según la ubicación de tu archivo df_endpoint_1.parquet
        df = pd.read_parquet("/Users/nicolashernandez/Desktop/Programación/PI MLOps - STEAM/API/endpoint2")

        # Aplicar la función para obtener el top de gastadores por año
        result = userdata_function(df, User_id)
        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    #Se utiliza FileNotFoundError y Exception para el manejo de erroes
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")

def User_For_Genre(df: pd.DataFrame, genero: str):
    '''
    Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento. el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.
    '''
    #Se inicializa un diccionario vacio
    resultado = {}
    #Se filtra en DataFrame para solo utilizar datos relevantes para la entrada
    df_filtrado = df[df['genres'] == genero]
    #Se suma el tiempo de juego agrupándolo de acuerdo con el usuario
    Usuario_top = df_filtrado.groupby('user_id')['playtime_forever'].sum().idxmax()
    #Se asigna el usuario con más horas de juego a una clave valor en el diccionario.
    resultado[f'Usuario con más horas jugadas para {genero}'] = Usuario_top
    #Se asignan claves valor al diccionario que contienen el numero de horas jugadas según el año de salida de los juegos
    Conteo_horas = df_filtrado[df_filtrado['user_id'] == Usuario_top].groupby('release_year')['playtime_forever'].sum().to_dict()
    resultado.update(Conteo_horas)
    return resultado

@app.get('/User_For_Genre/{genero}')
async def get_User_For_Genre(genero: str):
    try:
        #Se lee el archivo correspondiente al endpoint y se guardan los datos en un DataFrame
        df = pd.read_parquet("API/endpoint3")

        #
        result = User_For_Genre(df, genero)
        return JSONResponse(content=result, media_type="application/json")
    #Se utiliza FileNotFoundError y Exception para el manejo de erroes
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")


def best_developer_year(df: pd.DataFrame, release_year: float):
    '''
    Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)
    '''
    #Se filtra en DataFrame para solo utilizar datos relevantes para la entrada
    df_filtrado = df[df['release_year'] == release_year]
    #Se hace el manejo del caso en que el año solicitado no se encuentre en el DataFrame
    if df_filtrado.empty:
        raise ValueError(f"No data found for the release year {release_year}")
    #Se identifican y separan en un DataFrame los tres desarrolladores con mayor numero de recomendaciones
    top_developers = df_filtrado.groupby('developer')['sentiment'].count().nlargest(3)
    #Se organizan los tres desarrolladores en un diccionario asignándoles una clave valor según su puesto
    retorno = {
        'Para el año': release_year,
        'Puesto 1': top_developers.index[0] if len(top_developers) > 0 else None,
        'Puesto 2': top_developers.index[1] if len(top_developers) > 1 else None,
        'Puesto 3': top_developers.index[2] if len(top_developers) > 2 else None,
    }
    return retorno

@app.get("/best_developer_year/{release_year}")
async def get_best_developer_year(release_year: float):
    try:
        #Se lee el archivo correspondiente al endpoint y se guardan los datos en un DataFrame
        df = pd.read_parquet("API/endpoint4")
        #Se aplica la función
        result = best_developer_year(df, release_year)
        return JSONResponse(content=result, media_type="application/json")
    #Se utiliza FileNotFoundError y Exception para el manejo de erroes
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")

def developer_reviews_analysis(df: pd.DataFrame, desarrolladora: str):
    '''
    Según el desarrollador, devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.
    '''
    #Se filtra en DataFrame para solo utilizar datos relevantes para la entrada
    df_filtrado = df[df['developer'] == desarrolladora]
    #Se cuentan los valores positivos y los negativos para sentimiento
    Valor_negativo = int(df_filtrado[df_filtrado['sentiment'] == 0]['sentiment'].count())
    Valor_positivo = int(df_filtrado[df_filtrado['sentiment'] == 2]['sentiment'].count())
    #Se compila toda la información en un diccionario
    resultado = {
        'developer': desarrolladora,
        'Negative': Valor_negativo,
        'Positive': Valor_positivo
    }
    return resultado

@app.get('/developer_reviews_analysis/{desarrolladora}')
async def get_developer_reviews_analysis(desarrolladora: str):
    try:
        #Se lee el archivo correspondiente al endpoint y se guardan los datos en un DataFrame
        df = pd.read_parquet("API/endpoint5")
        #Se aplica la función
        result = developer_reviews_analysis(df, desarrolladora)
        return JSONResponse(content=result, media_type="application/json")
    #Se utiliza FileNotFoundError y Exception para el manejo de erroes
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")

def recommend_items(df:pd.DataFrame,user:str):
    '''
     Ingresando el id de un usuario, devuelve una lista con 5 juegos recomendados para dicho usuario.
    '''
    #Se utiliza pivot_table para crear una matriz que pueda ingresarse en el modelo de cosine_similarity
    pivot_table = df.pivot_table(index='user_id', columns='item_name', values='sentiment').fillna(0)
    #Se aplica el modelo de cosine_similarity
    user_similarity = cosine_similarity(pivot_table.T)
    #Se convierte la tabla de similaridad entre los usuarios a un DataFrame 
    user_similarity_df = pd.DataFrame(user_similarity, index=pivot_table.columns, columns=pivot_table.columns)
    #Se extraen los ratings específicos al usuario
    user_ratings = pivot_table.loc[user]
    #Se encuentran ratings parecidos en otros usuarios
    similar_scores = user_similarity_df.dot(user_ratings).div(user_similarity_df.sum(axis=1))
    #Se seleccionan los 5 elementos con mayor puntaje
    recommendations = similar_scores.sort_values(ascending=False).head(5)
    return recommendations.to_dict()

@app.get('/recommend_items/{user}')
async def get_recommend_items(user: str):
    try:
        #Se lee el archivo correspondiente al endpoint y se guardan los datos en un DataFrame
        df = pd.read_parquet('API_Datasets/df_Modelo')
        #Se aplica la función
        result = recommend_items(df, user)
        return JSONResponse(content=result, media_type="application/json")
    #Se utiliza FileNotFoundError y Exception para el manejo de erroes
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")
