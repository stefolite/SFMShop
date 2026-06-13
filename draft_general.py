class Descriptor:
    def __get__(self, instance, owner):
        print("__get__")
        return 123


class User:
    age = Descriptor()


u = User()
print(u.age)
print(User.__dict__)