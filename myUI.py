from nicegui import ui
import backnd
import time
from io import BytesIO
import base64
from PIL import Image
def displayGraph():
    timeNow = int(time.time())
    with open('images/image.png','rb') as img:
        imgBuffer = BytesIO(img.read())
    imgBase64 = base64.b64encode(imgBuffer.getvalue()).decode('utf-8')
    imgURL = f'data:image/png;base64,{imgBase64}'
    ui.image(imgURL).style('width: 400px')
    
def callBacknd():
    backnd.showLoopOuterCall([float(xCoords.value),float(yCoords.value)],float(distanceInput.value))
    displayGraph()
distanceInput = ui.number(label='Distance of the loop: ')
xCoords = ui.number(label = 'XCoords')
yCoords = ui.number(label = 'YCoords')
ui.button('Give me a loop !', on_click=callBacknd)
ui.run()