import os
import json


from flask import jsonify, request

from flask import session
from flask_cors import cross_origin

from .models import Customers, Countries, Cities, Orders, OrderDetails, Products

from sqlalchemy.sql import or_, and_
from sqlalchemy import select
from sqlalchemy import cast, String, Integer

#from sqlalchemy.ext.serializer import loads, dumps

from . import create_app # __init__.py
# app = create_app(os.getenv("CONFIG_MODE"))
app = create_app()


    
#------------------------

def to_tree(queries):
    
    tree = []
    for p in queries[0]:
        branch = {
            'key': p.get('pk'),
            'fk': p.get('fk'),
            'label': p.get('label')
        }
        if len(queries) > 1:
            branch['children'] = [c for c in to_tree(queries[1:]) if c.get('fk') == p.get('pk')]
        tree.append(branch)
    
    return tree
        
    
    
@app.route('/first/<digit>')
@cross_origin(supports_credentials=True)
def first(digit):
    
    if digit == '1':
        session['this_one'] = 'hello'
        return 'Hello was saved into session[this_one].'
    elif digit == '2':
        return 'Value inside session[this_one] is {}.'.format(session['this_one'])




#-------------------------

# A simple PrimeVue Dropdown
# GET cities to fill dropdown options, and customers
# to display customer information for each selected city
@app.route('/dropdown/<table>')
@cross_origin(supports_credentials=True)
def get_dropdown(table):
    
    if table == "cities":
        records = Cities.query.all()
        results = [
            {'city': record.city} for record in records
        ]
    elif table == "customers":
        records = Customers.query.all()
        results = [
            {'customerNumber': record.customerNumber,
             'customerName': record.customerName,
             'contactLastName': record.contactLastName,
             'city': record.city,
             'country': record.country} for record in records
        ]
    else:
        pass
        # TODO: request error handling
        
    # get attr e.g. <entry> 
    # results = [{entry: getattr(record, entry)} for record in records]
    # or limit number of records ?limit=5
    # lim = request.args.get("limit", type=int)
    # if lim is not None:
    #    results = results[:lim]
    
    return jsonify(results)


