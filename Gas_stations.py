import requests
import pandas as pd
import plotly.express as px


'''id_product from minetur.gob.es Productos Petroliferos
    Url "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/Listados/ProductosPetroliferos/"
    IDProducto      NombreProducto
            1       Gasolina 95 E5
            3       Gasolina 98 E5
            4       Gasóleo A habitual
            5       Gasóleo Premium
            17      Gases licuados del petroleo
            18      Gas natural comprimido
            19      Gas natural licuado'''


def extract_data(id_product):
    """Request data from Spain gobernment minetur, id code above"""

    url = f'https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/FiltroProducto/{id_product}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    stations = data['ListaEESSPrecio']
    return stations



def transform_data(data):

    pd.set_option('display.max_columns', None)

    stations_df = pd.DataFrame(data)
    #print(GLP_sations_df)

    # Only Venta al publico en general
    stations_df = stations_df[stations_df['Tipo Venta'] == 'P']


    # Rename Columns
    stations_df = stations_df.rename(columns={"Longitud (WGS84)": "Longitud", "PrecioProducto": "Precio"})

    # Replace comma with dot
    new_value = {'Latitud': {r',': '.'}, 'Longitud': {r',': '.'}, 'Precio': {r',': '.'}
    }

    stations_df.replace(new_value, regex=True, inplace=True)

    # Use made_func to change column data type
    astype_per_column(stations_df, 'Longitud', 'float')
    astype_per_column(stations_df, 'Latitud', 'float')
    astype_per_column(stations_df, 'Precio', 'float')

    return stations_df



def astype_per_column(df: pd.DataFrame, column: str, dtype):
    """Change data type by column"""
    df[column] = df[column].astype(dtype)



def plot_map(df):
    """Plot in map"""
    fig = px.scatter_mapbox(df, lat="Latitud", lon="Longitud", hover_name="Rótulo", hover_data=["Precio", "Dirección", "Municipio", "Horario"],
                            color_discrete_sequence=["blue"], zoom=3)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig.show()

