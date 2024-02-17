import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from library import yellow, CommonThings, find_most_common_vectors


def find_most_common_vectors(input_file_name, output_file_name, n_clusters=10):
    # Load the CSV file
    df = pd.read_csv(input_file_name)
    
    # Drop 'ORIGINAL_TLV' and 'ORIGINAL_SESSIONS' columns
    df = df.drop(['ORIGINAL_TLV', 'ORIGINAL_SESSIONS'], axis=1)
    
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(df)
    
    # Get cluster labels
    cluster_labels = kmeans.labels_
    
    # Calculate the average 'X' (average TLV) and 'Y' (average session count) for each cluster
    cluster_centers = kmeans.cluster_centers_
    cluster_x_values = [df.loc[cluster_labels == i, 'tlv'].mean() for i in range(n_clusters)]
    cluster_y_values = [df.loc[cluster_labels == i, 'sessions'].mean() for i in range(n_clusters)]
    
    # Get cluster counts
    cluster_counts = pd.Series(cluster_labels).value_counts().sort_index().values
    
    # Plot scatter chart with circles
    plt.figure(figsize=(10, 6))
    for i in range(n_clusters):
        plt.scatter(cluster_x_values[i], cluster_y_values[i], s=cluster_counts[i]*10, alpha=0.5, label=f'Cluster {i+1}')
        plt.annotate(f'Cluster {i+1}', (cluster_x_values[i], cluster_y_values[i]))
        circle = plt.Circle((cluster_x_values[i], cluster_y_values[i]), cluster_counts[i]*10, color='r', fill=False)
        plt.gca().add_patch(circle)
    
    # Plot cluster centroids
    plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], marker='x', color='k', label='Centroids')
    
    # Set plot labels and title
    plt.xlabel('Average TLV (X)')
    plt.ylabel('Average Session Count (Y)')
    plt.title('Clusters with Frequency and Centroids')
    plt.legend()
    
    # Save plot as an image file (e.g., PNG)
    plt.savefig(output_file_name)
    
    # Show plot
    plt.show()

# Example usage
if __name__ == "__main__":

    input_file_name = CommonThings.ROLLUP_VECTORIZED #'input_data.csv'  # Change to your input file name
    output_file_name =CommonThings.CLUSTERS2 # 'cluster_scatter_plot_with_centroids.png'  # Change to desired output file name
    find_most_common_vectors(input_file_name, output_file_name)