# Dynamic dependent TreeSelect components (via API)
# GET options
# POST model values on change via response
@app.route('/select/<selection>', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def get_treeselect(selection):
    
    if selection == "cities":
         
         # what if not GET or POST?
         
        if request.method == 'GET':
            
            # define class methods how to return e.g. countries, cities
            # Use API e.g. RestPlus?
            
            # define data model 
            
            query = Countries.query.all()
            countries = [
                {'key': q.id,
                'pk': q.country,
                'label': q.country} for q in query
            ]
            query = Cities.query.all()
            cities = [
                {'key': q.id,
                'pk': q.city,
                'fk': [c['pk'] for c in countries if c['key'] == q.countryId][0],
                'label': q.city} for q in query
            ]
            
            tree = to_tree([countries, cities])
            response_object = { "tree": tree }
            
            # return entire table
            
            query = (
                Customers.query.with_entities(
                    Customers.customerNumber, 
                    Customers.customerName,
                    Customers.country,
                    Customers.city
                )
                .join(Orders, Customers.customerNumber == Orders.customerNumber)
                .join(OrderDetails, Orders.orderNumber == OrderDetails.orderNumber)
                .join(Products, OrderDetails.productCode == Products.productCode)
                .add_columns(Orders.orderNumber, Products.productName, Products.productLine)
                #.order_by(cast(Customers.customerName, String))
                .order_by(cast(Customers.customerNumber, Integer))
                .all()
            )
            records = [ 
                {
                    "customerNumber": customerNumber,
                    "customerName": customerName,
                    "country": country,
                    "city": city,
                    "orderNumber": orderNumber,
                    "productLine": productLine,
                    "productName": productName
                } for customerNumber, customerName, country, city, orderNumber, productName, productLine in query
            ]
            response_object["records"] = records 
            response_object["totalRecords"] = len(records) 
            
            # Cookie “session” is invalid because its size is too big. Max size is 4096 B.
            # session["records"] = records
            
            #return jsonify(response_object)
            return response_object
        
        elif request.method == 'POST':
            
            # we need a better dynamic general purpose construction of filter queries...
            
            countries_or_cities = request.get_json().keys()
            
            # SELECT customers.customerNumber, customers.customerName, orders.orderNumber, products.productName FROM customers JOIN orders ON customers.customerNumber = orders.customerNumber JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber JOIN products ON orderdetails.productCode = products.productCode WHERE customers.city = "Berlin" ORDER BY(orderNumber);
            
            query = (
                Customers.query.with_entities(
                    Customers.customerNumber, 
                    Customers.customerName
                )
                .join(Orders, Customers.customerNumber == Orders.customerNumber)
                .join(OrderDetails, Orders.orderNumber == OrderDetails.orderNumber)
                .join(Products, OrderDetails.productCode == Products.productCode)
                .filter(
                    or_(Customers.city.in_(countries_or_cities),
                        Customers.country.in_(countries_or_cities))
                )
                .add_columns(Orders.orderNumber, Products.productName, Products.productLine)
                #.order_by(cast(Customers.customerName, String))
                .order_by(cast(Customers.customerNumber, Integer)) # ???
                .all()
            )
            
            # this might not work for large queries
            # and this is not great to query here, but filter twice FE + BE... and in addition to store data
            session["query"] = [ {
                    "customerNumber": customerNumber,
                    "customerName": customerName,
                    "orderNumber": orderNumber,
                    "productLine": productLine,
                    "productName": productName
                } for customerNumber, customerName, orderNumber, productName, productLine in query
                ]
            
            # response
            
            # here we need to wrangle the query, but if we had adequate models/tables
            # then we could possibly make this simpler...
            # order ??
            
            customers = list(set([(q[0], q[1]) for q in query]))
            customers = [
                {'key': customerNumber,
                    'pk': customerName,
                    'label': customerName} for customerNumber, customerName in customers
            ]
            orders = list(set([(q[1], q[2]) for q in query]))
            orders = [
                {'key': orderNumber,
                    'pk': orderNumber,
                    'fk': customerName,
                    'label': orderNumber} for customerName, orderNumber in orders
            ]
            products = list(set([(q[2], q[3]) for q in query]))
            products = [
                {'key': productName,
                    'pk': productName,
                    'fk': orderNumber,
                    'label': productName} for orderNumber, productName in products
            ]
            records = to_tree([customers, orders, products])
                    
            #print(records)
            return(jsonify(records))
        
    elif selection == "products":
        
        if request.method == 'GET':
            
            pass
        
        elif request.method == 'POST':
            
            customer_order_products = request.get_json().keys()
            
            # SELECT customers.customerNumber, customers.customerName, orders.orderNumber, products.productName FROM customers JOIN orders ON customers.customerNumber = orders.customerNumber JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber JOIN products ON orderdetails.productCode = products.productCode WHERE 
            #customers.country = "Germany" AND (customers.customerName IN ("Bavarian Collectables Imports, Co.", "10101", "1969 Dodge Charger") OR orders.orderNumber IN ("Bavarian Collectables Imports, Co.", "10101", "1969 Dodge Charger") OR products.productName IN ("Bavarian Collectables Imports, Co.", "10101", "1969 Dodge Charger"));
    
            # can we just use the previous query (a list) and filter it out?
            # for this we would need some (Redis or other) cache management...
                    
            #response = [(customerNumber, customerName, orderNumber, productName) for customerNumber, customerName, orderNumber, productName in session["query"] if (customerName in customer_order_products) or (orderNumber in customer_order_products) or (productName in customer_order_products) ]
            
            response = [(customerNumber, customerName, orderNumber, productName, productLine) for customerNumber, customerName, orderNumber, productName, productLine in session["query"] if (customerName in customer_order_products) or (orderNumber in customer_order_products) or (productName in customer_order_products)]

            # string/int types are different from qeury results and request
            
            response = [ d for d in session.get("query") 
                        if (d["customerName"] in customer_order_products) or (str(d["orderNumber"]) in customer_order_products) or (d["productName"] in customer_order_products) ]
            
            #session["response"] = response
            
            product_lines = list(set([d["productLine"] for d in response]))
            
            return jsonify(product_lines)
            #return response
            
    #elif selection == "lines":
        
        #if request.method == 'GET':
            
            #pass
        
        #elif request.method == 'POST':
            
            #lines = request.get_json()
            
            #response = [ d for d in session.get("response") if d["productLine"] in lines ]
            
            #return response # do we need to jsonify?
    else:
        
        pass
    


if __name__ == "__main__":
    app.run()
