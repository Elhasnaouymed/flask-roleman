
class GroupModelMixing:
    """
    The inherited class from this one must have:
        - name: String column
        - users: many-to-many relationship to the Users model, pass UserPrivileges.SECONDARY_USER_GROUP_TABLE_NAME to the `secondary=` argument
        - roles: many-to-many relationship to the Roles model, pass UserPrivileges.SECONDARY_GROUP_ROLE_TABLE_NAME to the `secondary=` argument
    """
    roles: list = None

    def __init_subclass__(cls, **kwargs):
        from . import RoleMan
        RoleMan.GroupModel = cls

    def has_role(self, role):
        from . import RoleMan
        if isinstance(role, str):
            role = RoleMan.RoleModel.query.filter_by(name=role.lower()).first()
        #
        if not role:
            return False
        #
        return role in self.roles

    def has_roles(self, *roles_seq):
        def _has_one_role(*_roles):
            # checks if the user has at least one role of many (OR Gate)
            for _role in _roles:
                if self.has_role(_role):
                    return True
            return False

        for role_value in roles_seq:
            if isinstance(role_value, (list, tuple, set)):
                if not _has_one_role(*role_value):
                    return False
            elif not self.has_role(role_value):
                return False
        return True
