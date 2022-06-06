import csv

# load and save data

class Data:
    def __init__(self):
        self.fieldnames = ['Fecha', 'Kms', 'Tipo_combustible', 'Precio_lt', 'Dto_gov',
                            'Dto_fidelidad',  'Litros', 'Est._servicio','Total', 'Total_dtos']


    def load_data(self, my_list):
        with open('Data/control_consumo.csv', mode='a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            consumption_dict = {self.fieldnames[i]: my_list[i] for i in range(len(self.fieldnames))}

            writer.writerow(consumption_dict)


#
# #
# # # Initial, writeheader
# with open('control_consumo.csv', mode='w') as csv_file:
#     fieldnames = ['Fecha', 'Kms', 'Tipo_combustible', 'Litros', 'Precio_lt',
#                             'Est._servicio', 'Dto_gov', 'Dto_fidelidad', 'Total', 'Total_dtos']
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
# # #
#     writer.writeheader()
#     #writer.writerow({})





