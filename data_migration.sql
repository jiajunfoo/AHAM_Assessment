-- Insert Managers into the Manager table
INSERT INTO Manager (manager_name) 
VALUES 
('Alice'),
('Bob');

-- Insert Funds into the InvestmentFund table
INSERT INTO InvestmentFund (name, manager_id, description, nav, date_of_creation, performance) 
VALUES 
('Tech Fund 1', 2, 'A technology investment fund.', 2000.00, '2024-09-29', 1.5),
('Health Fund 2', 1, 'A healthcare investment fund.', 500000.00, '2024-09-29', 5.5);
