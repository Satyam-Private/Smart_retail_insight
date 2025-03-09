import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data(file_path):
    """
    Load the CSV data into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully!")
        return df
    except Exception as e:
        raise Exception(f"Error loading CSV file: {e}")

def preprocess_data(df):
    """
    Preprocess the data:
    - Convert the 'Date' column to datetime if it exists.
    - Create a 'Revenue' column if not present.
    """
    if 'Date' in df.columns:
        try:
            df['Date'] = pd.to_datetime(df['Date'])
        except Exception as e:
            print("Error converting Date column:", e)
    
    # Create 'Revenue' column if it doesn't exist and if Quantity and Price columns are available.
    if 'Revenue' not in df.columns:
        if 'Quantity' in df.columns and 'Price' in df.columns:
            df['Revenue'] = df['Quantity'] * df['Price']
        else:
            raise Exception("Missing 'Quantity' or 'Price' columns. Cannot compute Revenue.")
    return df

def sales_overview(df):
    """
    Return an overview of sales including total revenue and total units sold.
    """
    total_revenue = df['Revenue'].sum()
    total_sales = df['Quantity'].sum()
    return {'total_revenue': round(total_revenue, 2), 'total_sales': total_sales}

def top_products(df, n=10):
    """
    Return the top N products by revenue.
    """
    product_summary = df.groupby('Product').agg({'Quantity': 'sum', 'Revenue': 'sum'})
    product_summary = product_summary.sort_values(by='Revenue', ascending=False).reset_index()
    return product_summary.head(n)

def revenue_trend(df, output_dir="outputs"):
    """
    Plot the daily revenue trend and save the plot.
    """
    if 'Date' in df.columns:
        daily_revenue = df.groupby(df['Date'].dt.date)['Revenue'].sum()
        plt.figure(figsize=(10,5))
        daily_revenue.plot(kind='line', marker='o')
        plt.title("Daily Revenue Trend")
        plt.xlabel("Date")
        plt.ylabel("Revenue")
        plt.grid(True)
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, "daily_revenue_trend.png")
        plt.savefig(file_path)
        plt.close()
        return file_path
    else:
        return None

def category_insights(df, output_dir="outputs"):
    """
    Provide insights based on product categories and save the corresponding plot.
    """
    if 'Category' in df.columns:
        category_summary = df.groupby('Category').agg({'Quantity': 'sum', 'Revenue': 'sum'})
        category_summary = category_summary.sort_values(by='Revenue', ascending=False)
        plt.figure(figsize=(10,5))
        category_summary['Revenue'].plot(kind='bar')
        plt.title("Revenue by Category")
        plt.xlabel("Category")
        plt.ylabel("Revenue")
        plt.xticks(rotation=45)
        plt.tight_layout()
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, "category_revenue.png")
        plt.savefig(file_path)
        plt.close()
        return file_path, category_summary
    else:
        return None, None



def generate_insights(file_path, output_dir="outputs"):
    """
    Load the CSV file, process the data, and generate insights.
    Returns a dictionary with key metrics and paths to the generated plots.
    """
    df = load_data(file_path)
    df = preprocess_data(df)
    
    results = {}
    results['sales_overview'] = sales_overview(df)
    results['top_products'] = top_products(df).to_dict('records')
    results['revenue_trend'] = revenue_trend(df, output_dir)
    
    cat_img, cat_data = category_insights(df, output_dir)
    results['category_insights_image'] = cat_img
    results['category_insights'] = cat_data.to_dict('records') if cat_data is not None else None

    return results
