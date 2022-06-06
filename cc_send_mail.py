from datetime import date, timedelta
import pandas as pd
import smtplib
import ssl
from email.message import EmailMessage
from cc_stats import DataAnalysis


class SendEmail:
    def __init__(self):
        self.recipients_list = ['xxxxx@hotmail.com',
                                'xxxxxxx@outlook.com']

        self.sender_credentials = {'email': 'xxxxxxx@outlook.com',
                                   'password': 'xxxxxxx'}



    def get_values(self):
        # Get date from previous month
        end_date = date.today().replace(day=1) - timedelta(days=1)
        start_date = date.today().replace(day=1) - timedelta(days=end_date.day)
        end_date = pd.to_datetime(end_date)
        start_date = pd.to_datetime(start_date)



        gas_data = DataAnalysis().consumption_data()
        df_c = gas_data.copy()
        # Replace 0 in lt_x_km with mean for mean purposes
        df_c['lt_x_km'] = df_c['lt_x_km'].replace(0,df_c['lt_x_km'].mean())
        df_c = df_c[(df_c['Fecha']>=start_date) & (df_c['Fecha']<=end_date)]

        total_km = f"{df_c.loc[df_c['Tipo_combustible'] == 17, 'Kms_btw_rec'].sum()} kms"
        avg_lt_x_km = f"{round(df_c.loc[df_c['Tipo_combustible'] == 17,'lt_x_km'].mean(), 2)}"
        total_payment = f"{round(df_c['Total'].sum(), 2)} €"
        total_pay_dto = f"{round(df_c['Total_dtos'].sum(), 2)} €"
        avg_lt_glp = f"{round(df_c.loc[df_c['Tipo_combustible'] == 17, 'Precio_lt'].mean(), 2)} €"

        avg_g95 = round(df_c.loc[df_c['Tipo_combustible'] == 1, 'Precio_lt'].mean(), 2)
        if avg_g95 > 0:
            avg_lt_g95 = f"{avg_g95} €"
        else:
             avg_lt_g95 = "Sin repostar"



        return total_km, avg_lt_x_km, total_payment, total_pay_dto, avg_lt_glp, avg_lt_g95

    def send_email__(self):
        """Send email to recipients on recipient list"""
        msg = EmailMessage()
        msg['Subject'] = f"Consumo combustible - {(date.today().replace(day=1) - timedelta(days=1)).strftime('%B %Y')}"
        msg['From'] = self.sender_credentials['email']
        msg['To'] = ', '.join(self.recipients_list)

        # add  HTML content
        msg_body = self.format_message()
        # msg.set_content(msg_body['text'])
        # msg.add_alternative(msg_body['html'], subtype='html')
        msg.set_content(msg_body['html'], subtype='html')

        # Secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP("outlook.office365.com") as server:
            server.starttls()
            server.login(self.sender_credentials['email'],
                         self.sender_credentials['password'])
            server.send_message(msg)

    def format_message(self):
        data = self.get_values()

        #########################
        ##### Generate HTML #####
        #########################
        html = f"""<html>
        <body>
        <center>
            <h1> Consumo combustible - {(date.today().replace(day=1) - timedelta(days=1)).strftime('%B %Y')}</h1>
            """

        html += f"""
            <h2>Consumo mensual Dacia Sandero Stepway: </h2> 
            <table>
                        """
        html += f"""
                <tr>
                    <td style="width: 205.77px;">&nbsp;Kms recorridos</td>
                    <td style="width: 222.23px;">&nbsp;{data[0]}</td>
                    </tr>
                <tr>
                    <td style="width: 205.77px;">&nbsp;Consumo medio Lt x 100kms</td>
                    <td style="width: 222.23px;">&nbsp;&nbsp;{data[1]}</td>
                </tr>
                <tr>
                    <td style="width: 205.77px;">&nbsp;Gasto total</td>
                    <td style="width: 222.23px;">&nbsp;&nbsp;{data[2]}</td>
                </tr>
                <tr>
                    <td style="width: 205.77px;">&nbsp;Gasto con descuentos</td>
                    <td style="width: 222.23px;">&nbsp;&nbsp;{data[3]}</td>
                </tr>
                <tr>
                    <td style="width: 205.77px;">&nbsp;Media valor litro GLP</td>
                    <td style="width: 222.23px;">&nbsp;&nbsp;{data[4]}</td>
                </tr>
                <tr>
                    <td style="width: 205.77px;">&nbsp;Media valor litro Gasolina 95</td>
                    <td style="width: 222.23px;">&nbsp;&nbsp;{data[5]}</td>
                </tr>
                            """

        html += """
                </table>
                        """


            # footer
        html += """
        </center>
            </body>
        </html>
                    """

        return {'html': html}
