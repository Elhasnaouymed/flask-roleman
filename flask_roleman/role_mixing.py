
class RoleModelMixing:
    """
    The inherited class from this one must have:
        - name: String column
        - groups: many-to-many relationship to the Groups model, use `backref='groups'` on the relationship made on the Groups model
    """

    def __init_subclass__(cls, **kwargs):
        from . import RoleMan
        RoleMan.RoleModel = cls
