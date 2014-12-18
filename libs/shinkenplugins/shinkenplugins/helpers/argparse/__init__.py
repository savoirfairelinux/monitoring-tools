
def escape_help(value):
    '''
    :param value: A string message to be used as an Argument help text.
    :return: The value with its % doubled.
    '''
    return value.replace('%', '%%')

