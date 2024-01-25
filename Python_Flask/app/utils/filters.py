# filters in Jinja are similar to the register helper functions
def format_date(date):
    return date.strftime('%m/%d/%y')  # helper function to format the date
# the strftime() method to convert it to a string. The %m/%d/%y format code will result in something like "01/01/20".


def format_url(url):
    return url.replace('http://', '').replace('https://', '').replace('www', '').split('/')[0].split('?')[0]
# Removes all extraneous information from a URL string, leaving only the domain name. Note that the methods we use,
# like replace() and split(), behave exactly the same as they do in JavaScript.


def format_plural(amount, word):
    if amount != 1:
        return word + 's'

    return word
