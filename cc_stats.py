import pandas as pd
import requests
import numpy as np

class DataAnalysis:

    def __init__(self):
        self.gas_df = pd.read_csv("control_consumo.csv")
        self.last_km()



    def last_km(self):
        """Get the last Km value from previous charge"""
        try:
            return self.gas_df.Kms.iloc[-1]
        except IndexError:
            return 0

    def stations_list(self):

        # Convert to function for listbox values in my GUI

        url1 = 'https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/'
        response = requests.get(url1)
        response.raise_for_status()
        data = response.json()

        # All gas stations in Spain, price for all products
        gasolineras = pd.DataFrame(data['ListaEESSPrecio'])
        stations = gasolineras['Rótulo'].str.title().value_counts()[:20]
        stations = stations.index.tolist()
        stations.append('Otra')

        return stations


    def consumption_data(self):
        # read csv file
        gas_df = pd.read_csv("Data/control_consumo.csv")

        # Change value types
        gas_df['Fecha'] = pd.to_datetime(gas_df['Fecha'])

        # Add new column with fuel name
        gas_df['Combustible'] = np.where(gas_df['Tipo_combustible']== 1, 'Gasolina 95 E5',
                                np.where(gas_df['Tipo_combustible'] ==17, 'GLP', 'Gasolina 98 E5'))

        # Consumo litros por cada 100Km
        glp_df = gas_df[gas_df['Tipo_combustible']== 17]
        glp_df = glp_df.drop(['Tipo_combustible', 'Dto_gov', 'Dto_fidelidad', 'Est._servicio', 'Total', 'Total_dtos'], axis=1)
        glp_df = glp_df.assign(Kms_btw_rec=glp_df["Kms"] - glp_df["Kms"].shift(1) )
        glp_df = glp_df.assign(lt_x_km=(glp_df['Litros']/glp_df['Kms_btw_rec']) * 100)

        # Null values = 0
        glp_df = glp_df.fillna(0)

        #pd.merge(gas_df, glp_df['Kms', 'Kms_btw_rec', 'lt_x_km'], on='Kms')
        gas_df = gas_df.merge(glp_df[['Fecha','Kms', 'Kms_btw_rec', 'lt_x_km']], on='Fecha')

        # Intervalo días y nombre día repstaje
        gas_df['time_lapse'] = gas_df['Fecha'].diff(periods=1)
        gas_df['Día'] = gas_df['Fecha'].dt.day_name()

        # Drop duplicate  column
        gas_df = gas_df.drop(['Kms_y'], axis=1)

        return gas_df
