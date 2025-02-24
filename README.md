# Multi-Bank Loan Approval Prediction App

This project is a Streamlit-based web application that predicts loan approval status based on various applicant and loan features. The app uses a pre-trained LightGBM model to make predictions.

## Project Structure

- `app.py`: The main application file containing the Streamlit app code.
- `lgbm_loan_model.pkl`: The pre-trained LightGBM model used for predictions.

## Application Features

### Sidebar

The sidebar contains detailed loan approval rules and guidelines for applicants. It is divided into several sections:

1. **Applicant Information**:
    - `person_age`: The applicant’s age.
    - `person_income`: Applicant’s annual income.
    - `person_home_ownership`: Type of home ownership.
    - `person_emp_length`: Years of employment.

2. **Loan Information**:
    - `loan_intent`: Purpose of the loan.
    - `loan_grade`: Loan risk grade.
    - `loan_amnt`: Total loan amount requested.
    - `loan_status`: Current status of the loan.
    - `loan_int_rate`: Interest rate on the loan.
    - `loan_percent_income`: Percentage of monthly income spent on loan repayment.

3. **Credit History & Risk Factors**:
    - `cb_person_default_on_file`: Has the applicant ever defaulted?
    - `cb_person_cred_hist_length`: Length of credit history in years.
    - `credit_score`: Creditworthiness score.

4. **Other Risk Factors**:
    - `existing_loans`: Number of ongoing loans.
    - `debt_to_income_ratio`: Percentage of income already used for debts.
    - `loan_term`: Loan duration.

### Main Content

- **Bank Selection**: A dropdown to select a bank from a list of Indian banks.
- **Loan Intent Selection**: A dropdown to select the purpose of the loan.
- **Loan Approval Form**: A form to input various loan details such as age, income, home ownership, employment length, loan amount, interest rate, credit score, etc.

### Model Prediction

- The app loads a pre-trained LightGBM model (`lgbm_loan_model.pkl`) to make predictions.
- The input data is prepared and encoded before making predictions.
- The app displays the prediction result and provides detailed reasons for loan approval or rejection based on the input data.

## How to Run the App

1. Ensure you have Streamlit installed:
    ```bash
    pip install streamlit
    ```

2. Run the app:
    ```bash
    streamlit run app.py
    ```

3. Open the provided URL in your web browser to interact with the app.

## Detailed Explanation of `app.py`

- **Imports**: Import necessary libraries such as Streamlit, NumPy, Pandas, joblib, and LightGBM.
- **Title and Sidebar**: Set up the title and sidebar with loan approval rules.
- **Bank and Loan Intent Selection**: Provide dropdowns for selecting a bank and loan intent.
- **Loan Approval Form**: Create a form to input various loan details.
- **Model Loading and Prediction**: Load the pre-trained model and make predictions based on the input data.
- **Prediction Display**: Display the prediction result and provide detailed reasons for loan approval or rejection.

## Conclusion

This app provides a user-friendly interface for predicting loan approval status based on various applicant and loan features. It uses a pre-trained LightGBM model to make accurate predictions and provides detailed feedback on the loan application.
