# this helper method code is from mlissner at
# https://stackoverflow.com/questions/44307480/convert-size-notation-with-units-100kb-32mb-to-number-of-bytes-in-python/44307481
def get_bytes(size_str):
    multipliers = {
        'kb': 1024,
        'k': 1024,
        'mb': 1024**2,
        'm': 1024**2,
        'gb': 1024**3,
        'g': 1024**3
    }

    for suffix in multipliers:
        size_str = size_str.lower().strip().strip('s')
        if size_str.lower().endswith(suffix):
            return int(float(size_str[0:-len(suffix)]) * multipliers[suffix])
    else:
        if size_str.endswith('b'):
            size_str = size_str[0:-1]
        elif size_str.endswith('byte'):
            size_str = size_str[0:-4]
    return int(size_str)