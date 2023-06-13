from PIL import Image
import random

def mix_image(pizza,toppings):
    main_pizza = Image.open(pizza)

    main_toppings = []
    for topping in toppings:
        top = Image.open(topping)
        main_toppings.append(top)

    first_intermediate = Image.alpha_composite(main_pizza,main_toppings[0])

    for topping in main_toppings:
        if topping != main_toppings[0]:
            first_intermediate = Image.alpha_composite(first_intermediate,topping)

    final_result = first_intermediate.save(f"image{random.choices(pizza,k=2)[0]}{random.choices(pizza,k=2)[1]}.png")

    return final_result
