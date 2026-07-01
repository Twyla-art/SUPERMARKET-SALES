import streamlit as st
import joblib
import pandas as pd

# ----------------------------
# Load the trained model
# ----------------------------
model = joblib.load('rating_prediction_model.pkl')

# ----------------------------
# Page Title
# ----------------------------
st.title('🛒 Customer Satisfaction Rating Predictor')
st.write('Enter transaction details below to predict the customer satisfaction rating.')

# ----------------------------
# Input Fields
# ----------------------------
branch = st.selectbox('Branch', options=[0, 1, 2],
                       format_func=lambda x: ['A', 'B', 'C'][x])

customer_type = st.selectbox('Customer Type', options=[0, 1],
                              format_func=lambda x: ['Member', 'Normal'][x])

gender = st.selectbox('Gender', options=[0, 1],
                       format_func=lambda x: ['Female', 'Male'][x])

product_line = st.selectbox('Product Line', options=[0, 1, 2, 3, 4, 5],
                             format_func=lambda x: [
                                 'Electronic accessories',
                                 'Fashion accessories',
                                 'Food and beverages',
                                 'Health and beauty',
                                 'Home and lifestyle',
                                 'Sports and travel'][x])

unit_price = st.number_input('Unit Price ($)', min_value=0.0, value=50.0, step=0.5)
quantity = st.number_input('Quantity', min_value=1, value=1, step=1)

# Total is calculated automatically (Unit price x Quantity x 1.05 tax)
total = round(unit_price * quantity * 1.05, 2)
st.write(f'Calculated Total (incl. 5% tax): **${total}**')

payment = st.selectbox('Payment Method', options=[0, 1, 2],
                        format_func=lambda x: ['Cash', 'Credit card', 'Ewallet'][x])

month = st.selectbox('Month', options=[1, 2, 3],
                      format_func=lambda x: ['January', 'February', 'March'][x - 1])

day = st.number_input('Day of Month', min_value=1, max_value=31, value=15, step=1)

hour = st.slider('Hour of Purchase (24h format)', min_value=10, max_value=21, value=14)

revenue_per_unit = round(total / quantity, 2)
st.write(f'Calculated Revenue per Unit: **${revenue_per_unit}**')

# ----------------------------
# Prediction
# ----------------------------
if st.button('Predict Rating'):
    input_data = pd.DataFrame(
        [[branch, customer_type, gender, product_line, unit_price,
          quantity, total, payment, month, day, hour, revenue_per_unit]],
        columns=['Branch', 'Customer type', 'Gender', 'Product line',
                 'Unit price', 'Quantity', 'Total', 'Payment',
                 'Month', 'Day', 'Hour', 'Revenue_per_unit']
    )

    prediction = model.predict(input_data)[0]
    prediction = round(prediction, 2)

    st.subheader("Prediction Result")

    if prediction < 6:
        st.error(f"⭐ Predicted Customer Rating: {prediction} / 10")
        st.error("Satisfaction Category: Needs Improvement")
    elif prediction < 8:
        st.warning(f"⭐ Predicted Customer Rating: {prediction} / 10")
        st.warning("Satisfaction Category: Good")
    else:
        st.success(f"⭐ Predicted Customer Rating: {prediction} / 10")
        st.success("Satisfaction Category: Excellent")

# ----------------------------
# Footer
# ----------------------------
st.markdown('---')
st.caption('Supermarket Sales Analysis Project — Linear Regression Model')