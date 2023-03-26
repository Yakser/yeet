def clean_field_name(value):
    return value.strip().replace('-', '_')


def clean_method(method):
    return method.strip().lower()


def clean_data(data):
    return {k: data[k][0] for k in data}
