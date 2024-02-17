import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import warnings

class CommonThings:
    CSV_TDD = "data/tdd_data.csv"
    ROLLUP_PII_FREE='data/rollup_pii_free.csv'
    ROLLUP_VECTORIZED='data/vectorized_rollup.csv'


class Colors:
    BG_RED = "\x1b[41m"
    BG_CYAN = "\x1b[46m"
    BG_YELLOW = "\x1b[43m"
    BG_GREEN = "\x1b[92m"
    BOLD = "\x1b[1m"
    RESET = "\x1b[0m"

def red(msg):
    print(f"{Colors.BG_RED}{msg}{Colors.RESET}")

def yellow(msg):
    print(f"{Colors.BG_YELLOW}{msg}{Colors.RESET}")

def green(msg):
    print(f"{Colors.BG_GREEN}{msg}{Colors.RESET}")

def normalize_matrix(df):
    """
    1: divide each person's data by their number of sessions, 
    which is stored in the first column. 
    2: normalize the columns. 
    3: Additionally, prepend the unmodified number of sessions and the unmodified total lifetime value (tlv)
    to each row in the output CSV.
    4: The data shape assumption is something like this: 
    sessions,tlv,a,b,c
    10, 1000, 1000, 100, 10
    100, 100, 2000, 200, 20
    10, 100, 500, 50, 5
    """

    # Save the 'sessions' and 'tlv' columns before any operations
    sessions_column_index = 0
    sessions_col = df.iloc[:, sessions_column_index]
    tlv_col = df['tlv']
    scaler = MinMaxScaler()

    # Exclude 'sessions' and 'tlv' from the normalization and division process
    data_columns = df.columns[1:]  # Assuming sessions is the first column and is followed by other features

    for column in data_columns:
        if column != 'tlv':  # Assuming 'tlv' should not be normalized/divided by sessions
            # Divide the data by the number of sessions, element-wise
            df[column] = df[column] / sessions_col

    # Normalize the columns (excluding 'sessions' and 'tlv' from normalization)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # Suppress all warnings
        df[data_columns] = scaler.fit_transform(df[data_columns])

    # Prepend 'sessions' and 'tlv' to the DataFrame
    df.insert(0, 'sessions_unmodified', sessions_col)
    df.insert(1, 'tlv_unmodified', tlv_col)

    return df
