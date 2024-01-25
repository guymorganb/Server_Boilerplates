from flask import session, redirect
from functools import wraps


# functools module contains several helper functions that we can use to change other functions.
# the wraps() function that we imported is a decorator itself
def login_required(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        print('wrapper')
        # if logged in, call original function with original arguments
        if session.get('loggedIn') == True:
            return func(*args, **kwargs)

        return redirect('/login')

    return wrapped_function
# A decorator is intended to return a new function—hence, we have the wrapped_function().
# However, by returning a new function, we change the internal name of the original function.
# To clarify, printing callback.__name__ prints wrapped_function instead of callback.
# That might not seem serious, but it can make debugging harder.
# Thankfully, the @wraps(func) decorator preserves the original name when creating the wrapped function.
# We want to preserve not only the name but any arguments that the original function received.
# For example, callback('data') should translate to func('data') when called inside the decorator.
# The *args and **kwargs keywords ensure that no matter how many arguments are given (if any),
# the wrapped_function() captures them all.
# Custom decorators are one of the trickier aspects of Python, so it's okay if this is a bit confusing.
# It might prove helpful to find the similarities with JavaScript callbacks, as the following example illustrates:
# function login_required(func) {
#   function wrapped_function() {
#     console.log('wrapper');
#     // func(*args, **kwargs)
#     return func(...arguments);
#   }
#   return wrapped_function;
# }
# // @login_required
# // def callback():
# const callback = login_required(() => {
#   console.log('hello');
# });
# callback();
