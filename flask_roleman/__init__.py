import functools
from flask import abort
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, model as _model


_Role: _model.Model | None = None  # holds the Role Model class to be accessed from ManMixing


class RoleMan:
    SECONDARY_TABLE_NAME = 'user_role'  # name of the secondary relationship table on the database
    ROLE_TABLE_NAME = 'role'  # name of the table that will hold the roles

    def __init__(self, db: _SQLAlchemy = None, user_table_name: str = 'user', user_table_class_name: str = 'User'):
        """
        This class is a Role Manager that will help you use the Authorization on Users to gain access,
        :param db: the SQLAlchemy database instance of your Flask web app
        :param user_table_name: specify your User table name on the database
        :param user_table_class_name: specify the name of the User class on the python code
        """
        self._initialized = False  # used within the object (private and protected)
        # > set the default values
        self._db = None
        self._user_table_name = user_table_name
        self._user_table_class_name = user_table_class_name
        self.UserRole = None
        self.Role = None

        # check whether to initialize now or not
        if db and (isinstance(db, _SQLAlchemy) or issubclass(type(db), _SQLAlchemy)):
            self.init_database(db, user_table_name, user_table_class_name)

    def init_database(self, db: _SQLAlchemy, user_table_name: str = None, user_table_class_name: str = None):
        """
        To initialize the instance if not already on the creation
        :param db:
        :param user_table_name:
        :param user_table_class_name:
        :return: None
        """
        if self._initialized:
            raise SyntaxError('The RoleMan is already initialized and can not be twice!')
        self._db = db
        # > next lines to ensure that the taken table names on the creation are the ones in use, unless they are specified again here
        self._user_table_name = self._user_table_name if not user_table_name else user_table_name
        self._user_table_class_name = self._user_table_class_name if not user_table_class_name else user_table_class_name

        self._init_roles_model()
        self._initialized = True

    def _init_roles_model(self):
        """
        This method creates the necessary models on the db object and creates the backref relationship for the User table
        :return: None
        """
        db = self._db

        # > create the secondary table for User and Role tables (with no primary key)
        self.UserRole = db.Table(self.SECONDARY_TABLE_NAME,
                                 db.Column('user_id', db.Integer(), db.ForeignKey(f'{self._user_table_name}.id')),
                                 db.Column('role_id', db.Integer(), db.ForeignKey(f'{self.ROLE_TABLE_NAME}.id')),
                                 )

        # >
        class Role(db.Model):
            __tablename__ = self.ROLE_TABLE_NAME
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String, nullable=False, unique=True)
            users = db.relationship(self._user_table_class_name, secondary=self.SECONDARY_TABLE_NAME, backref='roles')

            def __init__(self, name: str):
                self.name = name.lower()

            def __repr__(self):
                return f'<Role "{self.name}">'

        self.Role = Role
        global _Role
        _Role = Role


class RoleManMixing:
    roles = None  # just to not get the AttributeError from User, when accessing the relationship, before initializing this class

    def has_role(self, role):
        if isinstance(role, str):
            role = _Role.query.filter_by(name=role.lower()).first()
        #
        if not role:
            return False
        #
        return self in role.users

    def has_roles(self, *roles_seq):
        def _has_one_role(*_rls):
            # checks if the user has at least one role of many (OR Gate)
            for rl in _rls:
                if self.has_role(rl):
                    return True
            return False

        for role_value in roles_seq:
            if isinstance(role_value, (list, tuple, set)):
                if not _has_one_role(*role_value):
                    return False
            elif not self.has_role(role_value):
                return False
        return True


def roles_required(*roles):
    """
    This decorator is used before routes, to ensure that the current_user has the authorization to access that route
    :param role: role as str or Role object
    :return: None
    """

    def holder(action):
        @functools.wraps(action)
        def wrapper(*args, **kwargs):
            nonlocal roles
            #
            if current_user.has_roles(*roles):
                return action(*args, **kwargs)
            #
            return abort(401)

        return wrapper

    return holder


role_required = roles_required
