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

#--------------------------------------------------------------------
# some helper functions that may end up somehwere else... or nowhere...


def convert_tup_list_to_json(keys, query_list):
    # quickly convert to dict/json
    # we need a true solution to jsonify the query results...
    return [dict(zip(keys, q)) for q in query_list]


def paginate(query, first, rows):
    length = query.count()
    query = query.offset(first).limit(rows)
    # return {'totalRecords': length, 'content': convert_tup_list_to_json(query.all())}
    return (length, query)


#--------------------------------------------------------------------
# routes - could also go somewhere else if app gets bigger...


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
@app.route('/select', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_select():
         
    # this query should only be run on mount...
    # for our application, queries different tables (here this is duplicated with search
    # and I'm not sure this is sound - tree construction in the FE?)
    
    # this query should not be expensive...
    # TODO: caching?
        
    # order of keys = order of query
    # TODO: !
    keys = ["customerNumber", "customerName", "country", "city", "orderNumber", "productName", "productLine"]
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
            .order_by(cast(Customers.customerNumber, Integer))
    )
    response_object = {"records": convert_tup_list_to_json(keys, query.all()) }
 
    return response_object
    
    
@app.route('/search', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_test():
    
    city = request.args.getlist("city")
    product = request.args.getlist("product")
    line = request.args.getlist("line")
    print(f"{city}-{product}-{line}")
    first_record = request.args.get("firstRecord", type=int)
    max_records = request.args.get("maxRecords", type=int)
    print(f"{first_record}-{max_records}")
    
    #return(jsonify({ 'status': 'success'}))
        
    # order of keys = order of query
    # TODO: !
    keys = ["customerNumber", "customerName", "country", "city", "orderNumber", "productName", "productLine"]
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
            .order_by(cast(Customers.customerNumber, Integer))
    )
    
    if city:
        query = query.filter(
                    or_(Customers.city.in_(city),
                        Customers.country.in_(city))
        )
    if product:
        query = query.filter(
                    or_(Customers.customerName.in_(product),
                        Orders.orderNumber.in_(product),
                        Products.productName.in_(product))
        )
    if line:
        query = query.filter(Products.productLine.in_(line))
        
    # TODO: so far this hasn't hit the DB (is this correct?)...
    # whether we do convert_tup_list_to_json(keys, query.all()) or convert_tup_list_to_json(keys, query)
    # there seem to be no difference - because iterating through the list/rows?
    # TODO: caching (when?)
                    
    response_object = dict()
    response_object["totalRecords"], query = paginate(query, first_record, max_records)
    print(f"{response_object['totalRecords']}")
    print(f"{query.count()}")
    # ad hoc...
    response_object["records"] = convert_tup_list_to_json(keys, query.all())

    return response_object
            
                

if __name__ == "__main__":
    app.run()
