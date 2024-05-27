from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import pandas as pd
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any
from sklearn.metrics.pairwise import cosine_similarity


app = FastAPI()

def developer_function(df: pd.DataFrame, desarrollador: str):
    df_filtrado = df[df['developer'] == desarrollador]

    items_free = df_filtrado[df_filtrado['price'] == 0].groupby('release_year').count()['id']

    total_items = df_filtrado.groupby('release_year').count()['id']

    resultado = pd.DataFrame({
        'total_items': total_items,
        'items_free': items_free
    }).fillna(0)

    resultado['Free_percentage'] = (resultado['items_free'] * 100) / resultado['total_items']

    return resultado

@app.get("/developer/{desarrollador}")
async def get_developer(desarrollador: str):
    try:
        # Cambia la ruta del archivo según la ubicación de tu archivo df_endpoint_1.parquet
        df = pd.read_parquet("API/endpoint1")

        # Aplicar la función para obtener el top de gastadores por año
        result = developer_function(df, desarrollador)

        return JSONResponse(content=jsonable_encoder(result.to_dict(orient="index")), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")


def userdata_function(df: pd.DataFrame, User_id: str):
    df_filtrado = df[df['user_id'] == User_id]

    # Calculate total reviews
    total_reviews = df_filtrado['recommend'].count()

    # Calculate recommended items percentage
    if total_reviews > 0:  # Avoid division by zero
        num_recomendaciones = df_filtrado[df_filtrado['recommend'] == True].shape[0]
        percent_recommendation = (num_recomendaciones * 100) / total_reviews
    else:
        percent_recommendation = 0  # Handle no reviews case

    # Calculate money spent
    Dinero_gastado = df_filtrado['price'].sum()

    # Calculate total items
    cantidad_items = df_filtrado.shape[0]

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
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")

def User_For_Genre(df: pd.DataFrame, genero: str):
    resultado = {}
    df_filtrado = df[df['genres'] == genero]
    Usuario_top = df_filtrado.groupby('user_id')['playtime_forever'].sum().idxmax()
    resultado[f'Usuario con más horas jugadas para {genero}'] = Usuario_top
    Conteo_horas = df_filtrado[df_filtrado['user_id'] == Usuario_top].groupby('release_year')['playtime_forever'].sum().to_dict()
    resultado.update(Conteo_horas)
    return resultado

@app.get('/User_For_Genre/{genero}')
async def get_User_For_Genre(genero: str):
    try:
        # Change the path according to the location of your file df_endpoint_1.parquet
        df = pd.read_parquet("API/endpoint3")

        # Apply the function to get the top user and their playtime by year for the given genre
        result = User_For_Genre(df, genero)

        return JSONResponse(content=result, media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")


def best_developer_year(df: pd.DataFrame, release_year: float):
    df_filtrado = df[df['release_year'] == release_year]
    if df_filtrado.empty:
        raise ValueError(f"No data found for the release year {release_year}")

    top_developers = df_filtrado.groupby('developer')['sentiment'].count().nlargest(3)

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
        # Change the path according to the location of your file df_endpoint_1.parquet
        df = pd.read_parquet("API/endpoint4")

        # Apply the function to get the top developers by year
        result = best_developer_year(df, release_year)

        return JSONResponse(content=result, media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")

def developer_reviews_analysis(df: pd.DataFrame, desarrolladora: str):
    print("DataFrame head:\n", df.head())  # Debug: Print the first few rows of the dataframe
    df_filtrado = df[df['developer'] == desarrolladora]
    print("Filtered DataFrame:\n", df_filtrado)  # Debug: Print the filtered dataframe

    Valor_negativo = int(df_filtrado[df_filtrado['sentiment'] == 0]['sentiment'].count())
    Valor_positivo = int(df_filtrado[df_filtrado['sentiment'] == 2]['sentiment'].count())

    print(f"Negative sentiment count: {Valor_negativo}")  # Debug: Print the count of negative sentiments
    print(f"Positive sentiment count: {Valor_positivo}")  # Debug: Print the count of positive sentiments

    resultado = {
        'developer': desarrolladora,
        'Negative': Valor_negativo,
        'Positive': Valor_positivo
    }

    return resultado

@app.get('/developer_reviews_analysis/{desarrolladora}')
async def get_developer_reviews_analysis(desarrolladora: str):
    try:
        # Change the path according to the location of your file df_endpoint_1.parquet
        df = pd.read_parquet("API/endpoint5")

        # Apply the function to get the analysis result
        result = developer_reviews_analysis(df, desarrolladora)

        return JSONResponse(content=result, media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")

def recommend_items(df:pd.DataFrame,user:str):
    pivot_table = df.pivot_table(index='user_id', columns='item_name', values='sentiment').fillna(0)
    item_similarity = cosine_similarity(pivot_table.T)
    item_similarity_df = pd.DataFrame(item_similarity, index=pivot_table.columns, columns=pivot_table.columns)
    user_ratings = pivot_table.loc[user]
    similar_scores = item_similarity_df.dot(user_ratings).div(item_similarity_df.sum(axis=1))
    recommendations = similar_scores.sort_values(ascending=False).head(5)
    return recommendations.to_dict()

@app.get('/recommend_items/{user}')
async def get_recommend_items(user: str):
    try:
        df = pd.read_parquet('API/df_Modelo')
        result = recommend_items(df, user)  # Corrected variable name
        return JSONResponse(content=result, media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")


