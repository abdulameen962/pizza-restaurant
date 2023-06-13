from .models import *
from django.utils import timezone
import datetime

present_month = timezone.now().month
previous_month = timezone.now().replace(day=1) - datetime.timedelta(days=1)
previous_two_month = previous_month.replace(day=1) - datetime.timedelta(days=1)
previous_month = previous_month.month
previous_two_month = previous_two_month.month

def lowest(pizzas):
    lowest_pizza = ""

    for pizza in pizzas:
        for second in pizzas:
            if pizza != second:
                if len(pizza.creation_orders.all()) <= len(pizza.creation_orders.all()):
                    if lowest_pizza == "":
                        lowest_pizza = pizza

                    elif len(pizza.creation_orders.all()) < len(lowest_pizza.creation_orders.all()):
                        lowest_pizza = pizza

    return lowest_pizza

def lowestCreator(creators):
    lowest_creator = ""

    for first in creators:
        for second in creators:
            if first != second:
                if len(first.creations.filter(available=True)) <= len(second.creations.filter(available=True)):
                    if lowest_creator == "":
                        lowest_creator = first

                    elif len(first.creations.filter(available=True)) < len(lowest_creator.creations.filter(available=True)):
                        lowest_creator = first

    return lowest_creator

def calculate(orders,order_list,month):
    money_spent = 0

    for order in orders:
        if order.order_date.month == month:
            order_list.add(order)

    if len(order_list) > 0:
        for order in order_list:
            money_spent += order.price

    return money_spent

def present_month_spent(orders):
    present_month_orders = set()

    return calculate(orders,present_month_orders,present_month)

def previous_month_spent(orders):
    past_month_orders = set()

    return calculate(orders,past_month_orders,previous_month)
    

def calculate_completed(orders,orders_list,month):

    for order in orders:
        if order.order_date.month == month:
            orders_list.add(order)

    return len(orders_list)


def present_completed_orders(orders):
    present_month_orders = set()

    return calculate_completed(orders,present_month_orders,present_month)

def past_completed_orders(orders):
    past_month_orders = set()
    
    return calculate_completed(orders,past_month_orders,previous_month)

def calculate_creations(orders,orders_list,month):

    for order in orders:
        if order.created.month == month:
            orders_list.add(order)

    return len(orders_list)

def present_creations(creations):
    present_month_creations = set()

    return calculate_creations(creations,present_month_creations,present_month)

def past_creations(creations):
    past_month_orders = set()
    
    return calculate_creations(creations,past_month_orders,previous_month)
