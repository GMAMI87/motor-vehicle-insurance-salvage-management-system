from database import get_connection
import pandas as pd
from datetime import datetime

# VEHICLE
class Vehicle:

    def add_vehicle(self, data):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO vehicles 
            (insurance_company, previous_owner, contact, logbook_number,
             registration_number, make, model, year, damage_type, purchase_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

        conn.commit()
        conn.close()

    def get_all(self):
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM vehicles", conn)
        conn.close()
        return df

# BUYER

class Buyer:

    def add_buyer(self, data):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO buyers (full_name, phone_number, id_number)
            VALUES (?, ?, ?)
        """, data)

        conn.commit()
        conn.close()

    def get_all(self):
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM buyers", conn)
        conn.close()
        return df


# SALE

class Sale:

    def record_sale(self, vehicle_id, buyer_id, sale_price):
        conn = get_connection()
        cursor = conn.cursor()

        sale_date = datetime.now().strftime("%Y-%m-%d")

        # Insert sale
        cursor.execute("""
            INSERT INTO sales (vehicle_id, buyer_id, sale_price, sale_date)
            VALUES (?, ?, ?, ?)
        """, (vehicle_id, buyer_id, sale_price, sale_date))

        # Update vehicle status
        cursor.execute("""
            UPDATE vehicles
            SET status = 'Sold'
            WHERE vehicle_id = ?
        """, (vehicle_id,))

        conn.commit()
        conn.close()

    def get_sales(self):
        conn = get_connection()

        df = pd.read_sql_query("""
            SELECT s.sale_id,
                   v.registration_number,
                   b.full_name,
                   v.purchase_price,
                   s.sale_price,
                   (s.sale_price - v.purchase_price) AS profit,
                   s.sale_date
            FROM sales s
            JOIN vehicles v ON s.vehicle_id = v.vehicle_id
            JOIN buyers b ON s.buyer_id = b.buyer_id
        """, conn)

        conn.close()
        return df