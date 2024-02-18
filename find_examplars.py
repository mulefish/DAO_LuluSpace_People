

import pandas as pd
from library import yellow, CommonThings, find_most_common_vectors
import time

def do_the_thing(input_file_name, output_file_name, mode, low, high, loop):

    df = pd.read_csv(input_file_name)
    filtered_df = df[(df['ORIGINAL_TLV'] >= low) & (df['ORIGINAL_TLV'] <= high)]
    n = len(filtered_df)    
    most_common_df = find_most_common_vectors(filtered_df, loop, n, CommonThings.PRECISION, low, high, loop)
    most_common_df.to_csv(output_file_name, mode=mode, index=False, header=mode=='w')



    print(f" normalize_everything.py wrote to: '{output_file_name}'.")

if __name__ == "__main__":
    input_file_name = CommonThings.ROLLUP_VECTORIZED
    output_file_name = CommonThings.CLUSTERS
    bands = [(1, 1000), (1001, 5000), (5001, 10000), (10001, 20000), (20001, 30000), (30001, 999999)]
    loop = 0 
    for band in bands:
        low, high = band
        mode = 'w' if loop == 0 else 'a'
        loop += 1
        do_the_thing(input_file_name, output_file_name, mode, low, high, loop)
        yellow(f"loop={loop} of {len(bands)}")
