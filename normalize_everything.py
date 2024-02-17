

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from library import normalize_matrix, yellow
import time

def do_the_thing(input_file_name, output_file_name):
    df = pd.read_csv(input_file_name)
    print(df.describe())
    df.to_csv(output_file_name, index=False)
    print(f" normalize_everything.py wrote to: '{output_file_name}'.")

if __name__ == "__main__":

    """
    1: divide each person's data by their number of sessions, 
    which is stored in the first column. 
    2: normalize the columns. 
    3: Additionally, prepend the unmodified number of sessions and the unmodified total lifetime value (tlv)
    to each row in the output CSV.
    4: See tdd.py for data shape assumptions
    """

    input_file_name = 'rollup_pii_free.csv'
    # input_file_name = 'tdd_data.csv'
    output_file_name = 'vectorized_rollup.csv'
    t1 = time.time()
    do_the_thing(input_file_name, output_file_name)
    duration = time.time() - t1
    msg = f"execution={duration} seconds; input={input_file_name}; output={output_file_name}"
    yellow(msg)
