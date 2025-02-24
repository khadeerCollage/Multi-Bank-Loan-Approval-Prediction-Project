import streamlit as st
# import numpy as np 
import pandas as pd 
import joblib
# import lightgbm as lgb 

st.title('Multi-Bank Loan Approval Prediction App')

# Sidebar with loan approval rules
st.sidebar.title("Loan Approval Rules")

st.sidebar.subheader("1. Applicant Information")
st.sidebar.markdown("""
- **person_age (Numerical)** → The applicant’s age.
  - 🟢 Ideal Range: 21 - 65 years (Most banks have this limit).
  - 🔴 Risk Factor: Younger than 21 or older than 65 may lead to rejection.
- **person_income (Numerical)** → Applicant’s annual income.
  - 🟢 Higher income increases loan approval chances.
  - 🔴 Zero or very low income means high default risk.
- **person_home_ownership (Categorical, Encoded)** → Type of home ownership.
  - 1 = RENT, 2 = MORTGAGE, 3 = OWN, 4 = OTHER
  - 🟢 OWN/MORTGAGE shows financial stability.
  - 🔴 RENT/OTHER may indicate financial instability.
- **person_emp_length (Numerical)** → Years of employment.
  - 🟢 More than 2 years suggests stable employment.
  - 🔴 Less than 1 year may be a risk factor.
""")

st.sidebar.subheader("2. Loan Information")
st.sidebar.markdown("""
- **loan_intent (Categorical, Encoded)** → Purpose of the loan.
  - 1 = EDUCATION, 2 = MEDICAL, 3 = VENTURE, 4 = PERSONAL, 5 = DEBTCONSOLIDATION, 6 = HOMEIMPROVEMENT
  - 🟢 Education, Home Improvement, Medical → Lower risk.
  - 🔴 Venture & Personal loans → High-risk spending.
- **loan_grade (Categorical, Encoded)** → Loan risk grade (A-G).
  - 1 = A (Best Credit Quality) to 7 = G (High Risk)
  - 🟢 A, B, C are considered safer.
  - 🔴 F, G grades may get rejected.
- **loan_amnt (Numerical)** → Total loan amount requested.
  - 🟢 Should be reasonable compared to income (Loan-to-Income Ratio).
  - 🔴 If loan > 5x annual income, rejection is likely.
- **loan_status (Categorical)** → Current status of the loan (e.g., Fully Paid, Defaulted).
  - 🟢 Fully Paid history boosts approval chances.
  - 🔴 Defaults, Late Payments may lead to rejection.
- **loan_int_rate (Numerical)** → Interest rate on the loan.
  - 🟢 Lower rates (below 15%) indicate a lower-risk borrower.
  - 🔴 Above 20% suggests high credit risk.
- **loan_percent_income (Numerical)** → Percentage of monthly income spent on loan repayment.
  - 🟢 Should be below 50% for affordability.
  - 🔴 If more than 50%, risk of default is high.
""")

st.sidebar.subheader("3. Credit History & Risk Factors")
st.sidebar.markdown("""
- **cb_person_default_on_file (Categorical, Encoded)** → Has the applicant ever defaulted?
  - 0 = No, 1 = Yes
  - 🔴 "Yes" (1) is a strong rejection factor.
- **cb_person_cred_hist_length (Numerical)** → Length of credit history in years.
  - 🟢 Above 5 years is ideal.
  - 🔴 Below 2 years indicates a thin credit file.
- **credit_score (Numerical)** → Creditworthiness score (e.g., 300-850).
  - 🟢 Above 700 → Safe applicant.
  - 🔴 Below 600 → High rejection risk.
""")

st.sidebar.subheader("4. Other Risk Factors")
st.sidebar.markdown("""
- **existing_loans (Numerical)** → Number of ongoing loans.
  - 🟢 Less than 3 loans is preferred.
  - 🔴 More than 3 loans signals over-borrowing.
- **debt_to_income_ratio (Numerical)** → Percentage of income already used for debts.
  - 🟢 Below 40% is manageable.
  - 🔴 Above 40% → High rejection probability.
- **loan_term (Categorical, Encoded)** → Loan duration.
  - 36 months (3 years) or 60 months (5 years)
  - 🔴 Longer terms (60 months) with high-risk applicants = 🚫 rejection.
""")

st.sidebar.subheader("Final Notes")
st.sidebar.markdown("""
📌 A strong loan application typically includes:
- ✅ Age between 21-65
- ✅ Stable employment (2+ years)
- ✅ Income high enough for the requested loan
- ✅ Credit score above 700
- ✅ Low debt-to-income ratio (<40%)
- ✅ No previous defaults
""")

