from flask import Flask, jsonify, request, abort
from fund import db, InvestmentFund  # Import the SQLAlchemy instance and model
from datetime import datetime


# Configurations
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fund.db'

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True  # Enables testing mode

# Create the Flask app with the selected configuration
def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  # Initialize SQLAlchemy with the app

    # Create the database and tables
    with app.app_context():
        db.create_all()

    # Custom error handler for 404 (Not Found)
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    # Custom error handler for 400 (Bad Request)
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request", "message": str(error.description)}), 400

    # Custom error handler for 500 (Internal Server Error)
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    # Endpoint to retrieve a list of all funds
    @app.route('/funds', methods=['GET'])
    def get_funds():
        funds = InvestmentFund.query.all()
        return jsonify([fund.to_dict() for fund in funds]), 200

    # Endpoint to retrieve details of a specific fund using its ID
    @app.route('/funds/<int:fund_id>', methods=['GET'])
    def get_fund(fund_id):
        fund = InvestmentFund.query.get_or_404(fund_id)
        return jsonify(fund.to_dict()), 200

    # Endpoint to create a new fund
    @app.route('/funds', methods=['POST'])
    def create_fund():
        new_data = request.json
        # Check if all required fields are present in the request
        if not all(k in new_data for k in ('name', 'manager_name', 'description', 'nav', 'performance')):
            return jsonify({"error": "Missing required fields"}), 400

        # Validate that 'nav' and 'performance' are numbers
        try:
            nav = float(new_data['nav'])
            performance = float(new_data['performance'])
        except ValueError:
            return jsonify({"error": "NAV and performance must be numbers"}), 400

        # Default to the current date
        date_of_creation = new_data.get('date_of_creation', datetime.now().strftime('%Y-%m-%d'))

        # Create a new InvestmentFund instance (no need to manually assign 'fund_id')
        new_fund = InvestmentFund(
            name=new_data['name'],
            manager_name=new_data['manager_name'],
            description=new_data['description'],
            nav=nav,
            date_of_creation=date_of_creation,
            performance=performance
        )

        # Add the new fund to the database
        db.session.add(new_fund)
        db.session.commit()

        return jsonify(new_fund.to_dict()), 201

    # Endpoint to update the performance of a fund using its ID
    @app.route('/funds/<int:fund_id>', methods=['PUT'])
    def update_fund_performance(fund_id):
        fund = InvestmentFund.query.get_or_404(fund_id)

        data = request.json

        if 'performance' not in data:
            return jsonify({'message': 'Missing performance field'}), 400

        try:
            fund.performance = float(data['performance'])
        except ValueError:
            return jsonify({'message': "Invalid 'performance' value. Must be a number."}), 400

        db.session.commit()
        return jsonify(fund.to_dict()), 200

    # Endpoint to delete a fund using its ID
    @app.route('/funds/<int:fund_id>', methods=['DELETE'])
    def delete_fund(fund_id):
        fund = InvestmentFund.query.get_or_404(fund_id)

        db.session.delete(fund)
        db.session.commit()

        return jsonify({'message': 'Fund deleted successfully'}), 200

    return app


app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run(debug=True)
