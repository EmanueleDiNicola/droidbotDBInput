class ArgumentNullException(Exception):

    def __init__(self, error_name):
        self.error_name = error_name
        super().__init__(self.error_name)


class ArgumentException(Exception):

    def __init__(self, error_name):
        self.error_name = error_name
        super().__init__(self.error_name)


class SqlException(Exception):

    def __init__(self, error_name):
        self.error_name = error_name
        super().__init__(self.error_name)


class ArgumentOutOfRangeException(Exception):

    def __init__(self, error_name):
        self.error_name = error_name
        super().__init__(self.error_name)


class NotImplementedException(Exception):
    def __init__(self):
        self.error_name = "Not Implemented"
        super().__init__(self.error_name)


class InvalidOperationException(Exception):
    def __init__(self, error_name):
        self.error_name = error_name
        super().__init__(self.error_name)
