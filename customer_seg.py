import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import os

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully!")
        return df
    except Exception as e:
        raise Exception(f"Error loading CSV file: {e}")

def preprocess_data(df):
    if 'TotalSpend' not in df.columns:
        if 'Quantity' in df.columns and 'Price' in df.columns:
            df['TotalSpend'] = df['Quantity'] * df['Price']
        else:
            raise Exception("Missing 'Quantity' or 'Price' columns. Cannot compute TotalSpend.")
    return df

def model(file_path, output_dir="outputs"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = load_data(file_path)
    df = preprocess_data(df)
    df['TotalSpend'] = (df['Quantity'] * df['Price']).astype(int)
    
    le = LabelEncoder()
    df['CustomerID_encoded'] = le.fit_transform(df['CustomerID'])
    
    X = df[['TotalSpend', 'CustomerID_encoded']].values

    plt.scatter(df['TotalSpend'] , df['CustomerID_encoded'])
    plt.ylabel('CustomerID (encoded)')
    plt.xlabel('Total Spend')
    plt.title("before customer segmentation")
    plot_file_path = os.path.join(output_dir, "before_customer_segmentation.png")
    plt.savefig(plot_file_path)

    
    n_clusters = 2
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42)
    Y = kmeans.fit_predict(X)
    
    plt.figure(figsize=(8,8))
    plt.scatter(X[Y==0, 0], X[Y==0, 1], s=50, c='green', label='Cluster 1')
    plt.scatter(X[Y==1, 0], X[Y==1, 1], s=50, c='red', label='Cluster 2')

    
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
                s=100, c='cyan', label='Centroids')
    
    plt.title('After customer segmentation')
    plt.ylabel('CustomerID (encoded)')
    plt.xlabel('Total Spend')
    plt.legend()
    
    plot_file_path = os.path.join(output_dir, "after_customer_segmentation.png")
    plt.savefig(plot_file_path)
    


