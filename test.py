class major():
    x = 1


class minor(major):
    pass


print(major.x, minor.x)

minor.x = 2

print(major.x, minor.x)

major.x = 3

print(major.x, minor.x)
