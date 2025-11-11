# 📊 Customer Churn Analysis (Telco Dataset)

## 📌 Objective
The goal of this project is to analyze customer churn behavior for a telecom company.  
Churn is a critical business metric — retaining customers is often cheaper than acquiring new ones.  
This analysis identifies **key factors driving churn** and highlights **at-risk customer segments**.

---

## 🗂️ Dataset
- **Source**: [Telco Customer Churn Dataset (Kaggle)](https://www.kaggle.com/blastchar/telco-customer-churn)  
- **Rows**: 7043  
- **Columns**: 21  
- **Key Fields**:  
  - `customerID` – unique customer identifier  
  - `tenure` – number of months customer stayed  
  - `MonthlyCharges` – customer’s monthly bill  
  - `TotalCharges` – total revenue from customer  
  - `Contract` – month-to-month, one-year, two-year  
  - `PaymentMethod` – billing type  
  - `Churn` – whether the customer left (Yes/No)  

---

## ⚙️ Tools Used
- **PostgreSQL** (hosted in DBeaver)  
- SQL for data analysis and business insights  
- DBeaver export for result visualization  

---

## 📈 Key Analysis

### 1. Overall Churn Rate
- Overall churn rate is ~**26.5%**.

### 2. Churn by Contract Type
- **Month-to-month contracts** → churn ~43% (highest).  
- **Two-year contracts** → churn ~3% (lowest).  

### 3. Churn by Payment Method
- Customers paying via **Electronic Check** churn the most (~45%).  

### 4. Churn by Internet Service
- Customers using **Fiber optic** churn more compared to DSL.  

### 5. Customer Segments at Risk
- Customers with **Month-to-Month + Fiber Optic + Electronic Check** have the **highest churn risk**.

---

## 📝 Conclusion
- Overall churn rate is ~**26.5%**.  
- **Contract type** is the strongest churn predictor — long-term contracts drastically reduce churn.  
- Customers on **Electronic Check** are the riskiest payment group.  
- **High monthly charges** also correlate with churn.  
- A **retention strategy** could include:  
  - Offering discounts for month-to-month users.  
  - Incentivizing automatic payments over electronic checks.  
  - Targeting fiber-optic customers with loyalty perks.

---

## 📂 Files
- `queries.sql` – All SQL scripts.  
- `results/` – CSV exports of query results.  
- `README.md` – This report.  

---

## 📬 Connect
- [LinkedIn](https://linkedin.com/in/YOUR-LINKEDIN)  
- [GitHub](https://github.com/YOUR-GITHUB)  
