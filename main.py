from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import pandas as pd

app = FastAPI()

def developer(df: pd.DataFrame, desarrollador: str):
    df_filtrado = df[df['developer'] == desarrollador]

    items_free = df_filtrado[df_filtrado['price'] == 0].groupby('release_year').count()['id']

    total_items = df_filtrado.groupby('release_year').count()['id']

    resultado = pd.DataFrame({
        'total_items': total_items,
        'items_free': items_free
    }).fillna(0)

    resultado['Free_percentage'] = (resultado['items_free'] * 100) / resultado['total_items']

    return resultado

@app.get("/userdata/{desarrollador}")
async def userdata(desarrollador: str):
    try:
        # Cambia la ruta del archivo según la ubicación de tu archivo df_endpoint_1.parquet
        df = pd.read_parquet("endpoint1")

        # Aplicar la función para obtener el top de gastadores por año
        result = developer(df, desarrollador)

        return JSONResponse(content=jsonable_encoder(result.to_dict(orient="index")), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")