# List of Indian banks
# Combined list of all banks in India
banks = [
    "Reserve Bank of India",  # Central Bank

    # Public Sector Banks
    "State Bank of India", "Bank of Baroda", "Punjab National Bank", "Bank of India",
    "Union Bank of India", "Canara Bank", "Bank of Maharashtra", "Central Bank of India",
    "Indian Overseas Bank", "Indian Bank", "UCO Bank", "Punjab and Sind Bank",

    # Private Sector Banks
    "HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Mahindra Bank", "IndusInd Bank",
    "Yes Bank", "IDFC First Bank", "Federal Bank", "South Indian Bank", "RBL Bank",
    "Bandhan Bank", "IDBI Bank", "Jammu & Kashmir Bank", "Karnataka Bank",
    "Dhanlaxmi Bank", "City Union Bank", "Karur Vysya Bank", "Nainital Bank",
    "Tamilnad Mercantile Bank",

    # Regional Rural Banks (RRBs)
    "Andhra Pragathi Grameena Bank", "Chaitanya Godavari Gramin Bank", "Saptagiri Gramin Bank",
    "Arunachal Pradesh Rural Bank", "Assam Gramin Vikash Bank", "Dakshin Bihar Gramin Bank",
    "Uttar Bihar Gramin Bank", "Chhattisgarh Rajya Gramin Bank", "Baroda Gujarat Gramin Bank",
    "Saurashtra Gramin Bank", "Sarva Haryana Gramin Bank", "Himachal Pradesh Gramin Bank",
    "J&K Grameen Bank", "Ellaquai Dehati Bank", "Jharkhand Rajya Gramin Bank", "Karnataka Gramin Bank",
    "Karnataka Vikas Grameena Bank", "Kerala Gramin Bank", "Madhyanchal Gramin Bank",
    "Madhya Pradesh Gramin Bank", "Maharashtra Gramin Bank", "Vidharbha Konkan Gramin Bank",
    "Manipur Rural Bank", "Meghalaya Rural Bank", "Mizoram Rural Bank", "Nagaland Rural Bank",
    "Odisha Gramya Bank", "Utkal Grameen Bank", "Puduvai Bharathiar Grama Bank", "Punjab Gramin Bank",
    "Baroda Rajasthan Kshetriya Gramin Bank", "Rajasthan Marudhara Gramin Bank", "Tamil Nadu Grama Bank",
    "Telangana Grameena Bank", "Andhra Pradesh Grameena Vikas Bank", "Tripura Gramin Bank",
    "Aryavart Bank", "Prathama UP Gramin Bank", "Baroda UP Bank", "Uttarakhand Gramin Bank",
    "Paschim Banga Gramin Bank", "Bangiya Gramin Vikash Bank", "Uttarbanga Kshetriya Gramin Bank"
]


# Selection box for banks
selected_bank = st.selectbox("Select a Bank", banks)

# Display the selected bank
st.write(f"You selected: {selected_bank}")

# List of loan intents
loan_intents = [
    "EDUCATION", "MEDICAL", "VENTURE", "PERSONAL", 
    "DEBTCONSOLIDATION", "HOMEIMPROVEMENT"
]

# Selection box for loan intent
selected_loan_intent = st.selectbox("Select Loan Intent", loan_intents)

# Display the selected loan intent
st.write(f"You selected: {selected_loan_intent}")

# Display a message when both bank and loan intent are selected
if selected_bank and selected_loan_intent:
    st.markdown("### Our Basic Loan Approval Form")
    st.write("Please fill out the form below to predict your loan approval status based on the selected bank and loan intent.")

# Loan features
selected_features = [
    'person_age', 'person_income', 'person_home_ownership', 'person_emp_length',
    'loan_intent', 'loan_grade', 'loan_amnt','loan_status', 'loan_int_rate', 'loan_percent_income',
    'cb_person_default_on_file', 'cb_person_cred_hist_length', 'loan_term',
    'credit_score', 'existing_loans', 'debt_to_income_ratio'
]

