import sqlite3

# Connect to the database
conn = sqlite3.connect(r"C:\Users\dell\Desktop\Elevate labs\task3\olist.sqlite")
cursor = conn.cursor()

# Execute all queries step by step
# a. SELECT, WHERE, ORDER BY, GROUP BY
cursor.execute("""
    SELECT seller_id, COUNT(order_id) AS total_orders
    FROM order_items
    GROUP BY seller_id
    HAVING COUNT(order_id) > 5
    ORDER BY total_orders DESC
    LIMIT 5
""")
print("\na) Top 5 sellers with more than 5 orders:")
for row in cursor.fetchall():
    print(row)

# b. INNER JOIN
cursor.execute("""
    SELECT oi.order_id, s.seller_city, s.seller_state
    FROM order_items oi
    INNER JOIN sellers s ON oi.seller_id = s.seller_id
    LIMIT 5
""")
print("\nb) INNER JOIN (order_items + sellers):")
for row in cursor.fetchall():
    print(row)

# b. LEFT JOIN
cursor.execute("""
    SELECT c.customer_id, o.order_id
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LIMIT 5
""")
print("\nb) LEFT JOIN (customers + orders):")
for row in cursor.fetchall():
    print(row)

# c. Subquery
cursor.execute("""
    SELECT seller_id
    FROM sellers
    WHERE seller_id IN (
        SELECT seller_id
        FROM order_items
        GROUP BY seller_id
        HAVING COUNT(order_id) > 10
    )
    LIMIT 5
""")
print("\nc) Sellers with >10 orders (via subquery):")
for row in cursor.fetchall():
    print(row)

# d. Aggregate (AVG)
cursor.execute("""
    SELECT seller_id, AVG(freight_value) AS avg_freight
    FROM order_items
    GROUP BY seller_id
    ORDER BY avg_freight DESC
    LIMIT 5
""")
print("\nd) Top 5 sellers by average freight:")
for row in cursor.fetchall():
    print(row)

# e. Create and query view
cursor.execute("DROP VIEW IF EXISTS seller_sales_summary")
cursor.execute("""
    CREATE VIEW seller_sales_summary AS
    SELECT seller_id,
           COUNT(order_id) AS total_orders,
           SUM(price + freight_value) AS total_revenue
    FROM order_items
    GROUP BY seller_id
""")
cursor.execute("""
    SELECT * FROM seller_sales_summary
    ORDER BY total_revenue DESC
    LIMIT 5
""")
print("\ne) View: seller_sales_summary (Top 5 by revenue):")
for row in cursor.fetchall():
    print(row)

# f. Index creation
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_order_items_seller_id ON order_items(seller_id)
""")
print("\nf) Index created successfully.")

conn.close()
