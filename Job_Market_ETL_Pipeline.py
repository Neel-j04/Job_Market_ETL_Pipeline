import pandas as pd

# Extract
df = pd.read_csv("D:\Datasets\job_descriptions.csv")
print(df.head(5))

# Transform
print("Sum of Null values:", df.isnull().sum())
print("\nShape of Dataset:", df.shape)
print("\nData types:", df.dtypes)
print("\nSum of Duploicates:", df.duplicated().sum())
print("\nDrop duplicates:", df.drop_duplicates(inplace=True))

missing_percentage = (
    df["Company Profile"].isnull().sum() / len(df) * 100
)
print("\n Missing percentage:", missing_percentage)

df["Company Profile"] = df["Company Profile"].fillna("Not Available")

# Min, Max & Avg salary
print(df["Salary Range"].head(20).tolist())

df["salary_min"] = (
    pd.to_numeric(
        df["Salary Range"].str.extract(r"(\d+)")[0],
        errors="coerce"
    )
    * 1000
)

df["salary_max"] = (
    pd.to_numeric(
        df["Salary Range"].str.extract(r".*?(\d+)K$")[0],
        errors="coerce"
    )
    * 1000
)

df["salary_avg"] = (
    df["salary_min"] + df["salary_max"]
) / 2

print(df[[
    "Salary Range", "salary_min", "salary_max", "salary_avg"]].head(20))

print("\nNull values in salary_min:")
print(df["salary_min"].isnull().sum())

print("\nNull values in salary_max:")
print(df["salary_max"].isnull().sum())

# Date conversion
df["Job Posting Date"]
df["Job Posting Date"] = pd.to_datetime(df["Job Posting Date"], format="%d-%m-%Y")

# Country analysis
print("\nCountry value count:\n", df['Country'].value_counts())
print("\nTop 10 Countries:\n", df["Country"].value_counts().head(10))

# Work type analysis
print("\nWork Type:\n", df["Work Type"].value_counts())

# Skills analysis
print("\nSkills:\n", df['skills'].head())

skill_list = ["Python", "SQL", "AWS", "Spark", "Power BI", "Tableau", "Java","JavaScript", "HTML", "CSS", "React", "Angular", "Machine Learning", "Deep Learning", "Docker", "Kubernetes", "MySQL", "MongoDB", "Git"]

skill_count = {}

for skill in skill_list:
    count = df["skills"].str.contains(skill, case=False, na=False).sum()
    skill_count[skill] = count

skill_df = (
    pd.DataFrame(
        skill_count.items(), columns=["Skill", "Count"]
    )
    .sort_values(
        by="Count",
        ascending=False
    )
)

print(skill_df.head(20))

# Final Dataset
print("\nFinal Dataset Shape:", df.shape)
print("\nRemaining Null Values:", df.isnull().sum())

# Load
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:Neel2004@localhost:5432/job_market_db"
)

df.to_sql(
    "jobs",
    engine,
    if_exists="replace",
    index=False
)

print("\nData Loaded Successfully!")