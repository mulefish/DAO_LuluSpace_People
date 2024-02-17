

import pandas as pd
from library import yellow, CommonThings, find_most_common_vectors
import time

def do_the_thing(input_file_name, output_file_name, mode, low, high, loop):
    # df = pd.read_csv(input_file_name)
    # print(df.describe())
    # df = find_exemplar_vectors(df, CommonThings.PRECISION)
    # format_string = '%.{}f'.format(CommonThings.PRECISION) 
    # df.to_csv(output_file_name, float_format=format_string, index=False)

    # find_most_common_vectors(input_file_name, output_file_name)


    df = pd.read_csv(input_file_name)
    filtered_df = df[(df['ORIGINAL_TLV'] >= low) & (df['ORIGINAL_TLV'] <= high)]
    n = len(filtered_df)    
    most_common_df = find_most_common_vectors(filtered_df, loop, n, CommonThings.PRECISION)
    most_common_df.to_csv(output_file_name, mode=mode, index=False, header=mode=='w')



    print(f" normalize_everything.py wrote to: '{output_file_name}'.")

if __name__ == "__main__":



    input_file_name = CommonThings.ROLLUP_VECTORIZED
    output_file_name = CommonThings.CLUSTERS
    
    
    # t1 = time.time()
    # do_the_thing(input_file_name, output_file_name)

    # duration = time.time() - t1
    # msg = f"execution={duration} seconds; input={input_file_name}; output={output_file_name}"
    # yellow(msg)


    input_file_name = CommonThings.ROLLUP_VECTORIZED
    output_file_name = CommonThings.CLUSTERS
    bands = [(1, 1000), (1001, 5000), (5001, 10000)]
    loop = 0 
    for band in bands:
        low, high = band
        mode = 'w' if loop == 0 else 'a'
        loop += 1
        do_the_thing(input_file_name, output_file_name, mode, low, high, loop)
        yellow(f"loop={loop} of {len(bands)}")
