# Inventory Optimization

This project optimizes supply chain logistics by minimizing transportation costs between suppliers and storage facilities using Linear Programming (LP). The optimization is performed with **PuLP**, and **SQLite** is used to manage supply and demand data.

## Features
- **Database Setup:** SQLite database to store supplier, storage, and demand data.
- **Optimization Model:** Linear programming using PuLP to minimize transportation costs.
- **Data Visualization:** Bar charts to visualize the optimized shipping plan.
- **Scalability:** Easily adaptable to larger datasets and more complex constraints.

## Requirements
Ensure you have the following dependencies installed:
```sh
pip install pulp matplotlib sqlite3
```

## How to Run
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/supply-chain-optimization.git
   cd supply-chain-optimization
   ```
2. Run the Python script:
   ```sh
   python supply_chain_optimization.py
   ```
3. The results will be displayed in the console and as a visualization.

## Database Structure
- **storages**: Stores storage capacities.
- **suppliers**: Stores available supply and cost per unit.
- **demand**: Stores product demand by storage location.

## Results
The script computes optimal shipment quantities to minimize costs and provides a bar chart visualization of the optimized plan.

## Contributors
- Yeva Butovska ([email](mailto:yevabutovska@gmail.com))

