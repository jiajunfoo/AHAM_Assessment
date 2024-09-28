from collections import OrderedDict
class InvestmentFund:
    def __init__(self, fund_id, name, manager_name, description, nav, date_of_creation, performance):
        """
        Initializes an InvestmentFund instance with the provided attributes.
        
        :param fund_id: Unique identifier for the fund.
        :param name: Name of the fund.
        :param manager_name: Name of the fund manager.
        :param description: Description of the fund.
        :param nav: Net Asset Value (NAV) of the fund.
        :param date_of_creation: Date when the fund was created.
        :param performance: Performance of the fund as a percentage.
        """
        
        self.fund_id = fund_id
        self.name = name
        self.manager_name = manager_name
        self.description = description
        self.nav = nav
        self.date_of_creation = date_of_creation
        self.performance = performance
        
    def update_performance(self, new_performance):
        """
        Updates the performance of the fund.
        
        :param performance = new_performance
        """
        
        self.performance = new_performance
        
    def to_dict(self):
        """
        Converts the InvestmentFund instance to a dictionary.
        
        :return: A dictionary representation of the InvestmentFund instance. 
        """
        
        return OrderedDict([
            ('fund_id', self.fund_id),
            ('name', self.name),
            ('manager_name', self.manager_name),
            ('description', self.description),
            ('nav', self.nav),
            ('date_of_creation', self.date_of_creation),
            ('performance', self.performance)
        ])
        
    
    def __repr__(self):
        """
        Returns a string representation of the InvestmentFund object.
        """
        
        return f"Fund({self.fund_id}, {self.name}, {self.manager_name}, NAV: {self.nav}, Performance: {self.performance}%)"
        
    
