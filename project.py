__author__ = 'Steve'

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from mysql_setup2 import *


app = Flask(__name__)


@app.route('/')
def show_all_restaurant():
    rows = get_all_restaurants()
    return render_template('restaurants.html', rests=rows)


@app.route('/rest/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    items1 = get_all_menu_item_by_restaurant(restaurant_id)
    rest = get_restaurants_by_id(restaurant_id)
    return render_template('menu.html', restaurant=rest, items=items1)


# Task 1: Create route for newMenuItem function here

@app.route('/rest/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        name = request.form['newItemName']
        add_item(name, restaurant_id)
        flash("new menu item '{0}' created!".format(name))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        rest = get_restaurants_by_id(restaurant_id)
        return render_template('newmenuitem.html', rest=rest)


# Task 2: Create route for editMenuItem function here

@app.route('/rest/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        name = request.form['newItemName']
        price = request.form['newItemPrice']
        course = request.form['newItemCourse']
        description = request.form['newItemDescription']
        update_menu_item_name(menu_id=menu_id, new_name=name, new_course=course, new_price=price,
                              new_description=description)
        flash("menu item '{0}' modified!".format(name))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        menu = get_menu_item_by_id(menu_id)
        rest = get_restaurants_by_id(restaurant_id)
        return render_template('editMenuItem.html', rest=rest, menu=menu)


# Task 3: Create a route for deleteMenuItem function here

@app.route('/rest/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        menu = get_menu_item_by_id(menu_id)
        flash("menu item '{0}' deleted!".format(menu.name))
        delete_menu_item(menu_id)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        menu = get_menu_item_by_id(menu_id)
        return render_template('deleteItem.html', rest_id=restaurant_id, menu=menu)


@app.route('/rest/<int:restaurant_id>/json')
def restaurantMenuJSON(restaurant_id):
    items = get_all_menu_item_by_restaurant(restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/rest/<int:restaurant_id>/<int:menu_id>/json')
def menuJSON(restaurant_id, menu_id):
    item = get_menu_item_by_id(menu_id)
    return jsonify(MenuItem=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'haha'
    app.debug = True
    app.run()