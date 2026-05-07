import pandas as pd

# Preprocessing the dataset 1 spam

csv_path_1 = 'Dataset/spam.csv'

with open(csv_path_1, 'r', encoding='utf-8', errors='ignore') as f:
    print(pd.read_csv(f, nrows=0).shape[1])
    df1 = pd.read_csv(f, usecols=[0, 1], names=['label', 'text'], header=0)

df1['text'] = (df1['text'].str.replace(r'[^\w\s]', '', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip().str.lower())

df1 = df1[['text', 'label']].dropna()

print(df1.head())
print(df1.shape)


# Preprocessing the dataset 2 spam1

csv_path_2 = 'Dataset/spam1.csv'

with open(csv_path_2, 'r', encoding='utf-8', errors='ignore') as f:
    print(pd.read_csv(f, nrows=0).shape[1])
    df2 = pd.read_csv(f, usecols=[0, 1], names=['label', 'text'], header=0)

df2['text'] = (df2['text'].str.replace(r'[^\w\s]', '', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip().str.lower())
df2 = df2[['text', 'label']].dropna()

print(df2.head())
print(df2.shape)

# Preprocessing the dataset 3 emails

csv_path_3 = 'Dataset/emails.csv'

with open(csv_path_3, 'r', encoding='utf-8', errors='ignore') as f:
    print(pd.read_csv(f, nrows=0).shape[1])
    df3 = pd.read_csv(f, usecols=[0, 1], names=['text', 'label'], header=0)

df3['text'] = (df3['text'].str.replace(r'(?i)^\s*subject[:\s]+', '', regex=True).str.replace(r'[^\w\s]', '', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip().str.lower())
df3 = df3.dropna()
df3["label"] = df3["label"].apply(lambda x: 'ham' if x == 0 else 'spam')

print(df3.head())
print(df3.shape)

# Combine the datasets

combined_df = pd.concat([df1, df2, df3], ignore_index=True)

# Save the combined dataset to a new CSV file
combined_df.to_csv('Dataset/combined_spam_test.csv', index=False)
