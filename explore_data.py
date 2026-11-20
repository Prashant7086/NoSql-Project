import pandas as pd

# Dataset path
file_path = r"C:\Users\prash\Downloads\NoSql Project\DataSet\News_Category_Dataset_v3.json"

# Load JSON dataset
df = pd.read_json(file_path, lines=True)
# Display dataset information
print("\n========== DATASET INFORMATION ==========")
print("\nDataset Shape:")
print(df.shape)
print("\nColumn Names:")
print(df.columns.tolist())
print("\nData Types:")
print(df.dtypes)
print("\nFirst 5 Records:")
print(df.head())
print("\nMissing Values:")
print(df.isnull().sum())
print("\nDuplicate Rows:")
print(df.duplicated().sum())
print("\nDescriptive Statistics:")
print(df.describe(include="all"))