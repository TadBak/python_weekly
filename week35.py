from abc import ABCMeta, abstractmethod
import typing

class AbstractPayment(metaclass=ABCMeta):

    @abstractmethod
    def authorize_payment(self, user_id: int, amount: int, currency: str) -> bool:
        pass

    @abstractmethod
    def charge_payment(self, user_id: int, amount: int, currency: str,
                       merchant_id: int) -> int:
        """ The method should raise CannontChargeError exception if transaction
        can not proceed """ 
        pass

    @abstractmethod
    def reverse_payment(self, user_id: int, amount: int, currency: str,
                        merchant_id: int) -> int:
        """ The method should raise CannotReverseError exception if transaction
        can not proceed """ 
        pass
    

class CannotChargeError(Exception):
    pass


class CannotReverseError(Exception):
    pass


class MyNewPayment1(AbstractPayment):

    def authorize_payment(self, num):
        return num+5

    def charge_payment(self):
        pass

    def reverse_payment(self):
        pass


class MyNewPayment2(AbstractPayment):

    def authorize_payment(self, user_id: int, amount: int, currency: str) -> bool:
        return True

    def charge_payment(self, user_id: int, amount: int, currency: str,
                       merchant_id: int) -> int:
        if amount < 0:
            raise CannotChargeError()
        return 1

    def reverse_payment(self, user_id: int, amount: int, currency: str,
                        merchant_id: int) -> int:
        if amount < 0:
            raise CannotReverseError()
        return 1


mnp1 = MyNewPayment1()
print(f'MyNewPayment1 object created, method output: {mnp1.authorize_payment(2)}')
mnp2 = MyNewPayment2()
result = mnp2.authorize_payment(1, 20, 'AUD')
print(f'MyNewPayment2 object created, method output: {result}')

