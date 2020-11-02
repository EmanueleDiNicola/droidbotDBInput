from numpy.core.defchararray import lower


def CleanString(string):
    new_string = ''.join(e for e in string if e.isalnum())
    new_string = lower(new_string)
    return str(new_string)

# exec(open("DBInput\\relations\\fieldcolumncomparer\StringTransformation.py").read())
