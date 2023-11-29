from flask import abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user

import functools
import typing

from .user_mixing import UserModelMixing
from .group_mixing import GroupModelMixing
from .role_mixing import RoleModelMixing

__version__ = '1.0.0'
__all__ = ('roles_required', 'RoleMan', 'UserModelMixing', 'GroupModelMixing', 'RoleModelMixing')


class RoleMan:
    UserModel = None
    GroupModel = None
    RoleModel = None
    SECONDARY_USER_GROUP_TABLE_NAME = 'users_groups'
    SECONDARY_GROUP_ROLE_TABLE_NAME = 'groups_roles'

    def __init__(self, db: SQLAlchemy = None, create_secondaries=True):
        self._user_group_secondary = None
        self._group_role_secondary = None
        self._db = db
        self._initialized = False
        if db:
            self.init_db(db, create_secondaries=create_secondaries)

    def init_db(self, db: SQLAlchemy, create_secondaries=True):
        if self._initialized:
            raise RuntimeError('UserPrivileges is already initialized !!')
        _m = 'You Forget to Inherit {}! or you Initialized {self.__class__.__name__} before importing your db Models !'
        if self.UserModel is None:
            raise TypeError(_m.format('UserModel'))
        if self.GroupModel is None:
            raise TypeError(_m.format('GroupModel'))
        if self.RoleModel is None:
            raise TypeError(_m.format('RoleModel'))

        self._db = db
        if create_secondaries:
            self.create_secondaries()
        self._initialized = True

    def create_secondaries(self):
        self._user_group_secondary = self._db.Table(
            self.SECONDARY_USER_GROUP_TABLE_NAME,
            self._db.Column('user_id', self._db.Integer(), self._db.ForeignKey(f'{self.UserModel.__tablename__}.id')),
            self._db.Column('group_id', self._db.Integer(), self._db.ForeignKey(f'{self.GroupModel.__tablename__}.id')),
        )
        #
        self._group_role_secondary = self._db.Table(
            self.SECONDARY_GROUP_ROLE_TABLE_NAME,
            self._db.Column('group_id', self._db.Integer(), self._db.ForeignKey(f'{self.GroupModel.__tablename__}.id')),
            self._db.Column('role_id', self._db.Integer(), self._db.ForeignKey(f'{self.RoleModel.__tablename__}.id')),
        )


def roles_required(*roles):
    """
    This decorator is used before routes, to ensure that the current_user has the authorization to access that route
    """
    def holder(action):
        @functools.wraps(action)
        def wrapper(*args, **kwargs):
            nonlocal roles
            #
            if current_user.is_authenticated and current_user.has_roles(*roles):
                return action(*args, **kwargs)
            #
            return abort(401)

        return wrapper

    return holder
