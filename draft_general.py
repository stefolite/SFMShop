class A:
    def method(self):
        print('A.method()')


class B(A):
    def method(self):
        print('B.method()')
        super().method()


class C(A):
    def method(self):
        print('C.method()')
        super().method()


class D(B, C):
    def method(self):
        print('D.method()')
        super().method()


if __name__ == '__main__':
    print(D.mro())
    d = D()
    d.method()

    # [<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]
    # D.method()
    # B.method()
    # C.method()
    # A.method()

    # методы вызываются согласно порядку в MRO.
    # таким образом, с помощью super()
    # решена проблема ромбовидного наследования,
    # и method() класса A вызывается только однократно
