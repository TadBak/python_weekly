import arrow
from decimal import Decimal

class Loan:
    """Simple bank loan representation."""

    def __init__(self, amount, interest, starts_on = None):
        """Initialisation of Loan object.

        Parameters
        ----------
        amount : float or numeric string
            The amount of borrowed money.
        interest : float or numeric string
            Interest rate per annum, expressed as a fraction, not a percent
        starts_on : string (optional)
            First day of the loan period, default is the current day. If supplied
            this parameter must be in the format: yyyy-mm-dd

        Returns
        -------
        None

        Exceptions
        ----------
        TypeError
            Raised when arguments: amount and/or interest are not numbers nor
            numeric strings
        arrow.parser.ParserError
            Raised when the argument: starts_on does not conform to specified
            format.        
        """

        self.amount = Decimal(str(amount))
        self.interest = Decimal(str(interest))
        # mixing Decimals with integers is OK
        self.daily_interest = self.interest * self.amount / 365
        if starts_on is None:
            self.starts_on = arrow.now().floor('day')
        else:
            self.starts_on = arrow.get(starts_on, 'YYYY-MM-DD')

    def total_on(self, ends_on):
        """Calculates total amount owed on a given day.

        It is assumed that no repayments have been made, therefore the calculated
        amount is the sum of principal and interest.

        Parameters
        ----------
        ends_on : string
            Date in the format: yyyy-mm-dd for which the total is calculated.

        Returns
        -------
        float
            Total amount owed.

        Exceptions
        ----------
        arrow.parser.ParserError
            Raised when the argument: ends_on does not conform to specified
            format.        
        """

        days = (arrow.get(ends_on, 'YYYY-MM-DD') - self.starts_on).days
        return (0.0 if days < 0 else 
                float(round(self.daily_interest * days + self.amount, 2)))

    def total_on_each(self, starts_on, ends_on):
        """Calculates amount owed for every day within given period.

        It is assumed that no repayments have been made, therefore the calculated
        amount is the sum of principal and interest.

        Parameters
        ----------
        starts_on, ends_on : string
            First and last day of the time period. Both dates are in the
            format: yyyy-mm-dd 

        Returns
        -------
        list of tuples
            Each tuple contain a string representing the date and a float
            representing the amount owed on that day.

        Exceptions
        ----------
        arrow.parser.ParserError
            Raised when the arguments: starts_on and/or ends_on do not conform
            to specified format.       
        """

        starts_on = arrow.get(starts_on, 'YYYY-MM-DD')
        ends_on = arrow.get(ends_on, 'YYYY-MM-DD')
        days = (starts_on - self.starts_on).days
        period = (ends_on - starts_on).days
        return [(starts_on.shift(days = i).format(fmt = 'D MMM YYYY'), 
                0.0 if days + i < 0 else 
                float(round(self.daily_interest * (days + i) + self.amount, 2)))
                for i in range(period + 1)]


        

