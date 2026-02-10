import requests
import os

path=r"..\..\data\\raw"
pathfc=r"..\..\data\\processed"
for file in os.listdir(path): 
    pathc=os.path.join(path, file)
    if os.path.isfile(pathc) and ".jpg" in file:
        pathf=os.path.join(pathfc,file)
        with open(pathc, 'rb') as f_in:
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file':f_in},
                data={'size': 'auto'},
                headers={'X-Api-Key': 'jRhaHEKjKGxTKhCyhLmRnJBj'},
            )
        if response.status_code == requests.codes.ok:
            #pathf=pathf.replace(".jpg",".png")
            with open(pathf, 'wb') as out:
                out.write(response.content)
        else:
            print("Error:", response.status_code, response.text)