import sqlite3
from nicegui import ui

from nicegui.element import Element

from leaflet import leaflet

conn = sqlite3.connect("app.sqlite")
cursor = conn.cursor()

name = ui.input(label="user").classes("w-full")

dataList = ui.column()

getID = ui.label()

class spatialite(Element):
# add data
    def addData():
        try:
            cursor.execute('''INSERT INTO users(name) VALUES (?)''',(name.value,))
            conn.commit()
            ui.notify(f"data saved: {name.value}", color="blue")
            name.value = ""
            dataList.clear()
            getData()
        except Exception as e:
            print ("total desaster!")
            print (e)

    ui.button("add new user",
            on_click=addData
            )
    def editData():
        pass

    def deleteData(x):
        getID.text = x.default_slot.children[0].text
        try:
            cursor.execute('''DELETE FROM users WHERE id = (?)''',(getID.text,))
            conn.commit()
            ui.notify(f"data deleted!", color="red")
            dataList.clear()
            getData()
        except Exception as e:
            print ("total desaster!")
            print (e)


def getData():
    cursor.execute('''SELECT * FROM users''')
    res = cursor.fetchall()
    result = []
    for r in res:
        data = {}
        for i,col in enumerate(cursor.description):
            data[col[0]] = r[i]
        result.append(data)
    print(result)

    for d in result:
        with dataList:
            with ui.card():
                with ui.column():
                    with ui.row().classes("justify-between w-full") as carddata:
                        ui.label(d['id'])
                        ui.label(d['name'])
                    with ui.row():
                         ui.button("edit").on("click", lambda e, carddata=carddata : editData(carddata))
                         ui.button("delete").on("click", lambda e, carddata=carddata : deleteData(carddata)).classes("bg-red")

# getData()

inforangeDB  = "./buildInDB.sqlite"


def getPointsDB(table_name):
    inforangeDB  = "./buildInDB.sqlite"
    """Fetch point data (latitude, longitude) from a SpatiaLite database."""
    connection = sqlite3.connect(inforangeDB)
    connection.enable_load_extension(True)
    connection.load_extension('mod_spatialite')
    cursor = connection.cursor()

    # Example query to retrieve point data (adjust table and column names as needed)
    query = f"SELECT ST_X(geom), ST_Y(geom), captured_at FROM {table_name} order by captured_at desc limit 100"
    cursor.execute(query)
    points = cursor.fetchall()

    connection.close()
    return points  # Returns a list of tuples: [(lon, lat, name), ...]

def showPoints(points):
     for point_lon, point_lat, created_at in points:
            ui.run_javascript(f'''
                set_point({point_lat}, {point_lon});
            ''')


ui.run()