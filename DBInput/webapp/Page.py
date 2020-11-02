# exec(open("DBInput\database\Page.py").read())
from DBInput.DBIExceptions import ArgumentNullException


class Page:
    def __init__(self, fields, url=None, title=None):
        if fields is None or None in fields:
            raise ArgumentNullException("fields")
        self.fields = fields
        self.url = url
        self.title = title

    def get_field_count(self):
        return len(self.fields)

    def equals(self, obj):
        if not isinstance(obj, Page) or obj is None:
            return False
        other_page = obj
        if len(self.fields) != len(other_page.fields):
            return False
        for i in range(len(self.fields)):
            if self.fields[i].same(other_page.fields[i]):
                pass
            else:
                return False
        return True

    def get_fields(self):
        return self.fields

    def get_title(self):
        return self.title

    def get_url(self):
        return self.url

    def tostring(self):
        stringresult = "Page : ["
        if self.url is not None:
            stringresult = stringresult + " Url: " + self.url
        if self.title is not None:
            stringresult = stringresult + " Title : " + self.title
        for field in self.fields:
            stringresult = stringresult + "(" + field.tostring() + "), "
        return stringresult + "]"

    def get_hash_code(self):
        hash_code = 3042524
        for field in self.fields:
            hash_code = hash_code + field.get_hash_code()
        return hash_code
