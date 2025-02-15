import sqlite3
from pulp import LpMinimize, LpProblem, LpVariable
import matplotlib.pyplot as plt

# 1. SETUP DATABASE AND INSERT DATA
conn = sqlite3.connect("supply_chain.db")
cursor = conn.cursor()

# Create tables
cursor.executescript('''
CREATE TABLE IF NOT EXISTS storages (
    id INTEGER PRIMARY KEY,
    name TEXT,
    capacity INT
);

CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    supply INT,
    cost_per_unit FLOAT
);

CREATE TABLE IF NOT EXISTS demand (
    storage_id INT,
    product TEXT,
    demand_qty INT,
    FOREIGN KEY (storage_id) REFERENCES storages(id)
);
''')

# Insert sample data
cursor.executemany("INSERT INTO storages VALUES (?, ?, ?)", [
    (1, "Storage A", 500),
    (2, "Storage B", 400)
])

cursor.executemany("INSERT INTO suppliers VALUES (?, ?, ?, ?)", [
    (1, "Supplier X", 600, 5),
    (2, "Supplier Y", 300, 7)
])

cursor.executemany("INSERT INTO demand VALUES (?, ?, ?)", [
    (1, "Product 1", 400),
    (2, "Product 1", 300)
])

conn.commit()

# 2. FETCH DATA FROM DATABASE
cursor.execute("SELECT capacity FROM storages")
storage_capacities = [row[0] for row in cursor.fetchall()]

demand_total = sum(storage_capacities)
cursor.execute("SELECT supply, cost_per_unit FROM suppliers")
suppliers = cursor.fetchall()

# 3. OPTIMIZATION MODEL
model = LpProblem("Minimize_Shipping_Cost", LpMinimize)

# Decision variables
x1 = LpVariable("Ship_SupplierX_to_StorageA", lowBound=0, cat="Integer")
x2 = LpVariable("Ship_SupplierX_to_StorageB", lowBound=0, cat="Integer")
x3 = LpVariable("Ship_SupplierY_to_StorageA", lowBound=0, cat="Integer")
x4 = LpVariable("Ship_SupplierY_to_StorageB", lowBound=0, cat="Integer")

# Objective function: Minimize cost
model += suppliers[0][1] * (x1 + x2) + suppliers[1][1] * (x3 + x4)

# Constraints
model += x1 + x3 == storage_capacities[0]  # Storage A capacity
model += x2 + x4 == storage_capacities[1]  # Storage B capacity
model += x1 + x2 <= suppliers[0][0]  # Supplier X supply
model += x3 + x4 <= suppliers[1][0]  # Supplier Y supply

# Solve the problem
model.solve()

# 4. RESULTS
optimal_shipments = [x1.varValue, x2.varValue, x3.varValue, x4.varValue]
print("Optimal Shipments:")
print(f"Supplier X -> Storage A: {x1.varValue}")
print(f"Supplier X -> Storage B: {x2.varValue}")
print(f"Supplier Y -> Storage A: {x3.varValue}")
print(f"Supplier Y -> Storage B: {x4.varValue}")

# 5. DATA VISUALIZATION
storages = ["Storage A", "Storage B"]
shipments = [x1.varValue + x3.varValue, x2.varValue + x4.varValue]

plt.bar(storages, shipments, color=["blue", "green"])
plt.xlabel("Storage")
plt.ylabel("Units Shipped")
plt.title("Optimized Shipping Plan")
plt.show()

# Close DB connection
conn.close()
