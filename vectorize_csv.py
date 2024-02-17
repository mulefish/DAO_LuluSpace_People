
"""
1: divide each person's data by their number of sessions, 
which is stored in the first column. 
2: normalize the columns. 
3: Additionally, you will prepend the unmodified number of sessions and the unmodified total lifetime value (tlv)
 to each row in the output CSV.
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

input_file_name = 'rollup_pii_free.csv'
# input_file_name = 'tdd_data.csv'

output_file_name = 'vectorized_rollup.csv'

df = pd.read_csv(input_file_name)

# Save the 'sessions' and 'tlv' columns before any operations
sessions_col = df.iloc[:, 0]  # Assuming the first column is 'sessions'
tlv_col = df['tlv']  # Replace 'tlv' with the actual column name for total lifetime value

scaler = MinMaxScaler()

# Exclude 'sessions' and 'tlv' from the normalization and division process
data_columns = df.columns[1:]  # Assuming sessions is the first column and is followed by other features

for column in data_columns:
    if column != 'tlv':  # Assuming 'tlv' should not be normalized/divided by sessions
        # Divide the data by the number of sessions, element-wise
        df[column] = df[column] / sessions_col

# Normalize the columns (excluding 'sessions' and 'tlv' from normalization)
df[data_columns] = scaler.fit_transform(df[data_columns])

# Prepend 'sessions' and 'tlv' to the DataFrame
df.insert(0, 'sessions_unmodified', sessions_col)
df.insert(1, 'tlv_unmodified', tlv_col)

df.to_csv(output_file_name, index=False)

print(f"The processed data has been written to '{output_file_name}'.")
