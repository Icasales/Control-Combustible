
# Fuel management app

App to manage the fuel consumption of your vehicle

## Introduction

As a new car owner, and data passionate. I was incredibly curious about my car
consumption data. I was especially curious, besides the amount of money spent on fuel,
 about some potential analyses relevant to kilometers and liters. so, from the first refueling, I started to collect data, such as fuel value, total amount, and kilometers driven.

I started with the development of a graphical user interface to record the collected data in a simpler way and this led to this more complex project, still in progress.



## Features

Things you can do:
- Record data
- View service stations according to the type of fuel selected
- Display dashboard with fuel consumption analysis
- Send emails with consumption statistics





## Overview

### GUI

![gui](https://user-images.githubusercontent.com/75090602/172237308-fd7ce37e-c6c4-4227-a348-d7c0aae03889.gif)

The graphical user interface::
- Does not allow to leave empty fields
- Does not receive data of any other type than that specified
- Ask for confirmation to save data

<img src=https://user-images.githubusercontent.com/75090602/172237637-39be8507-9c01-47ce-a8a9-b6088e2a152d.png height="250"> <img src=https://user-images.githubusercontent.com/75090602/172237658-0ad13aaa-c721-4e19-af23-90604eeb8184.png height="250"> <img src=https://user-images.githubusercontent.com/75090602/172237669-26427bad-a6a6-433f-8ac8-cbb88af57f4f.jpg height="250">

### Gas Stations

Visualize fuel stations in Spain in open map.
Daily updated data extracted from the: "Ministry of Industry, Trade and Tourism; S.G. of Industry and Small and Médium Enterprises; S.E. for Trade; S.E. for Tourism; Tourism institute of Spain." [serviciosmin.es](https://sede.serviciosmin.gob.es/en-US/datosabiertos/catalogo/precios-carburantes)

The label shows:
- Fuel brand
- Price per liter current day
- Opening hours and address
- City name

![Gas stations](https://user-images.githubusercontent.com/75090602/172245852-33793688-4706-4258-bf49-8471b59b9abb.gif)


### Dashboard

Fuel consumption analysis, can be filtered by time intervals

![dash](https://user-images.githubusercontent.com/75090602/172256516-65a725df-799b-43f9-bfb1-23ec053c7a81.png)

![dash1](https://user-images.githubusercontent.com/75090602/172256955-7dfb5ffc-1f74-46db-92a7-71d56a08a49f.png)


#### Preview

![dashboard](https://user-images.githubusercontent.com/75090602/172245936-fb6af14d-0919-442a-9d93-d9f9e739a4b7.gif)


### Send Email

Send email with previous month consumption data 

<img src=https://user-images.githubusercontent.com/75090602/172246931-a35c8a4b-e51d-42c8-816e-d3ae3212f05f.jpg height="200"> 

 
  
  
## Technologies Used

Python -
- tkinter
- dash 
- plotly 
- requests
- pandas
- smtplib   

## Future Features
- Improve GUI design
- Create and configure a database user
- Host application  


## Contact

Angélica González | angelicaggon@outlook.com  
LinkedIn Profile: linkedin.com/in/angelicaggon



