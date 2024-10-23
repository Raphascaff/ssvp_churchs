import re

def decode_unicode_escapes(text):
    return re.sub(r'\\u[0-9a-fA-F]{4}', lambda match: chr(int(match.group(0)[2:], 16)), text)

def extract_lat_long(text):
    a, b, c = text.find('!3d'), text.find('!4d'), text.find('!16')
    lat = text[a:b].replace('!3d', '')
    lon = text[b:c].replace('!4d', '')
    return [float(lat), float(lon)]