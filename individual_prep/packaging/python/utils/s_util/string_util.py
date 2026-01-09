from ..m_util.math_util import add

def capitalize(str):
    if len(str) <= 1:
        return str.upper()

    return str[0].upper() + str[1:]