import streamlit as st
import pandas as pd
from os import path
import pickle



# Load model
with open("Data/tuned_random_forest.pkl", "rb") as file:
    model = pickle.load(file)
#st.title('📦 Supply Chain Delivery Schedule Prediction App')

st.markdown(
    "<h1 style='text-align: center; color: #1F4E79;'>🚚 Supply Chain Delivery Schedule Prediction</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; font-size:18px;'>AI-Powered Logistics Date Prediction System</p>",
    unsafe_allow_html=True
)
st.subheader("Enter Shipment Details")


scheduled_days = st.selectbox(
    "Days for shipment (scheduled)",
    [1, 2, 3, 4, 5, 6]
)

latitude = st.number_input(
    "Latitude",
    min_value=-33.94,
    max_value=48.79,
    format="%.6f"
)

longitude = st.number_input(
    "Longitude",
    min_value=-158.03,
    max_value=115.27,
    format="%.6f"
)
dept_id = st.number_input("Department Id", min_value=2,
    max_value=12,
    step=1)



shipping_mode = st.selectbox("Shipping Mode", ['Standard Class', 'First Class', 'Second Class', 'Same Day'])

market = st.selectbox("Market", ['Pacific Asia', 'USCA', 'Africa', 'Europe', 'LATAM'])

shipping_date = st.date_input(
    "Shipping Date (DateOrders)",
    min_value=pd.to_datetime("2015-01-01"),
    max_value=pd.to_datetime("2018-12-31")
)

Order_Region = st.selectbox('Order Region',['Southeast Asia', 'South Asia', 'Oceania', 'Eastern Asia',
       'West Asia', 'West of USA ', 'US Center ', 'West Africa',
       'Central Africa', 'North Africa', 'Western Europe',
       'Northern Europe', 'Central America', 'Caribbean', 'South America',
       'East Africa', 'Southern Europe', 'East of USA', 'Canada',
       'Southern Africa', 'Central Asia', 'Eastern Europe',
       'South of  USA '])


year = shipping_date.year
month = shipping_date.month
day = shipping_date.day

weekday = shipping_date.strftime("%A")

# -------- Shipping Mode Dummies --------
shipping_same_day = 1 if shipping_mode == "Same Day" else 0
shipping_second = 1 if shipping_mode == "Second Class" else 0
shipping_standard = 1 if shipping_mode == "Standard Class" else 0
# No First Class — because model doesn't have it.

# -------- Market Dummies --------
market_europe = 1 if market == "Europe" else 0
market_latam = 1 if market == "LATAM" else 0
market_pacific = 1 if market == "Pacific Asia" else 0
market_usca = 1 if market == "USCA" else 0



# -------- Weekday Dummies --------
weekday_dict = {
    "Monday":0,
    "Saturday":0,
    "Sunday":0,
    "Thursday":0,
    "Tuesday":0,
    "Wednesday":0,
    'Friday':0
}

weekday_dict[weekday] = 1

region_dict = {
    'Caribbean':0,
    'Central Africa':0,
    'Central America':0,
    'Central Asia':0,
    'East Africa':0,
    'East of USA':0,
    'Eastern Asia':0,
    'Eastern Europe':0,
    'North Africa':0,
    'Northern Europe':0,
    'Oceania':0,
    'South America':0,
    'South Asia':0,
    'South of  USA ':0,
    'Southeast Asia':0,
    'Southern Africa':0,
    'Southern Europe':0,
    'US Center ':0,
    'West Africa':0,
    'West Asia':0,
    'West of USA ':0,
    'Western Europe':0
}

region_dict[Order_Region] = 1



#-------Input DataFrame-----------
input_data = pd.DataFrame([{
    "Days for shipment (scheduled)": scheduled_days,
    
    "Latitude": latitude,
    "Longitude": longitude,
    "Department Id": dept_id,
    "shipping_year": year,
    "shipping_month": month,
    "shipping_day": day,

    "Shipping Mode_Same Day": shipping_same_day,
    "Shipping Mode_Second Class": shipping_second,
    "Shipping Mode_Standard Class": shipping_standard,

    "Market_Europe": market_europe,
    "Market_LATAM": market_latam,
    "Market_Pacific Asia": market_pacific,
    "Market_USCA": market_usca,


    "shipping_weekdays_Monday": weekday_dict["Monday"],
    "shipping_weekdays_Saturday": weekday_dict["Saturday"],
    "shipping_weekdays_Sunday": weekday_dict["Sunday"],
    "shipping_weekdays_Thursday": weekday_dict["Thursday"],
    "shipping_weekdays_Tuesday": weekday_dict["Tuesday"],
    "shipping_weekdays_Wednesday": weekday_dict["Wednesday"],

    "Order Region_Caribbean": region_dict["Caribbean"],
    "Order Region_Central Africa": region_dict["Central Africa"],
    "Order Region_Central America": region_dict["Central America"],
    "Order Region_Central Asia": region_dict["Central Asia"],
    "Order Region_East Africa": region_dict["East Africa"],
    "Order Region_East of USA": region_dict["East of USA"],
    "Order Region_Eastern Asia": region_dict["Eastern Asia"],
    "Order Region_Eastern Europe": region_dict["Eastern Europe"],
    "Order Region_North Africa": region_dict["North Africa"],
    "Order Region_Northern Europe": region_dict["Northern Europe"],
    "Order Region_Oceania": region_dict["Oceania"],
    "Order Region_South America": region_dict["South America"],
    "Order Region_South Asia": region_dict["South Asia"],
    "Order Region_South of  USA ": region_dict["South of  USA "],
    "Order Region_Southeast Asia": region_dict["Southeast Asia"],
    "Order Region_Southern Africa": region_dict["Southern Africa"],
    "Order Region_Southern Europe": region_dict["Southern Europe"],
    "Order Region_US Center ": region_dict["US Center "],
    "Order Region_West Africa": region_dict["West Africa"],
    "Order Region_West Asia": region_dict["West Asia"],
    "Order Region_West of USA ": region_dict["West of USA "],
    "Order Region_Western Europe": region_dict["Western Europe"]
}])


#--------Prediction Button----------
predict_btn = st.button("🚚 Predict Delivery Time", use_container_width=True)
if predict_btn:
    
    
    input_data = input_data[model.feature_names_in_]
    
    prediction = model.predict(input_data)
    predicted_days = round(prediction[0])
    
    st.success(f"📦 Estimated Delivery Time: {predicted_days} days")  

