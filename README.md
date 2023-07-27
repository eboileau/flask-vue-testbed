Flask-VueJS testbed application
===============================

**Back-end (server)**

- MySQL database (MariaDB)
- Python3 and Flask

**Front-end (client)**

- VueJS
- vue-router
- PrimeVue (components)
- Tailwind (CSS)

Installation
------------

Separately install BE + FE, following instructions below. Later we containerize everything.

### Back-end

#### MySQL database

Use an example database to quickly get up and running.

```mysql
# Download the classicmodels database from https://www.mysqltutorial.org/wp-content/uploads/2018/03/mysqlsampledatabase.zip
# sudo mysql
source /home/eboileau/prj/RMapDFGTRR319/database/mysqlsampledatabase.sql
GRANT ALL PRIVILEGES ON classicmodels.* TO 'eboileau'@'localhost';
```

#### Python3 and Flask

Initialize the virtual environment and install the dependencies under server/src/

```bash
python3 -m venv ~/.venv/toy-app
source ~/.venv/toy-app/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
# https://docs.sqlalchemy.org/en/20/intro.html#building-the-cython-extensions
```

`mysqlclient` may require some setup (see https://pypi.org/project/mysqlclient/), *e.g.*

```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
# 0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
# check https://docs.sqlalchemy.org/en/20/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqldb
# pip install mysqlclient
```

### Front-end

```bash
# init client
npm init vue@3 

cd client
npm install
npm run format
# Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
# PrimeVue
npm install primevue
npm install primeicons
# Axios
npm install axios
```

If installing from this repository

```bash
# within the root directory
npm install
```

Running the application
-----------------------

Each needs to be started independently. Start the server (client) and the Flask server

```bash
# start client
npm run dev
# start under server/src
source ~/.venv/toy-app/bin/activate
flask run --debug
```

Development notes
-----------------

```bash
# remote copy
rsync -avzh flask-vue-testbed eboileau@cluster.dieterichlab.org:/prj/TRR319_RMaP/Project_C02/sci-modom/backup-local/
```

### Python/SQLAlchemy

So far use a declarative-like approach with `DeferredReflection`. Maybe we could be more explicit -> DB schema, *etc.*? Need to look into Alembic documentation.

How to check session status while the app is running? Does teardown works?

#### Caching

Unclear whether we require caching queries, this may depend on the actual strategy (lazy loading, *etc.* ). I currently use Flask `session`, there is some
stuff on the web, TL;DR, but in summary we need to enable CORS and credentials support on the back end, and use credentials in the front end code when issuing requests, because the javascript is not on a template served by Flask, but coming from a different origin.

```python
from flask_cors import CORS, cross_origin
# use decorator
@cross_origin(supports_credentials=True)
```

then set `withCredentials: true` when creating Axios instance (services/index.js).

But more generally, we might need a true solution to cache database queries, *e.g.* using Redis

- before reading from the database, check if the data exists in the cache
- if the data exists, use it, otherwise query the database
- update the cache with query results before returning 


For other stuff, I think we first have to look at Pinia (VueJS store), and FireBase.

#### API

Plain Flask, Flask-RESTful, Flask-RESTPlus ???

#### Serialization format

So far, no big problem, but we use custom query handling. We probably need a better all-purpose approach, *e.g.* flask.ext.jsontools, marshmallow-sqlalchemy, Pickle (not secure), or define our own methods, *etc.* 

**Note:** The `@dataclass` decorator doesn't work directly on `Reflected` classes, I think we might have to define them explicitely...

Check out [How to serialize SqlAlchemy result to JSON?](https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json)

#### CORS

https://flask-cors.readthedocs.io/en/latest/

BE server *vs.* dev proxy. Start with simple: allow CORS for all domains on all routes.

#### Snippets

```python
# using the classicmodels DB outside the app
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()
DATABASE = "mysql+mysqldb://eboileau:@localhost/classicmodels"
engine = create_engine(DATABASE)
Base.prepare(autoload_with=engine)

# define models
Customers = Base.classes.customers
OrderDetails = Base.classes.orderdetails
Orders = Base.classes.orders
Products = Base.classes.products
Countries = Base.classes.countries
Cities = Base.classes.cities

session = Session(engine)

# perform queries...
# query = session.query(Customers, ...) ... .join() .filter() .all()
# query = session.execute(select(Customers, ...)) ... .join() .filter() .all()
# query[0].__mapper__.attrs.keys() # a list

```

### VueJS

#### API calls - Axios

Lazy loading with custom pagination using `limit` and `offset`.

#### Router

Check https://router.vuejs.org/guide/advanced/data-fetching.html

### MySQL

Add 2 tables:

```mysql
USE classicmodels;

CREATE TABLE countries (id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id), country varchar(50) NOT NULL)
    SELECT country FROM customers 
    GROUP BY(country);
  
CREATE TABLE cities (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, countryId INT NOT NULL, city VARCHAR(50) NOT NULL) 
    SELECT countries.id AS countryId, customers.city AS city FROM customers 
    JOIN countries ON customers.country = countries.country 
    GROUP BY(city);
    
-- NOTE: FOREIGN KEY (countryId) REFERENCES countries(id) ???
```

#### UUID
    
Do we need it? With MariaDB that might be more difficult.

### Data model, data handling, and communication (API but not Axios-specific)

#### TreeSelect

Tree construction is arbitrary, here we used customerName > orderNumber > productName, but this results in non-unique choices in the tree, *e.g.* same productName for different orderNumber (*i.e.* if selecting a given product under a certain order, all orders containing this product are actually displayed). In our true application, this should not occur! The PrimeVue `TreeSelect` component selects ALL of them when one is selected. In summary, we need to make sure the data model is consistent and normalized (-> about RNA modification - *e.g.* m6A mRNA and m6A rRNA, or organism *e.g.* H. Sapiens Heart and M. Musculus Heart, *etc.*)!





