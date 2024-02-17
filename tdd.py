import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from io import StringIO

input_file_name = 'tdd_data.csv'

expected_output = """a,b,c
0.3333333333333333,0.33333333333333337,0.3333333333333333
1.0,1.0,1.0
0.0,0.0,0.0
"""
df = pd.read_csv(input_file_name)

output_file_name = 'vectorized_rollup.csv'

df = pd.read_csv(input_file_name)
sessions_col = df.iloc[:, 0] # first column is 'sessions'
tlv_col = df['tlv']  # Replace 'tlv' with the actual column name for total lifetime value
scaler = MinMaxScaler()
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

print( df )

# normalized_data_str = output.getvalue().strip()
# normalized_data_str = normalized_data_str.replace('\r\n', '\n')


# df.to_csv(output_file_name, index=False)

# print(f"The processed data has been written to '{output_file_name}'.")
