import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
# from collections import Counter

class CommonThings:
    CSV_TDD = "data/tdd_data.csv"
    ROLLUP_PII_FREE='data/rollup_pii_free.csv'
    ROLLUP_VECTORIZED='data/vectorized_rollup.csv'
    PRECISION=6 # how far to the right of the decimal
    CLUSTERS='data/cluster.csv'
    CLUSTERS2='data/cluster2.png'

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



def find_most_common_vectors(filtered_df, group, n, precision):
    """
    This function, find_most_common_vectors, is designed to perform K-means clustering on a filtered DataFrame and generate a DataFrame containing information about the most common vectors in each cluster. Let's break down the steps of the function:
    This function is designed to process input data, perform clustering, and output a DataFrame with detailed cluster information, including average values and frequencies, while adhering to the specified precision requirements.
    """

    n_clusters = 10
    
    # Drop 'ORIGINAL_TLV' and 'ORIGINAL_SESSIONS' columns
    # Drop sessions - do not want to introduce that noise into the normalized data clustering
    filtered_df = filtered_df.drop(['ORIGINAL_TLV', 'ORIGINAL_SESSIONS', 'sessions'], axis=1)
    
    # Adjust number of clusters if the number of samples is less than the number of clusters
    if len(filtered_df) < n_clusters:
        print(f"Number of samples ({len(filtered_df)}) is less than the number of clusters ({n_clusters}). "
              f"Reducing the number of clusters to match the number of samples.")
        n_clusters = len(filtered_df)
    
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(filtered_df)
    
    # Get cluster labels
    cluster_labels = kmeans.labels_
    
    # Calculate the average 'X' (average TLV) and 'Y' (average session count) for each cluster
    cluster_centers = kmeans.cluster_centers_
    cluster_x_values = [filtered_df.loc[cluster_labels == i, 'tlv'].mean() for i in range(n_clusters)]
    
    
    
    # Removed 'sessions' from the calculation! 
    # Y was being set to use sessions. But. Now it is gone. What to replace Y with?
    # Likely nothing. Likely do not need X either, actually.
    cluster_y_values = [0] * n_clusters  # Since 'sessions' is dropped, assign 0 to all cluster y-values
    
    # Create a DataFrame for cluster information
    cluster_info = pd.DataFrame({'Cluster': range(n_clusters), 'X': cluster_x_values, 'Y': cluster_y_values})
    
    # Get cluster counts
    cluster_counts = pd.Series(cluster_labels).value_counts().sort_index().items()
    
    # Convert centroids and counts to DataFrame
    most_common_df = pd.DataFrame(cluster_centers, columns=filtered_df.columns)
    most_common_df['Frequency'] = [count for _, count in cluster_counts]
    
    # Add 'Cluster' column to most_common_df
    most_common_df['Cluster'] = range(n_clusters)
    
    # Merge cluster information with most common vectors DataFrame
    most_common_df = pd.merge(most_common_df, cluster_info, on='Cluster', how='left')
    
    # Add 'Group' and 'N' columns to the DataFrame
    most_common_df['Group'] = group
    most_common_df['N'] = n
    
    # Reorder columns
    most_common_df = most_common_df[['Cluster', 'X', 'Y', 'Frequency', 'Group', 'N'] +
                                    [col for col in most_common_df.columns
                                     if col not in ['Cluster', 'X', 'Y', 'Frequency', 'Group', 'N']]]
    
    # Replace values below precision threshold with 0
    most_common_df = most_common_df.round(precision).replace(0, 0.0)
    
    # Write DataFrame to CSV with specified precision and without scientific notation
    most_common_df.to_csv('output.csv', index=False, float_format=f'%.{precision}f')
    
    return most_common_df