# Form to input loan details
with st.form(key='loan_form'):
    person_age = st.number_input('Person Age ', min_value=18, max_value=100)
    person_income = st.number_input('Person Income (Higher income improves loan repayment ability.)', min_value=0)
    person_home_ownership = st.selectbox('Person Home Ownership', ['RENT', 'OWN', 'MORTGAGE', 'OTHER'])
    person_emp_length = st.number_input('Person Employment Length (years)', min_value=0)
    loan_grade = st.selectbox('Loan Grade (Assigned by the lender based on creditworthiness)', ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    loan_amnt = st.number_input('Loan Amount (Loan amount requested by the applicant)', min_value=0)
    loan_status = st.selectbox('Loan Status', ['Fully Paid', 'Charged Off', 'Current'])
    loan_int_rate = st.number_input('Loan Interest Rate (Higher interest rates indicate riskier loans.)', min_value=0.0, max_value=100.0)
    loan_percent_income = st.number_input('Loan Percent Income (Measures if the loan amount is affordable compared to income)', min_value=0.0, max_value=100.0)
    cb_person_default_on_file = st.selectbox('Credit Bureau Person Default on File (If the person has defaulted before, they are high-risk)', ['Y', 'N'])
    cb_person_cred_hist_length = st.number_input('Credit History Length [Years](A longer credit history means more data for assessment)', min_value=0)
    loan_term = st.selectbox('Loan Term', ['36 months', '60 months'])
    credit_score = st.number_input('Credit Score (A key factor in deciding loan approval)', min_value=300, max_value=850)
    existing_loans = st.number_input('Existing Loans (More existing loans increase financial burden.)', min_value=0)
    debt_to_income_ratio = st.number_input('Debt to Income Ratio (Higher ratios mean the applicant has more debt compared to income)', min_value=0.0, max_value=100.0)
    
    submit_button = st.form_submit_button(label='Submit')

# Load the trained model
model = joblib.load("lgbm_loan_model.pkl")

if submit_button:
    st.write("Form Submitted")
    
    # Prepare the input data for prediction
    input_data = pd.DataFrame({
        'person_age': [person_age],
        'person_income': [person_income],
        'person_home_ownership': [person_home_ownership],
        'person_emp_length': [person_emp_length],
        'loan_intent': [selected_loan_intent],
        'loan_grade': [loan_grade],
        'loan_amnt': [loan_amnt],
        'loan_int_rate': [loan_int_rate],
        'loan_percent_income': [loan_percent_income],
        'cb_person_default_on_file': [cb_person_default_on_file],
        'cb_person_cred_hist_length': [cb_person_cred_hist_length],
        'loan_term': [loan_term],
        'credit_score': [credit_score],
        'existing_loans': [existing_loans],
        'debt_to_income_ratio': [debt_to_income_ratio]
    })

    # Encode categorical features
    input_data['person_home_ownership'].replace({'RENT': 1, 'MORTGAGE': 2, 'OWN': 3, 'OTHER': 4}, inplace=True)
    input_data['loan_intent'].replace({'EDUCATION': 1, 'MEDICAL': 2, 'VENTURE': 3, 'PERSONAL': 4, 'DEBTCONSOLIDATION': 5, 'HOMEIMPROVEMENT': 6}, inplace=True)
    input_data['loan_grade'].replace({'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}, inplace=True)
    input_data['cb_person_default_on_file'].replace({'N': 0, 'Y': 1}, inplace=True)
    input_data['loan_term'].replace({'36 months': 36, '60 months': 60}, inplace=True)

    # Log the input data
    st.write("Input Data:")
    st.write(input_data)

    # Make prediction
    prediction = model.predict(input_data)
    st.write(f"Raw Prediction Value: {prediction[0]}")

    # Set conditions for loan approval
    if input_data['person_income'][0] == 0:
        st.error("Loan Rejected: Applicant has no income.")
    elif input_data['credit_score'][0] < 600:
        st.error("Loan Rejected: Low credit score.")
    elif input_data['debt_to_income_ratio'][0] > 40:
        st.error("Loan Rejected: High debt-to-income ratio.")
    elif input_data['person_emp_length'][0] < 1:
        st.error("Loan Rejected: Applicant has less than 1 year of employment.")
    elif input_data['loan_amnt'][0] > (input_data['person_income'][0] * 5):  
        st.error("Loan Rejected: Loan amount is too high compared to income.")
    elif input_data['person_age'][0] < 21 or input_data['person_age'][0] > 65:
        st.error("Loan Rejected: Applicant does not meet the age requirement.")
    elif input_data['cb_person_default_on_file'][0] == 1:
        st.error("Loan Rejected: Applicant has previously defaulted on a loan.")
    elif input_data['cb_person_cred_hist_length'][0] < 2:
        st.error("Loan Rejected: Credit history is too short (less than 2 years).")
    elif input_data['existing_loans'][0] > 3:
        st.error("Loan Rejected: Too many existing loans.")
    elif input_data['loan_int_rate'][0] > 20:
        st.error("Loan Rejected: High interest rate makes repayment risky.")
    elif input_data['loan_percent_income'][0] > 50:
        st.error("Loan Rejected: Loan amount exceeds 50% of monthly income.")
    elif input_data['person_home_ownership'][0] == 4:  # 'OTHER'
        st.error("Loan Rejected: Home ownership status is unclear or other.")
    elif input_data['loan_grade'][0] > 5:  # Grade F or G
        st.error("Loan Rejected: Loan grade is too low (high risk).")
    elif input_data['loan_term'][0] == 60 and input_data['loan_grade'][0] > 4:  # Long-term, high-risk loan
        st.error("Loan Rejected: High-risk loan grade with a long loan term (60 months).")
    else:
        # Apply threshold to determine class
        prediction_class = 'Approved' if prediction[0] >= 0.5 else 'Rejected'

        # Display the prediction
        if prediction_class == 'Approved':
            st.success(f"Loan Prediction: {prediction_class}")
        else:
            st.error(f"Loan Prediction: {prediction_class}")



