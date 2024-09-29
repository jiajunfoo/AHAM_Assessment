from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

class Manager(db.Model):
    __tablename__ = 'managers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    
# Define the InvestmentFund model
class InvestmentFund(db.Model):
    __tablename__ = 'funds'
    
    fund_id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing ID
    name = db.Column(db.String(100), nullable=False, unique=True)  # Fund name
    manager_name = db.Column(db.String(255), nullable=False)  # Manager's name
    description = db.Column(db.String(255), nullable=False)  # Fund description
    nav = db.Column(db.Float, nullable=False)  # Net Asset Value
    date_of_creation = db.Column(db.String(20), default=datetime.now().strftime('%Y-%m-%d'))  # Default to current date
    performance = db.Column(db.Float, nullable=False)  # Performance percentage

    def to_dict(self):
        """
        Converts the InvestmentFund instance to a dictionary.
        
        :return: A dictionary representation of the InvestmentFund instance.
        """
        return {
            'fund_id': self.fund_id,
            'name': self.name,
            'manager_name': self.manager_name,
            'description': self.description,
            'nav': self.nav,
            'date_of_creation': self.date_of_creation,
            'performance': self.performance
        }

    def __repr__(self):
        """
        Returns a string representation of the InvestmentFund object.
        """
        return f"Fund({self.fund_id}, {self.name}, {self.manager_name}, NAV: {self.nav}, Performance: {self.performance}%)"
