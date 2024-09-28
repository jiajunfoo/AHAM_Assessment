from flask import Flask, jsonify, request, abort
from fund import InvestmentFund
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# In-memory storage for funds
funds = {}

# Endpoint to retrieve a list of all funds
@app.route('/funds', methods=['GET'])
def get_funds():
    return jsonify([fund.to_dict() for fund in funds.values()])

# Endpoint to retrieve details of a specific fund using its ID
@app.route('/funds/<int:fund_id>', methods=['GET'])
def get_fund(fund_id):
    fund = funds.get(fund_id)
    if not fund:
        abort(404, description='Fund not found')
    return jsonify(fund.to_dict())

# Endpoint to create a new fund
@app.route('/funds', methods=['POST'])
def create_fund():
    new_data = request.json
    # Check if all required fields are present in the request
    if not all(k in new_data for k in ('name', 'manager_name', 'description', 'nav', 'performance')):
        abort(400, description="Missing fields")
        
    # Validate that 'nav' and 'performance' are numbers
    try:
        nav = float(new_data['nav'])
        performance = float(new_data['performance'])
    except ValueError:
        abort(400, description="Invalid 'nav' or 'performance' value. Must be a number.")
    
    # Generate a new fund_id based on the current highest id
    if funds:
        fund_id = max(funds.keys()) + 1  # Auto-increment
    else:
        fund_id = 1  # First fund gets ID 1
    
    # Default to the current date
    date_of_creation = new_data.get('date_of_creation', datetime.now().strftime('%Y-%m-%d'))
    
    # Create a new InvestmentFund instance
    new_fund = InvestmentFund(
        fund_id = fund_id,
        name = new_data['name'],
        manager_name = new_data['manager_name'],
        description = new_data['description'],
        nav = nav,
        date_of_creation = date_of_creation,
        performance = performance
    )
    
    # Add the new fund to the in-memory storage
    funds[fund_id] = new_fund
    return jsonify(new_fund.to_dict()), 201

# Endpoint to update the performance of a fund using its ID
@app.route('/funds/<int:fund_id>', methods=['PUT'])
def update_fund_performance(fund_id):
    data = request.json
    fund = funds.get(fund_id)
    
    if not fund:
        abort(404, description="Fund not found")
    
    if 'performance' not in data:
        abort(400, description="Missing performance field")
    
    try:
        performance = float(data['performance'])
    except ValueError:
        abort(400, description="Invalid 'performance' value. Must be a number.")
    
    fund.update_performance(performance)
    return jsonify(fund.to_dict())



# Endpoint to delete a fund using its ID
@app.route('/funds/<int:fund_id>', methods=['DELETE'])
def delete_fund(fund_id):
    if fund_id not in funds:
        abort(404, description="Fund not found")
        
    del funds[fund_id]
    return jsonify({'message': 'Fund deleted successfully'}), 200



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)