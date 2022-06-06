import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from cc_getdata import Data
import Gas_stations
from cc_stats import DataAnalysis
import webbrowser
from dashboard1_0 import my_dashboard
from cc_send_mail import SendEmail

# create user interface

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('Control Combustible')
        self.config(padx=20, pady=20)
        self.canvas = tk.Canvas(width=200, height=300, highlightthickness=0)
        fuel = tk.PhotoImage(file='images/fuel.png')
        self.canvas.create_image(100, 150, image=fuel)
        self.canvas.grid(row=1, column=2, rowspan =5 ,pady=50)
        self.title_label = tk.Label(text=' \u26FD Control Combustible \u26FD',
                               font='Arial 32 normal', justify='center', padx=20, pady=20)
        self.title_label.grid(row=0, column=0, columnspan=3)

        # Choose Date
        self.date_label = tk.Label(text='Fecha de repostaje:', justify='left').grid(row=1, column=0)
        self.calendar = DateEntry(width=12, background='darkblue',
                    foreground='white', borderwidth=2)
        self.calendar.grid(row=1, column=1)

        # Km entry
        self.km_frame = tk.LabelFrame(text='Kilometros', padx=35, pady=10)
        self.km_frame.grid(row=2, column=0, columnspan=2)
        tk.Label(self.km_frame, text=f"Kms anterior repostaje: {DataAnalysis().last_km()}", justify='left').grid(row=0, column=0, columnspan=2)
        tk.Label(self.km_frame, text = "Kms al repostar: ").grid(row=1, column=0)
        self.kms = tk.Entry(self.km_frame, width=10)
        self.kms.grid(row=1, column=1)

        # Fuel type
        self.fuel_var=tk.IntVar()
        self.frame_fuel = tk.LabelFrame(text='Combustible', padx=10, pady=10)
        self.frame_fuel.grid(row=3, column=0, columnspan=2)

        tk.Radiobutton(self.frame_fuel, text='GLP', variable=self.fuel_var, value=17).grid(row=0, column=1)
        tk.Radiobutton(self.frame_fuel, text="Gasolina 95 E5", variable=self.fuel_var, value=1).grid(row=0, column=2)
        tk.Radiobutton(self.frame_fuel, text="Gasolina 98 E5", variable=self.fuel_var, value=3).grid(row=1, column=1)

        # Cost
        self.frame_cost = tk.LabelFrame(text='Precio', padx=22, pady=10)
        self.frame_cost.grid(row=4, column=0, columnspan=2)
        var_cost = tk.IntVar()
        var_cost.set(0.899)
        tk.Label(self.frame_cost, text = "Precio litro (€):").grid(row=0, column=0)
        self.spin_cost = tk.Spinbox(self.frame_cost, from_=0.700, to=2.500, width=6, increment=0.001, textvariable=var_cost)
        self.spin_cost.grid(row=0, column=1)

        # Discount
        tk.Label(self.frame_cost, text = "Descuento gov.: cts/l").grid(row=1, column=0)
        self.discount_spin1 = tk.Spinbox(self.frame_cost, from_=0.00, to=2.00, width=6, increment=0.01)
        self.discount_spin1.grid(row=1, column=1)

        tk.Label(self.frame_cost, text = "Dto. estación serv: cts/l").grid(row=2, column=0)
        self.discount_spin2 = tk.Spinbox(self.frame_cost, from_=0.00, to=2.00, width=6, increment=0.01)
        self.discount_spin2.grid(row=2, column=1)

        # Liters
        self.frame_liters = tk.LabelFrame(text='Litros', padx=50, pady=10)
        self.frame_liters.grid(row=5, column=0, columnspan=2)
        tk.Label(self.frame_liters, text="Capacidad Lt").grid(row=0, column=0)
        tk.Label(self.frame_liters, text="Litros: ").grid(row=1, column=0)
        self.liters = tk.Spinbox(self.frame_liters, from_=10.00, to=45.00, width=6, increment=0.01)
        self.liters.grid(row=1, column=1)

        # Gas station
        gas_station_frame = tk.LabelFrame(text="Estación de servicio: ", padx=50, pady=10)
        gas_station_frame.grid(row=6, column=0, columnspan=2)
        #gas_station_list = ['Alcampo', 'BP', 'Ballenoil', 'Cepsa', 'Carrefour', 'Galp', 'Repsol', 'Shell', 'Petroprix', 'Plenoil', 'otra']
        gas_station_list = DataAnalysis().stations_list()
        self.listbox = tk.Listbox(gas_station_frame, height=4)
        for item in gas_station_list:
            self.listbox.insert(gas_station_list.index(item), item)
        self.listbox.bind("<<ListboxSelect>>")
        self.listbox.grid(row=0, column=0)

        # Total Label
        self.total_label = tk.Label(text="Total :  \nTotal dto: ", font='Arial 22 bold', justify='left')
        self.total_label.grid(row=6,column=1, columnspan=2 )

        # Save frame
        save_frame = tk.LabelFrame(text='Acciones', padx=10, pady=10)
        save_frame.grid(row=10, column=0, columnspan=4)
        self.save_data(save_frame)
        gas_station = tk.Button(save_frame, text= 'Estaciones de Servicio', command=self.gas_stations_data, padx=10)
        gas_station.grid(row=0, column=1,padx=10)
        consumption = tk.Button(save_frame, text='Consumo', command=self.open_dashboard)
        consumption.grid(row=0, column=2, padx=10)
        send_email = tk.Button(save_frame, text='Enviar Correo', command=self.send_email)
        send_email.grid(row=0, column=3, padx=10)


        #set variables send email
        self.__email = SendEmail()
        self.mainloop()


    def submit_info(self):
        """Check for valid values and when all values are filled and correct, load data to csv file"""
        if len(self.kms.get()) == 0 or self.listbox.curselection() == () or self.fuel_var.get() == 0:
            messagebox.showerror(title="Campos vacios", message="Tienes uno o más campo sin rellenar.\n"
                                                                "Por favor, rellena todos los campos.")

        else:
            try:
                date = self.calendar.get_date()
                km = float(self.kms.get())
                price = float(self.spin_cost.get())
                dto1 = float(self.discount_spin1.get())
                dto2 = float(self.discount_spin2.get())
                liters = float(self.liters.get())
                cursor = self.listbox.curselection()
                gas_st = self.listbox.get(cursor)
                fuel_choice = self.fuel_var.get()
                total = price * liters
                total_dto = (price-dto1-dto2) * liters
                self.total_label.config(text=f"Total : €{total:0.2f} \nTotal dto: €{total_dto:0.2f} ")
                fuel_name = ""
                if fuel_choice == 1:
                    fuel_name = "Gasolina 95 E5"
                elif fuel_choice == 3:
                    fuel_name = "Gasolina 98 E5"
                elif fuel_choice == 17:
                    fuel_name = "GLP"



                data = [date, km, fuel_choice, price, dto1, dto2, liters, gas_st, total, total_dto]

                check_save = messagebox.askquestion('Cargar datos', f'Se grabarán los siguientes valores: \n\n Fecha: {date}\n'                                                       
                                                       f' Km: {km}\n Combustible: {fuel_name}\n '
                                                       f'Precio:{price} \n Dto gov = {dto1}\n Dto estación serv: {dto2}\n'
                                                       f' Litros: {liters}\n Estación: {gas_st}\n\n'
                                                       f'¿Quieres continuar?')
                print(check_save)
                if check_save == 'yes':
                    print(check_save)
                    x = Data()
                    x.load_data(data)
                    messagebox.showinfo('OK', 'Datos grabados')

                elif check_save == 'no':
                    messagebox.showinfo('Sin grabar', 'Datos NO grabados')


            except Exception as e:
                print(e)
                messagebox.showerror(title="Valor no valido", message="Introduce un valor númerico o decimal.")

    def save_data(self, master):
        save_button = tk.Button(master, text='Grabar', width=10, command=self.submit_info, padx=10)
        save_button.grid(row=0, column=0)

    def gas_stations_data(self):
        """Get id_product from radio Button and plot map for product prices"""
        try:
            data = Gas_stations.extract_data(self.fuel_var.get())
            stations_df = Gas_stations.transform_data(data)
            Gas_stations.plot_map(stations_df)
        except Exception as e:
            print(e)
            messagebox.showerror(title="Tipo combustible", message="Selecciona un tipo de combustible")

    def open_dashboard(self):
        # Call dash app
        self.destroy()
        my_dashboard()
        new = 1
        url = "http://127.0.0.1:8050/"
        webbrowser.open(url, new=new)


    def send_email(self):
        print('Sending email')
        self.__email.send_email__()


if __name__ == "__main__":
    app = App()
    app.mainloop()
