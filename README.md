
> This Software is in **Alpha Version**, you should expect major changes from time to time !

# Flask-Roleman

**flask-roleman** is a very Simple and Minimal Flask Extension to help you manage User Authorizations using *Roles*.

### About

- **Dependencies**: `flask-login`, `flask-sqlalchemy`
- **License**: Open Source Under **GNU GPL v2**
- **Author**: Mohamed El-Hasnaouy `github/elhasnaouymed`

## Install

#### Using PIP

You can install **flask-roleman** using **pip**:

```shell
pip install flask-roleman
```

#### From source

Or you can download & compile & install it from source:

1. `git clone https://github.com/Elhasnaouymed/flask-roleman.git`
2. `cd flask-roleman`
3. `python setup.py sdist`
4. `pip install dist/flask-roleman-*.tar.gz`

> Note: Install from source will **only** work inside a Virtual Environment

## Initialization

As most Extensions of Flask, you first import and create the Main Instance, then you can **Initialize** it in place
or after:

```python
from flask_roleman import RoleMan
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
roleman = RoleMan()

app = Flask()

db.init_app(app)
roleman.init_database(db, user_table_name='user', user_table_class_name='User')
```

You have to specify **user_table_name** and **user_table_class_name** arguments if the User Model class name is not
"User" and its `__tablename__` is not "user".

## Usage

### Mixing

To use **RoleMan** in your project, you need to have the **User Model** inherit from **RoleManMixing**;

Example:

```python
from flask_roleman import RoleManMixing

class User(db.Model, RoleManMixing):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    ...
```

### Static Authorizing

Then... Whenever you want to **Require a role** from User, use this Decorator:

```python
from flask_roleman import roles_required

@app.route('/admin')
@roles_required('admin')
def admin_page():
    ...
    return render_template('admin.html')
```

### Dynamic Authorizing

Or you can check dynamically using `current_user.has_roles`:

```python
from flask_login import current_user
from flask import abort

@app.route('/admin')
def admin_page():
    if not current_user.has_roles('admin'):
        return abort(401)
    return render_template('admin.html')
```

## Control

### Advanced Checking

 Both `role_required` and `has_roles` checks if the `current_user` has the input roles;

- `role_required` allows the Request to continue if `True`, Otherwise rises `401` **abort error code**  
- `has_roles` returns `True` or `False`


`*roles` argument is `Tuple[Union[List[str], str]]`, 
which means it can take Both Strings and/or Lists of Strings as arguments, 
Presenting the names of the **Roles** a User Must have to gain access.

> For the User to be **Authorized** it must have all the string Roles and at least one Role of each list provided.

### Table Names

**flask-roleman** Creates two tables when Initialized, **role** and **user_role**, 
You can change their names using this code but only before Initialization of the `RoleMan` instance:

```python
from flask_roleman import RoleMan

RoleMan.ROLE_TABLE_NAME = "any_role_name"
RoleMan.SECONDARY_TABLE_NAME = "any_secondary_name"
```
> When Changing these table names, the whole database will need to be **Recreated** or **Migrated** for the changes to take effect !
