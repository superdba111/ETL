A decorator in Python is a callable (function, method, or class) that is used to modify or enhance a function or method. A decorator is passed the original object being defined and returns a modified object, which is then bound to the name in the definition.
(the complete guide--https://www.youtube.com/watch?v=QH5fw9kxDQA)

Here's a basic example of a decorator:

def simple_decorator(function):
    def wrapper():
        print("Before the function call")
        function()
        print("After the function call")
    return wrapper

@simple_decorator
def hello():
    print("Hello, world!")

hello()
In this example, the @simple_decorator before the hello() function is equivalent to hello = simple_decorator(hello).

When hello() is called, it's now the wrapper() function that gets executed. Inside the wrapper() function, you can execute code before or after the original function call.

Some best practices when using decorators include:

Preserve the Metadata: Decorators replace functions, which can lose some of the metadata of the original function. The functools.wraps decorator can be used in your decorator definition to copy the lost metadata.

import functools

def simple_decorator(function):
    @functools.wraps(function)
    def wrapper():
        print("Before the function call")
        function()
        print("After the function call")
    return wrapper

## Avoid mutable arguments: Decorators are run only once (at definition time), so if you use mutable default arguments, they can persist state between different functions or method calls, which is usually not what you want.

## Use class-based decorators for greater flexibility: If you need a decorator that can maintain state or be configured by arguments, you may want to use a class-based decorator instead.

## Remember that decorators execute at definition time, not runtime: When you decorate a function, the decorator's logic runs immediately. This can be surprising if you're not used to it.

## Use decorators sparingly: While decorators can be powerful and can make your code more concise, they can also make your code harder to read if they're overused or complex.

## Document your decorators: As decorators can change the behavior of the functions they decorate, it's important to document both what your decorator does and how it should be used.





