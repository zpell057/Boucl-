from nicegui import ui
import backnd
import time
from io import BytesIO
import base64
from PIL import Image
graph = None
def get_location(): #This function was written by chatgpt but ended up being heavily modified by me
    ui.run_javascript('''
    const divWithAll = document.getElementById('c3');
    const xco = divWithAll.children[1].children[0].children[0].children[0].children[0]
    const yco = divWithAll.children[2].children[0].children[0].children[0].children[0]
    navigator.geolocation.getCurrentPosition(
        (position) => {
            xco.value = position.coords.latitude;
            yco.value = position.coords.longitude;
        },
        (error) => {
            console.error('Error occurred while getting location:', error.message);
        }
    );

    ''')

def displayGraph():
    timeNow = int(time.time())
    with open('images/image.png','rb') as img:
        imgBuffer = BytesIO(img.read())
    imgBase64 = base64.b64encode(imgBuffer.getvalue()).decode('utf-8')
    imgURL = f'data:image/png;base64,{imgBase64}'
    graph = ui.image(imgURL).style('width: 400px;position:absolute;top:0.5pc;right:3pc;')
    
def callBacknd():
    backnd.showLoopOuterCall([float(xCoords.value),float(yCoords.value)],float(distanceInput.value))
    displayGraph()
ui.add_head_html('<style>body { font-family:"consolas",sans-serif; }</style>')
distanceInput = ui.number(label='Distance of the loop: ')
xCoords = ui.number(label = 'XCoords')
yCoords = ui.number(label = 'YCoords')
ui.button('Ask for my location', on_click=get_location)
ui.button('Give me a loop !', on_click=callBacknd)
ui.run()
