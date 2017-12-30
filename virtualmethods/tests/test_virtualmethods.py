from virtualmethods import (virtual_methods,
                            virtual_method, non_virtual_method,
                            VIRTUAL, NON_VIRTUAL)


# NON-VIRTUAL classes

class A(object):
    __metaclass__ = virtual_methods(default=NON_VIRTUAL)

    def __init__(self):
        pass

    @property
    def secret(self):
        return [A]

    @secret.setter
    def secret(self, value):
        value.append(A)

    def get_secret(self):
        return [A.get_secret] + self.secret

    def set_secret(self, value):
        value.append(A.set_secret)
        self.secret = value

    @virtual_method
    def regular_fun1(self):
        return [A.regular_fun1]

    def regular_fun2(self):
        return [A.regular_fun2] + self.regular_fun1()

    def non_virtual_fun1(self):
        return [A.non_virtual_fun1]

    def non_virtual_fun2(self):
        return [A.non_virtual_fun2] + self.non_virtual_fun1()

    def enter_inner(self):
        return [A.enter_inner]

    def __enter__(self):
        return [A.__enter__] + self.enter_inner()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self, *args, **kwargs):
        return [A.__call__]

    def call(self):
        return [A.call] + self()

    @staticmethod
    def static_fun1():
        return [A.static_fun1]

    def static_fun2(self):
        return [A.static_fun2] + self.static_fun1()


class B(A):
    def __init__(self):
        super(B, self).__init__()

    @property
    def secret(self):
        return [B]

    @secret.setter
    def secret(self, value):
        value.append(B)

    def get_secret(self):
        rv = super(B, self).get_secret()
        return [B.get_secret] + self.secret + rv

    def set_secret(self, value):
        value.append(B.set_secret)
        self.secret = value
        super(B, self).set_secret(value)

    @virtual_method
    def regular_fun1(self):
        return [B.regular_fun1]

    def regular_fun2(self):
        rv = super(B, self).regular_fun2()
        return [B.regular_fun2] + self.regular_fun1() + rv

    def non_virtual_fun1(self):
        return [B.non_virtual_fun1]

    def non_virtual_fun2(self):
        rv = super(B, self).non_virtual_fun2()
        return [B.non_virtual_fun2] + self.non_virtual_fun1() + rv

    def enter_inner(self):
        return [B.enter_inner]

    def __enter__(self):
        rv = super(B, self).__enter__()
        return [B.__enter__] + self.enter_inner() + rv

    def __call__(self, *args, **kwargs):
        return [B.__call__]

    def call(self):
        rv = super(B, self).call()
        return [B.call] + self() + rv

    @staticmethod
    def static_fun1():
        return [B.static_fun1]

    def static_fun2(self):
        rv = super(B, self).static_fun2()
        return [B.static_fun2] + self.static_fun1() + rv


class C(B):
    def __init__(self):
        super(C, self).__init__()

    @property
    def secret(self):
        return [C]

    @secret.setter
    def secret(self, value):
        value.append(C)

    def regular_fun1(self):
        return [C.regular_fun1]

    def non_virtual_fun1(self):
        return [C.non_virtual_fun1]

    def enter_inner(self):
        return [C.enter_inner]

    def __call__(self, *args, **kwargs):
        return [C.__call__]

    @staticmethod
    def static_fun1():
        return [C.static_fun1]


# VIRTUAL classes

class X(object):
    __metaclass__ = virtual_methods(default=VIRTUAL)

    def __init__(self):
        pass

    @property
    @non_virtual_method
    def secret(self):
        return [X]

    @secret.setter
    @non_virtual_method
    def secret(self, value):
        value.append(X)

    def get_secret(self):
        return [X.get_secret] + self.secret

    def set_secret(self, value):
        value.append(X.set_secret)
        self.secret = value

    def regular_fun1(self):
        return [X.regular_fun1]

    def regular_fun2(self):
        return [X.regular_fun2] + self.regular_fun1()

    @non_virtual_method
    def non_virtual_fun1(self):
        return [X.non_virtual_fun1]

    def non_virtual_fun2(self):
        return [X.non_virtual_fun2] + self.non_virtual_fun1()

    @non_virtual_method
    def enter_inner(self):
        return [X.enter_inner]

    def __enter__(self):
        return [X.__enter__] + self.enter_inner()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @non_virtual_method
    def __call__(self, *args, **kwargs):
        return [X.__call__]

    def call(self):
        return [X.call] + self()


