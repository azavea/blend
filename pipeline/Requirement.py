class Requirement:
    """
    Represents the a dependency that one Resource has on another.
    """
    def __init__(self, name, type, insert_location = 0):
        """
        Arguments:
        name -- The string name of the required resource
        type -- Where to search for the required resource. Can be local or global
        """
        if not name:
            raise Exception('Requirement must be created with a name')
        if not isinstance(name, str):
            raise Exception('The name argument must be set to a string')
        self._name = name

        if not type:
            raise Exception('Requirement must be created with a type')
        if not isinstance(type, str):
            raise Exception('The type argument must be set to a string')
        if not type in ['local', 'global']:
            raise Exception('The type argument must be "local" or "global"')
        self._type = type

        if isinstance(insert_location, basestring):
            raise Exception('The insert_location argument must be a number or a two-number tuple')
        self._insert_location = insert_location

    @property
    def name(self):
        """
        The string name of the required resource
        """
        return self._name

    @property
    def type(self):
        """
        Where to search for the required resource. Can be local or global
        """
        return self._type

    @property
    def insert_location(self):
        """
        The descriptions of the the other resources that this resource depends on
        """
        return self._insert_location