import streamlit as st
from database import create_tables
from models import Vehicle, Buyer, Sale

st.set_page_config(page_title="Salvage System", layout="wide")
create_tables()

# LOGIN CHECK
from auth import login

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# MAIN APP

st.title("Motor Vehicle Insurance Salvage Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Add Vehicle", "Add Buyer",
     "Record Sale", "View Vehicles", "View Buyers", "View Sales"]
)

vehicle = Vehicle()
buyer = Buyer()
sale = Sale()

# DASHBOARD

if menu == "Dashboard":
    vehicles = vehicle.get_all()
    sales = sale.get_sales()

    total_purchase = vehicles["purchase_price"].sum() if not vehicles.empty else 0
    total_sales = sales["sale_price"].sum() if not sales.empty else 0
    total_profit = sales["profit"].sum() if not sales.empty else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Purchase", total_purchase)
    col2.metric("Total Sales", total_sales)
    col3.metric("Total Profit", total_profit)

    if not sales.empty:
        st.bar_chart(sales.set_index("registration_number")["profit"])


# ADD VEHICLE

elif menu == "Add Vehicle":

    data = (
        st.text_input("Insurance Company"),
        st.text_input("Previous Owner"),
        st.text_input("Contact"),
        st.text_input("Logbook Number"),
        st.text_input("Registration Number"),
        st.text_input("Make"),
        st.text_input("Model"),
        st.number_input("Year", min_value=1990, max_value=2026),
        st.text_input("Damage Type"),
        st.number_input("Purchase Price", min_value=0.0)
    )

    if st.button("Save Vehicle"):
        vehicle.add_vehicle(data)
        st.success("Vehicle added successfully")

# ADD BUYER

elif menu == "Add Buyer":

    data = (
        st.text_input("Full Name"),
        st.text_input("Phone Number"),
        st.text_input("ID Number")
    )

    if st.button("Save Buyer"):
        buyer.add_buyer(data)
        st.success("Buyer added successfully")



# RECORD SALE

elif menu == "Record Sale":

    vehicles = vehicle.get_all()
    buyers = buyer.get_all()

    available = vehicles[vehicles["status"] == "Available"]

    vehicle_id = st.selectbox(
        "Select Vehicle",
        available["vehicle_id"],
        format_func=lambda x:
        available[available["vehicle_id"] == x]["registration_number"].values[0]
    )

    buyer_id = st.selectbox(
        "Select Buyer",
        buyers["buyer_id"],
        format_func=lambda x:
        buyers[buyers["buyer_id"] == x]["full_name"].values[0]
    )

    sale_price = st.number_input("Sale Price", min_value=0.0)

    if st.button("Confirm Sale"):
        sale.record_sale(vehicle_id, buyer_id, sale_price)
        st.success("Sale recorded successfully")


# VIEW VEHICLES

elif menu == "View Vehicles":
    df = vehicle.get_all()
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), "vehicles.csv")


# VIEW BUYERS

elif menu == "View Buyers":
    df = buyer.get_all()
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), "buyers.csv")

# VIEW SALES
elif menu == "View Sales":
    df = sale.get_sales()
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), "sales.csv")