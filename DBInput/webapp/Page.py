# exec(open("DBInput\database\Page.py").read())
from DBInput.DBIExceptions import ArgumentNullException


class Page:
    def __init__(self, fields, url=None, title=None):
        if fields is None or None in fields:
            raise ArgumentNullException("Page: fields is None or None is in field")
        self.fields = fields
        self.url = url
        self.title = title

    def GetFieldCount(self):
        return len(self.fields)

    def Equals(self, obj):
        if not isinstance(obj, Page) or obj is None:
            return False
        other_page = obj
        if len(self.fields) != len(other_page.fields):
            return False
        for i in range(len(self.fields)):
            if self.fields[i].Same(other_page.fields[i]):
                pass
            else:
                return False
        return True

    def GetFields(self):
        return self.fields

    def GetTitle(self):
        return self.title

    def GetUrl(self):
        return self.url

    def ToString(self):
        stringresult = "Page : ["
        if self.url is not None:
            stringresult = stringresult + " Url: " + self.url
        if self.title is not None:
            stringresult = stringresult + " Title : " + self.title
        for field in self.fields:
            stringresult = stringresult + "(" + field.ToString() + "), "
        return stringresult + "]"

    def GetHashCode(self):
        hash_code = 3042524
        for field in self.fields:
            hash_code = hash_code + field.GetHashCode()
        return hash_code
