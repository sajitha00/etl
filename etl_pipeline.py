
import pandas as pd
import numpy as np
import logging
from typing import Tuple, Dict, Any
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SocialAdsETL:

    # ETL Pipeline for Social Media Ads Data
    def __init__(self, file_path: str = 'data/social_ads.csv'):
       
        # Initialize the ETL pipeline
        self.file_path = file_path
        self.raw_data = None
        self.processed_data = None
        self.data_quality_report = {}
        
    def extract(self) -> pd.DataFrame:


        # Extract data from CSV file
        try:
            logger.info(f"Extracting data from {self.file_path}")
            
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"File {self.file_path} not found")
            
            # Read CSV with proper data types
            self.raw_data = pd.read_csv(
                self.file_path,
                dtype={
                    'Age': 'int64',
                    'EstimatedSalary': 'int64',
                    'Purchased': 'int64'
                }
            )
            
            logger.info(f"Successfully extracted {len(self.raw_data)} records")
            return self.raw_data
            
        except Exception as e:
            logger.error(f"Error during data extraction: {str(e)}")
            raise
    
    def validate_data(self) -> Dict[str, Any]:
        
        # Validate data quality and generate quality report
        
        if self.raw_data is None:
            raise ValueError("No data to validate. Run extract() first.")
        
        logger.info("Validating data quality")
        
        # Basic data info
        total_records = len(self.raw_data)
        
        # Check for missing values
        missing_values = self.raw_data.isnull().sum()
        
        # Check for duplicates
        duplicates = self.raw_data.duplicated().sum()
        
        # Data type validation
        expected_dtypes = {
            'Age': 'int64',
            'EstimatedSalary': 'int64',
            'Purchased': 'int64'
        }
        
        dtype_issues = []
        for col, expected_dtype in expected_dtypes.items():
            if str(self.raw_data[col].dtype) != expected_dtype:
                dtype_issues.append(f"{col}: expected {expected_dtype}, got {self.raw_data[col].dtype}")
        
        # Value range validation
        age_issues = []
        if self.raw_data['Age'].min() < 0 or self.raw_data['Age'].max() > 120:
            age_issues.append("Age values outside reasonable range (0-120)")
        
        salary_issues = []
        if self.raw_data['EstimatedSalary'].min() < 0:
            salary_issues.append("Negative salary values found")
        
        purchase_issues = []
        unique_purchase_values = set(self.raw_data['Purchased'].unique())
        if not unique_purchase_values.issubset({0, 1}):
            purchase_issues.append("Purchased column contains values other than 0 and 1")
        
        # Compile quality report
        self.data_quality_report = {
            'total_records': total_records,
            'missing_values': missing_values.to_dict(),
            'duplicate_records': duplicates,
            'dtype_issues': dtype_issues,
            'age_issues': age_issues,
            'salary_issues': salary_issues,
            'purchase_issues': purchase_issues,
            'data_shape': self.raw_data.shape,
            'memory_usage': self.raw_data.memory_usage(deep=True).sum()
        }
        
        # Log quality issues
        if duplicates > 0:
            logger.warning(f"Found {duplicates} duplicate records")
        if any(missing_values > 0):
            logger.warning(f"Missing values found: {missing_values[missing_values > 0].to_dict()}")
        if dtype_issues:
            logger.warning(f"Data type issues: {dtype_issues}")
        
        logger.info("Data validation completed")
        return self.data_quality_report
    
    def transform(self) -> pd.DataFrame:
        if self.raw_data is None:
            raise ValueError("No data to transform. Run extract() first.")
        
        logger.info("Starting data transformation")
        
        # Create a copy for transformation
        self.processed_data = self.raw_data.copy()
        
        # Remove duplicates if any
        initial_count = len(self.processed_data)
        self.processed_data = self.processed_data.drop_duplicates()
        removed_duplicates = initial_count - len(self.processed_data)
        
        if removed_duplicates > 0:
            logger.info(f"Removed {removed_duplicates} duplicate records")
        
        # Create age groups for analysis
        self.processed_data['AgeGroup'] = pd.cut(
            self.processed_data['Age'],
            bins=[0, 25, 35, 45, 55, 100],
            labels=['18-25', '26-35', '36-45', '46-55', '55+'],
            include_lowest=True
        )
        
        # Create salary groups
        self.processed_data['SalaryGroup'] = pd.cut(
            self.processed_data['EstimatedSalary'],
            bins=[0, 30000, 60000, 90000, 120000, float('inf')],
            labels=['Low (≤30K)', 'Medium-Low (30K-60K)', 'Medium (60K-90K)', 
                   'Medium-High (90K-120K)', 'High (>120K)'],
            include_lowest=True
        )
        
        # Create binary labels for better readability
        self.processed_data['PurchaseStatus'] = self.processed_data['Purchased'].map({
            0: 'Not Purchased',
            1: 'Purchased'
        })
        
        # Calculate additional metrics
        self.processed_data['SalaryPerAge'] = (
            self.processed_data['EstimatedSalary'] / self.processed_data['Age']
        ).round(2)
        
        logger.info(f"Data transformation completed. Final dataset shape: {self.processed_data.shape}")
        return self.processed_data
    
    def load(self, output_path: str = 'data/processed_social_ads.csv') -> None:
       
        if self.processed_data is None:
            raise ValueError("No processed data to load. Run transform() first.")
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save processed data
            self.processed_data.to_csv(output_path, index=False)
            logger.info(f"Processed data saved to {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving processed data: {str(e)}")
            raise
    
    def run_pipeline(self, save_processed: bool = True) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        
        # Run the complete ETL pipeline
        logger.info("Starting ETL pipeline")
        
        try:
            # Extract
            self.extract()
            
            # Validate
            quality_report = self.validate_data()
            
            # Transform
            self.transform()
            
            # Load (optional)
            if save_processed:
                self.load()
            
            logger.info("ETL pipeline completed successfully")
            return self.processed_data, quality_report
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {str(e)}")
            raise
    
    def get_data_summary(self) -> Dict[str, Any]:
       
        # Get a summary of the processed data
        if self.processed_data is None:
            raise ValueError("No processed data available. Run the pipeline first.")
        
        summary = {
            'total_records': len(self.processed_data),
            'purchase_rate': (self.processed_data['Purchased'].sum() / len(self.processed_data) * 100).round(2),
            'age_stats': {
                'mean': self.processed_data['Age'].mean().round(2),
                'median': self.processed_data['Age'].median(),
                'min': self.processed_data['Age'].min(),
                'max': self.processed_data['Age'].max(),
                'std': self.processed_data['Age'].std().round(2)
            },
            'salary_stats': {
                'mean': self.processed_data['EstimatedSalary'].mean().round(2),
                'median': self.processed_data['EstimatedSalary'].median(),
                'min': self.processed_data['EstimatedSalary'].min(),
                'max': self.processed_data['EstimatedSalary'].max(),
                'std': self.processed_data['EstimatedSalary'].std().round(2)
            },
            'age_group_distribution': self.processed_data['AgeGroup'].value_counts().to_dict(),
            'salary_group_distribution': self.processed_data['SalaryGroup'].value_counts().to_dict(),
            'purchase_by_age_group': self.processed_data.groupby('AgeGroup')['Purchased'].mean().round(3).to_dict(),
            'purchase_by_salary_group': self.processed_data.groupby('SalaryGroup')['Purchased'].mean().round(3).to_dict()
        }
        
        return summary