class Y(X):
    def __init__(self):
        super(Y, self).__init__()

    @property
    @non_virtual_method
    def secret(self):
        return [Y]

    @secret.setter
    @non_virtual_method
    def secret(self, value):
        value.append(Y)

    def get_secret(self):
        rv = super(Y, self).get_secret()
        return [Y.get_secret] + self.secret + rv

    def set_secret(self, value):
        value.append(Y.set_secret)
        self.secret = value
        super(Y, self).set_secret(value)

    def regular_fun1(self):
        return [Y.regular_fun1]

    def regular_fun2(self):
        rv = super(Y, self).regular_fun2()
        return [Y.regular_fun2] + self.regular_fun1() + rv

    @non_virtual_method
    def non_virtual_fun1(self):
        return [Y.non_virtual_fun1]

    def non_virtual_fun2(self):
        rv = super(Y, self).non_virtual_fun2()
        return [Y.non_virtual_fun2] + self.non_virtual_fun1() + rv

    @non_virtual_method
    def enter_inner(self):
        return [Y.enter_inner]

    def __enter__(self):
        rv = super(Y, self).__enter__()
        return [Y.__enter__] + self.enter_inner() + rv

    @non_virtual_method
    def __call__(self, *args, **kwargs):
        return [Y.__call__]

    def call(self):
        rv = super(Y, self).call()
        return [Y.call] + self() + rv


class Z(Y):
    def __init__(self):
        super(Z, self).__init__()

    @property
    @non_virtual_method
    def secret(self):
        return [Z]

    @secret.setter
    @non_virtual_method
    def secret(self, value):
        value.append(Z)

    def regular_fun1(self):
        return [Z.regular_fun1]

    @non_virtual_method
    def non_virtual_fun1(self):
        return [Z.non_virtual_fun1]

    @non_virtual_method
    def enter_inner(self):
        return [Z.enter_inner]

    @non_virtual_method
    def __call__(self, *args, **kwargs):
        return [Z.__call__]


# tests for default NON-VIRTUAL methods

def test_regular_method_call():
    instance = C()
    assert [B.regular_fun2,
            C.regular_fun1,
            A.regular_fun2,
            C.regular_fun1] == instance.regular_fun2()


def test_non_virtual_method_call():
    instance = C()
    assert [B.non_virtual_fun2,
            B.non_virtual_fun1,
            A.non_virtual_fun2,
            A.non_virtual_fun1] == instance.non_virtual_fun2()


def test_context_call():
    with C() as calling_chain:
        pass
    assert [B.__enter__,
            B.enter_inner,
            A.__enter__,
            A.enter_inner] == calling_chain


def test_dunder_call():
    instance = C()
    assert [B.call,
            B.__call__,
            A.call,
            A.__call__] == instance.call()


def test_property_getting():
    instance = C()
    assert [B.get_secret,
            B,
            A.get_secret,
            A] == instance.get_secret()


def test_property_setting():
    instance = C()
    lst = []
    instance.set_secret(lst)
    assert [B.set_secret,
            B,
            A.set_secret,
            A] == lst


def test_static_method():
    instance = C()
    assert [B.static_fun2,
            B.static_fun1,
            A.static_fun2,
            A.static_fun1] == instance.static_fun2()


# tests for default VIRTUAL methods (regular Python behaviour)

def test_virtual_regular_method_call():
    instance = Z()
    assert [Y.regular_fun2,
            Z.regular_fun1,
            X.regular_fun2,
            Z.regular_fun1] == instance.regular_fun2()


def test_virtual_non_virtual_method_call():
    instance = Z()
    assert [Y.non_virtual_fun2,
            Y.non_virtual_fun1,
            X.non_virtual_fun2,
            X.non_virtual_fun1] == instance.non_virtual_fun2()


def test_virtual_context_call():
    with Z() as calling_chain:
        pass
    assert [Y.__enter__,
            Y.enter_inner,
            X.__enter__,
            X.enter_inner] == calling_chain


def test_virtual_dunder_call():
    instance = Z()
    assert [Y.call,
            Y.__call__,
            X.call,
            X.__call__] == instance.call()


def test_virtual_property_getting():
    instance = Z()
    assert [Y.get_secret,
            Y,
            X.get_secret,
            X] == instance.get_secret()


def test_virtual_property_setting():
    instance = Z()
    lst = []
    instance.set_secret(lst)
    assert [Y.set_secret,
            Y,
            X.set_secret,
            X] == lst
