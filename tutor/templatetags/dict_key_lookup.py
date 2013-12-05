from django import template
register = template.Library()

@register.simple_tag
def dictKeyLookup(the_dict, key):
    try: # In case key is an int
        if '+' in key:
            return ' + '.join([ dictKeyLookup(the_dict, single_key) for single_key in key.split('+') ])
    except:
        pass
    return the_dict.get(key, key)
