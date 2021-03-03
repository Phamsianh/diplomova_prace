
def decorator(func):
    def wrapper():
        func()
        func()
        return func
    return wrapper


# @decorator
def sayhi():
    print('Hi')


sayhi = decorator(sayhi)


# sayhi()
print(sayhi)
