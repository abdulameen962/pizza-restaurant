from PIL import Image,ImageDraw
import random
import urllib.request
import os
from django.conf import settings

def delete_image(path):
    file_path = os.path.join(settings.BASE_DIR,path)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        
        except PermissionError or OSError:
            state = "jj"



def mix_image(pizza,toppings):
    main_pizza = urllib.request.urlretrieve(pizza,"media/pizza.png")
    main_pizza = Image.open(main_pizza[0])
    main_pizza.thumbnail((250, 250))
    main_toppings = []
    for topping in toppings:
        top = urllib.request.urlretrieve(topping,f"media/topping{toppings.index(topping)}.png")
        top = Image.open(top[0])
        top.resize(main_pizza.size)
        main_toppings.append(top)

    first_intermediate = main_pizza
    if len(main_toppings) > 0:
        mask = Image.new("L", main_toppings[0].size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle((200, 100, 300, 200), fill=255)
        first_intermediate = Image.composite(main_toppings[0],main_pizza,mask)

        for topping in main_toppings:
            if topping != main_toppings[0]:
                mask = Image.new("L", top.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.rectangle((800, 800, 800, 800), fill=255)
                first_intermediate = Image.composite(topping,first_intermediate,mask)

        for topping in main_toppings:
            path = topping.filename
            if path:
                delete_image(path)    

    path = main_pizza.filename
    if path:
        delete_image(path)

    #delete all toppings images
    filename = f"media/image{random.randint(1,1000000000)}{random.randint(1,50000000)}.png"
    first_intermediate.save(filename)
    first_intermediate = Image.open(filename)

    return first_intermediate