def main():
    # Main function to demonstrate ETL pipeline usage
    
    # Initialize ETL pipeline
    etl = SocialAdsETL()
    
    try:
        # Run the complete pipeline
        processed_data, quality_report = etl.run_pipeline()
        
        # Print summary
        print("\n" + "="*50)
        print("ETL PIPELINE EXECUTION SUMMARY")
        print("="*50)
        
        print(f"\nData Quality Report:")
        print(f"- Total Records: {quality_report['total_records']}")
        print(f"- Duplicate Records: {quality_report['duplicate_records']}")
        print(f"- Missing Values: {sum(quality_report['missing_values'].values())}")
        print(f"- Data Shape: {quality_report['data_shape']}")
        
        # Get and print data summary
        summary = etl.get_data_summary()
        print(f"\nData Summary:")
        print(f"- Overall Purchase Rate: {summary['purchase_rate']}%")
        print(f"- Average Age: {summary['age_stats']['mean']} years")
        print(f"- Average Salary: ${summary['salary_stats']['mean']:,.2f}")
        
        print(f"\nPurchase Rate by Age Group:")
        for age_group, rate in summary['purchase_by_age_group'].items():
            print(f"- {age_group}: {rate*100:.1f}%")
        
        print(f"\nPurchase Rate by Salary Group:")
        for salary_group, rate in summary['purchase_by_salary_group'].items():
            print(f"- {salary_group}: {rate*100:.1f}%")
        
        print("\n" + "="*50)
        print("ETL PIPELINE COMPLETED SUCCESSFULLY")
        print("="*50)
        
    except Exception as e:
        print(f"Pipeline failed: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())