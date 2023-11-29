
> This Software is in **Beta Version**, Please place an issue or contact me if you found a Bug !

# Flask-Roleman

**flask-roleman** is a flask extension for User Authorizations, Users can have Groups, 
and Each Group can have Roles, you can define your Groups Model and Roles Model, as well as Users Model.

### About

- **Dependencies**: `flask` `flask-login`, `flask-sqlalchemy`
- **License**: Open Source Under **GNU GPL v2**
- **Author**: Mohamed El-Hasnaouy `codeberg.org/elhasnaouymed`

## Live Example

[**Jump to live example**](#the-live-example)

## Install

#### Using PIP

You can install **flask-roleman** using **pip**:

```shell
pip install flask-roleman
```

#### From source

Or you can download & compile & install it from source:

1. `git clone https://codeberg.org/Elhasnaouymed/flask-roleman.git`
2. `cd flask-roleman`
3. `python setup.py sdist`
4. `pip install dist/flask-roleman-*.tar.gz`

> Note: on most GNU/Linux distributions, You can install **only** inside a Virtual Environment (see [PEP 0668](https://peps.python.org/pep-0668/))

## Initialization

As most Extensions of Flask, you first import and create the Main Instance, then you can **Initialize** it in place
or after:

```python
...

db = SQLAlchemy()
roleman = RoleMan()

...

roleman.init_db(db, create_secondaries=True)

...
```

But before initialization, you **must** define the three models to inherit from their mixing,
as shown in the [next section](#usage).

also you should initialize before `db.init_app()` to allow secondary tables to be created.

### Mixing

To use **RoleMan** in your project, you need to have:
 - **User Model** that inherits from `flask_roleman.UserModelMixing`.
 - **Group Model** that inherits from `flask_roleman.GroupModelMixing`.
 - **Role Model** that inherits from `flask_roleman.RoleModelMixing`.

> Group Model must have:
> - A String column `name`.
> - `users`: *many-to-many* relationship to the Users model, with `secondary=RoleMan.SECONDARY_USER_GROUP_TABLE_NAME` and `backref="groups"`.
> - `roles`: *many-to-many* relationship to the Roles model, with `secondary=RoleMan.SECONDARY_GROUP_ROLE_TABLE_NAME` and `backref="groups"`.

> Role Model must have:
> - A String column `name`.

### Minimal Example
Minimal Example of defining the three necessary Models with their Inheritance:

```python
from flask_roleman import RoleMan, UserModelMixing, GroupModelMixing, RoleModelMixing

class User(db.Model, UserModelMixing):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    ...

class Group(db.Model, GroupModelMixing):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    users = db.relationship('User', secondary=RoleMan.SECONDARY_USER_GROUP_TABLE_NAME, backref="groups")
    roles = db.relationship('Role', secondary=RoleMan.SECONDARY_GROUP_ROLE_TABLE_NAME, backref="groups")
    ...
    
class Role(db.Model, RoleModelMixing):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    ...
```

# Usage

There are two ways to use this tool, [One](#static-authorizing) by decorating the route you want to protect, 
[Two](#dynamic-authorizing) is by using `.has_roles()` method over a User or a Group

Both methods take variable length argument `*roles=Tuple[Union[List[str], str]]`, you can pass a list of roles like `['admin', 'manager', 'chief']`
or just a role name as string like `'admin'`

> * by passing a list, the User must have at least one of the Roles
> * by passing a string, the User must have that Role
> 
> In other words: the program performs *AND* operator over the method arguments, and *OR* over the list values.


> **Notes**
>> You should assign Roles to Groups, and Groups to the Users.
> 
>> The user get Authorized only if he has at least one of the Requested roles bound to one of his Groups.   

## Static Authorizing

Whenever you want to **Require a role** from User, use this Decorator:

```python
from flask_roleman import roles_required

@app.route('/admin')
@roles_required('admin')
def admin_page():
    ...
    return render_template('admin.html')
```

## Dynamic Authorizing

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


# The Live Example

**In This example, the user will always get 401 error when accessing `/admin`,
until he logs in with a user that has the 'admin' role in one of his groups**

```python
from flask import Flask
from flask_login import LoginManager
from flask_roleman import RoleMan, UserModelMixing, GroupModelMixing, RoleModelMixing, roles_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5d19362626f3290221a2b37f0a5038d07e5aa0e18a9967ffcbedc69eaee4cce9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy()
login_manager = LoginManager(app)


@login_manager.user_loader
def user_loader(id: int):
    return User.query.get(id)


class User(db.Model, UserModelMixing):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class Group(db.Model, GroupModelMixing):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    users = db.relationship('User', secondary=RoleMan.SECONDARY_USER_GROUP_TABLE_NAME, backref="groups")
    roles = db.relationship('Role', secondary=RoleMan.SECONDARY_GROUP_ROLE_TABLE_NAME, backref="groups")


class Role(db.Model, RoleModelMixing):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


@app.route('/')
def home():
    return 'Hello World! from Home'

@app.route('/admin')
@roles_required('admin')
def admin():
    return 'Admin Page !!!'


if __name__ == '__main__':
    app.run(debug=True)

```