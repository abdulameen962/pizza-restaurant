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

#topping
# https://res.cloudinary.com/abdulameen/image/upload/v1686939342/ahbpz3fwgxnzkclrckcb.png
#pizza
# https://res.cloudinary.com/abdulameen/image/upload/v1686938567/ics6uo021j0u1xmvr75b.png

def mix_image(pizza,toppings):
    main_pizza = urllib.request.urlretrieve(pizza,"media/pizza.png")
    main_pizza = Image.open(main_pizza[0])
    first_name = main_pizza.filename
    type(main_pizza)
    main_pizza.resize((250, 250)).save(first_name)
    type(main_pizza)
    main_pizza = Image.open(first_name)
    main_toppings = []
    for topping in toppings:
        top = urllib.request.urlretrieve(topping,f"media/topping{toppings.index(topping)}.png")
        top = Image.open(top[0])
        second_name = top.filename
        top.resize(main_pizza.size).save(second_name)
        top = Image.open(second_name)
        main_toppings.append(top)

    first_intermediate = main_pizza
    if len(main_toppings) > 0:
        # mask = Image.new("L", main_toppings[0].size, 0)
        # draw = ImageDraw.Draw(mask)
        # draw.rectangle((200, 100, 300, 200), fill=255)
        first_intermediate = Image.alpha_composite(main_pizza,main_toppings[0])

        for topping in main_toppings:
            if topping != main_toppings[0]:
                # mask = Image.new("L", top.size, 0)
                # draw = ImageDraw.Draw(mask)
                # draw.rectangle((800, 800, 800, 800), fill=255)
                first_intermediate = Image.alpha_composite(first_intermediate,topping)

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


# creating a image1 object and converting it to mode 'L'
# main_pizza = urllib.request.urlretrieve('https://res.cloudinary.com/abdulameen/image/upload/v1686938567/ics6uo021j0u1xmvr75b.png',"media/pizza.png")
# main_pizza = Image.open(main_pizza[0])
# first_name = main_pizza.filename
# main_pizza = main_pizza.resize((250, 250))
# main_pizza.save(first_name)
# main_pizza = Image.open(first_name)
# top = urllib.request.urlretrieve('https://res.cloudinary.com/abdulameen/image/upload/v1686939342/ahbpz3fwgxnzkclrckcb.png',f"media/topping.png")
# top = Image.open(top[0])
# second_name = top.filename
# top = top.resize(main_pizza.size)
# top.save(second_name)
# top = Image.open(second_name)
# creating a mask image object and converting it to mode 'L'
# mask = Image.new("L", top.size, 5)
# draw = ImageDraw.Draw(mask)
# draw.rectangle((200, 100, 300, 200), fill=255)
# compositing all the three images
# first_intermediate = Image.alpha_composite(main_pizza,top)
