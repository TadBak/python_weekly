from abc import ABC, abstractmethod

class AbstractPayment(ABC):

    @abstractmethod
    def authorize_payment(self, user_id, amount, currency):
        """ returns True or False """

    @abstractmethod
    def charge_payment(self, user_id, amount, currency, merchant_id):
        """ returns a transaction ID number or raises CannotCharge """

    @abstractmethod
    def reverse_payment(self, user_id, amount, currency, merchant_id):
        """ returns a transaction ID number or raises CannotReverse """
    

class MyNewPayment1(AbstractPayment):

    def authorize_payment(self):
        pass

    def charge_payment(self):
        pass

    def reverse_payment(self):
        pass


class MyNewPayment2(AbstractPayment):
    pass


mnp = MyNewPayment1()                   # this works fine
print('MyNewPayment1 object created')
mnp = MyNewPayment2()                   # this raises TypeError
print('MyNewPayment2 object created')
