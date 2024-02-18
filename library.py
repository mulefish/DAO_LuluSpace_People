import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# from collections import Counter

class CommonThings:
    CSV_TDD = "static/tdd_data.csv"
    ROLLUP_PII_FREE='static/rollup_pii_free.csv'
    ROLLUP_VECTORIZED='static/vectorized_rollup.csv'
    PRECISION=6 # how far to the right of the decimal
    CLUSTERS='static/cluster.csv'
    # CLUSTERS2='data/cluster2.png'

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



def normalize_matrix_round_concat(df, precision):

    """
    Normalize all columns including 'sessions' and 'tlv', while preserving their original values.
    Prepend these original values to each row with the names 'ORIGINAL_SESSIONS' and 'ORIGINAL_TLV'.
    Ensure that numbers effectively rounding to 0.0000 are just represented as 0.
    """

    # Preserve original values of 'sessions' and 'tlv'
    original_sessions = df['sessions'].copy()
    original_tlv = df['tlv'].copy()

    scaler = MinMaxScaler()

    # Normalize the entire DataFrame
    normalized_df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    # Define a small threshold based on precision to treat values as zero
    threshold = 10 ** -precision

    # Apply rounding and replace values effectively zero with 0
    format_str = f"{{:.{precision}f}}"  # Construct format string based on precision
    normalized_df = normalized_df.applymap(lambda x: format_str.format(x).rstrip('0').rstrip('.') if abs(x) >= threshold else '0')

    # Prepend original 'sessions' and 'tlv' values to the normalized DataFrame
    normalized_df.insert(0, 'ORIGINAL_TLV', original_tlv)
    normalized_df.insert(0, 'ORIGINAL_SESSIONS', original_sessions)

    return normalized_df




def find_most_common_vectors(filtered_df, group, n, precision, LOW, HIGH, LOOP):
    n_clusters = 10
    COUNT = filtered_df['count']
    
    # Dropping specified columns before clustering
    filtered_df = filtered_df.drop(['ORIGINAL_SESSIONS', 'sessions', 'count', 'tlv'], axis=1)
    
    if len(filtered_df) < n_clusters:
        print(f"Number of samples ({len(filtered_df)}) is less than the number of clusters ({n_clusters}). "
              f"Reducing the number of clusters to match the number of samples.")
        n_clusters = len(filtered_df)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(filtered_df)
    
    cluster_labels = kmeans.labels_
    cluster_info = pd.DataFrame({'CLUSTER': range(n_clusters)})    
    cluster_counts = pd.Series(cluster_labels).value_counts().sort_index().items()
    
    # Creating DataFrame of most common vectors in each cluster
    most_common_df = pd.DataFrame(kmeans.cluster_centers_, columns=filtered_df.columns)
    most_common_df['FREQUENCY'] = [count for _, count in cluster_counts]
    most_common_df['CLUSTER'] = range(n_clusters)
    most_common_df = pd.merge(most_common_df, cluster_info, on='CLUSTER', how='left')
    most_common_df['GROUP'] = group
    most_common_df['N'] = n
    most_common_df['LOW'] = LOW
    most_common_df['HIGH'] = HIGH
    most_common_df['LOOP'] = LOOP
    
    # Reordering columns
    most_common_df = most_common_df[['CLUSTER', 'FREQUENCY', 'GROUP', 'N', 'LOW', 'HIGH', 'LOOP'] +
                                    [col for col in most_common_df.columns
                                     if col not in ['CLUSTER', 'FREQUENCY', 'GROUP', 'N', 'LOW', 'HIGH', 'LOOP']]]
    
    # Rounding and formatting
    most_common_df = most_common_df.round(precision).replace(0, 0.0)
    
    # Saving to CSV
    most_common_df.to_csv('output.csv', index=False, float_format=f'%.{precision}f')    
    return most_common_df
