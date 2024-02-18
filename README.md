# REPO
https://github.com/mulefish/DAO_LuluSpace_People

# PII
There is none. Data are in 'rollup_pii_free.csv' and it contains zero PII.

# Steps
- Step 0 ( get rollup_pii_free.csv from the other dyanmodb-2-sql-2-csv project )
- Step 1 ( normalize_everything.py )
    1: divide each person's data by their number of sessions, which is stored in the first column.   
    2: normalize the columns.   
    3: Additionally, prepend the unmodified number of sessions and the unmodified total lifetime value (tlv) to each row in the output CSV.  
- Step 2 ( find_examplars.py ( that spelling looks wrong ))
    1: Perform K-means clustering on a filtered DataFrame and generate a DataFrame containing information about the most common vectors in each cluster. 
    2: process input data, perform clustering, and output a DataFrame with detailed cluster information, including average values and frequencies, while adhering to the specified precision requirements.



# GOAL
Vectorize the matrix, use KNN ( or something ) and find exemplar vectors in the matrix