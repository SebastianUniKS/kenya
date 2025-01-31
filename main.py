#!/usr/bin/env python3
from nicegui import Client, ui, app

from pygments import *

from leaflet import leaflet
from db import * # spatialite, getPointsDB , showPoints

from queryInfoRangeAPI import getGPSdata

from sentinelAPI import *
from uploadCropStack import *

from counter import Counter

#from weather import Weather

from climate import mouse_handler

# ui.label("Hello World")
app.add_static_files('/pics', 'pics')
app.add_static_files('/static', 'static')



locations = {
    (3.564293995225903, 38.64452830878511): 'Sololo',
    (3.035032763707658, 38.756943658838956):'Amballo',
    (1.7412757745740912, 37.31536534666663): 'Ngurunit',
    (2.322920338801376, 37.99268689194787): 'Marsabit',
    (-18.176413901509832, 20.91621324764841): 'somewhere in Namibia',
    (51.350300480813004, 9.855289171837422): 'WIZ Agrartechnik'

}

@ui.page('/')
async def main_page(client: Client):
    ui.add_body_html('<script src="static/leaflet.js"></script>')
    ui.markdown('### Should I stay or should I go?')

    with ui.row():
### weather #######################################################################################################
        #Weather()
### climate #######################################################################################################
        with ui.expansion('Marsabit climate diagram!', icon='open_with').classes('w-full'):
            with ui.card():
                src = 'https://images.climate-data.org/location/11138/climate-graph.png'
                ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown', 'mouseup'], cross=True)
            
### Map ############################################################################################################
    
    map = leaflet().props('id=InfoRangeMap').classes("w-full h-96")
    print("the map id is: ",map.id)    
        
    ui.markdown('#### Choose your location')
    selection = ui.select(locations,value= (1.7412757745740912, 37.31536534666663), on_change=lambda e: map.set_location(e.value)).classes('w-40')
    
    await client.connected()  # wait for websocket connection


### GPS Data #########################################################################################################
    
    ui.markdown('#### Query the InfoRange API')
    
    def getDate(date_value):
        ui.notify(f'You selected: {date_value}')
        startDate = date_value[:10]+" 00:00:00"
        endDate = date_value[13:24]+" 23:59:59"
        #print(startDate, "to", endDate)
        GPSdata = getGPSdata(startDate,endDate)
        ui.notify(f'Result: {GPSdata}')
        print(GPSdata)

    date_input = ui.input('Date range').classes('w-40')
    
    ui.date().props('range').bind_value(
        date_input,
        forward=lambda x: f'{x["from"]} - {x["to"]}' if x else None,
        backward=lambda x: {
            'from': x.split(' - ')[0],
            'to': x.split(' - ')[1],
        } if ' - ' in (x or '') else None,
    )
   
    ui.button('get location data', on_click=lambda: getDate(date_input.value))

    def getPoints():
        points = getPointsDB('coordinates')
        ui.notify(f'Points: {points}')
        if points:
           ui.button('Show Points', on_click=lambda: showPoints(points))


    ui.button('process points', on_click=lambda: getPoints())

#####################################################################################################################   
### DB interaction ###
    #db =  spatialite()
#####################################################################################################################
    # with ui.tabs().classes('w-full') as tabs:
    #     one = ui.tab('get Data')
    #     two = ui.tab('upload Data')
    #     three = ui.tab('Display Data')
    # with ui.tab_panels(tabs).classes('w-full'):
    #     with ui.tab_panel(one):
    # ### Query Sentinel API ###   
    #         days = 10
            
    #         ui.markdown('### Get some data..')
    #         days = ui.number(label='for the last ... days.', value=days)
    #         #print (days.value)
    #         #print(selection.value)
            
    #         ui.button('Query Sentinel API!', on_click=lambda: queryAPI (int(days.value),float(selection.value[1]),float(selection.value[0])))
    #         imageID = ui.number(label='Image ID')
            
    #         ui.button('Download!', on_click=lambda: getSatelliteData(int(imageID.value)))
    #         # ui.button('Download Sentinel Image'on_click=lambda: ui.download(downloadLink))
        
    #     with ui.tab_panel(two):
    #         #ui.upload(on_upload=lambda e: uploadAOI()).classes('max-w-full')
    #         ui.label('Upload your AreaOfInterest:')
    #         aoi = uploadAOI()
    #         ui.label('Upload Band 2,3,4,8:')
    #         satBand = uploadBand()

        # with ui.tab_panel(three):    
        #     roi = getDBdata('aoi')
        #     ui.label('Choose your AOI.')
        #     availableAOI = ui.select(roi, value = 1).classes('max-w-40')
        #     #ui.button('Display AOI ..', on_click=lambda: loadAOI(availableAOI))
        #     ui.button('test')


#####################################################################################################################
### Custom ###
    #ui.link('Checkout the custom vue component', '/counter')

    #await client.connected()  # wait for websocket connection
    #selection.set_value(next(iter(locations)))  # trigger map.set_location with first location in selection

################################################

@ui.page('/counter')
async def counter_page(client: Client):

    ui.markdown('''
    #### Try the new click counter!
    Click to increment its value.
    ''')
    with ui.card():
        counter = Counter('Clicks', on_change=lambda msg: ui.notify(f'The value changed to {msg["args"]}.'))

    ui.button('Reset', on_click=counter.reset).props('small outline')

################################################
#leaflet.set_point((51.505, -0.09))

ui.run(favicon='🚀', host="127.0.1.1")