📊 Social Media Ads Purchase Analysis

🚀 Project Overview
This project analyzes social media advertising data to understand customer purchase behavior and identify valuable customer segments for optimized marketing strategies. Using data analysis and machine learning techniques, this analysis aims to drive actionable insights and improve advertising ROI.

🎯 Business Objective
Challenge: Identify which types of customers are most likely to purchase after seeing social media ads.

Goal: Generate data-driven recommendations to optimize ad targeting, increase conversion rates, and maximize marketing ROI.

🛠️ Setup Instructions

Prerequisites
-Python 3.8+
-Jupyter Notebook

# Clone the repository

git clone <[repository-url](https://github.com/sajitha00/etl)>
cd social-media-ads-analysis

# Install dependencies

pip install -r requirements.txt

# Run ETL pipeline

python etl_pipeline.py

# Launch Jupyter Notebook

jupyter notebook analysis.ipynb or install jupyter extension on vs code then can view through run cells buttons or you can export it as html file or pdf from top of the bar

📚 Dataset Description

Records: 400 customers

Features:
Age: Customer age
EstimatedSalary: Estimated annual salary
Purchased: Purchase status (0 = No, 1 = Yes)

📈 Key Insights
Overall Metrics
Total customers: 400

Overall purchase rate: 36.5%

Average customer age: 37.7 years

Average salary: $69,743

Age Group Performance
Age Group Purchase Rate
55+ 64.0%
46-55 50.0%
36-45 40.0%
26-35 23.2%
18-25 5.0%

Salary Group Performance
Salary Group Purchase Rate
High (>$120K) 58.3%
Medium-High ($90K-120K) 45.8%
Medium ($60K-90K) 35.0%
Medium-Low ($30K-60K) 25.7%
Low (≤$30K) 15.2%

Correlation Analysis
Age vs Purchase: 0.622 (Strong positive correlation)

Salary vs Purchase: 0.362 (Moderate positive correlation)

🤖 Machine Learning Results
Model Accuracy AUC Score
Random Forest 85.0% 0.912
Logistic Regression 83.8% 0.895

Feature Importance:

Age (Primary factor)

EstimatedSalary (Secondary factor)

💡 Strategic Recommendations

1️⃣ Focus ad targeting on 45+ age groups and high-income segments
2️⃣ Adjust budget allocation to prioritize high-conversion demographics
3️⃣ Develop segment-specific messaging and creative content
4️⃣ Implement machine learning-based predictive targeting for optimization

📊 Business Impact (Projected)

Increase purchase rate from 36.5% → ~47.5%
ROI increase ~30%
Cost per acquisition reduction ~40%
Improved targeting efficiency

🔍 Technical Highlights

End-to-end ETL pipeline with data validation and transformation
Statistical analysis and visual insights
Machine learning classification with multiple models
Clear, actionable business recommendations

📞 Contact
For questions or collaboration inquiries, please feel free to contact me.
email-sajithageevinda.sd@gmail.com
