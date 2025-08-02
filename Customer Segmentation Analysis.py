import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# MAIN LOGIC
# ------------------------------
def main():
    df = load_transaction_data("data.csv")  # Load dataset
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])  # Convert date column

    rfm_df = compute_rfm_metrics(df)  # Create RFM table
    assign_customer_segments(rfm_df)  # Add segment classification
    print(rfm_df.head())

    plot_segment_distribution(rfm_df)  # Create bar & pie charts
    save_rfm_to_csv(rfm_df,'rfm_output.csv')


# ------------------------------
# LOAD AND PREPARE DATA
# ------------------------------
def load_transaction_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
        print("Missing values per column:\n", df.isnull().sum())
        print("Dataset summary:\n", df.describe())
        return df
    except:
        raise TypeError("The file doesn't exist or couldn't be loaded.")


# ------------------------------
# COMPUTE RFM METRICS
# ------------------------------
def compute_rfm_metrics(df):
    # Reference date = most recent invoice
    reference_date = df["InvoiceDate"].max()

    # Recency: Days since last purchase
    recency_df = df.groupby('CustomerID')["InvoiceDate"].max().reset_index()
    recency_df["Recency"] = (reference_date - recency_df['InvoiceDate']).dt.days

    # Frequency: Number of purchases
    frequency_df = df.groupby('CustomerID')['InvoiceNo'].count().reset_index()
    frequency_df.rename(columns={'InvoiceNo': 'Frequency'}, inplace=True)

    # Monetary: Total amount spent
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    monetary_df = df.groupby('CustomerID')['TotalPrice'].sum().reset_index()
    monetary_df.rename(columns={'TotalPrice': 'Monetary'}, inplace=True)

    # Merge RFM tables
    rfm_df = recency_df.merge(frequency_df, on='CustomerID')
    rfm_df = rfm_df.merge(monetary_df, on='CustomerID')

    print("\nRFM Table Info:")
    print(rfm_df.info())

    return rfm_df

# ------------------------------
# SEGMENT CUSTOMERS
# ------------------------------
def assign_customer_segments(rfm_df):
    # Score each R, F, M metric from 1–5
    rfm_df["R"] = pd.qcut(rfm_df["Recency"], 5, labels=[5, 4, 3, 2, 1])
    rfm_df["F"] = pd.qcut(rfm_df["Frequency"].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm_df["M"] = pd.qcut(rfm_df["Monetary"], 5, labels=[1, 2, 3, 4, 5])

    # Combine into RFM score string
    rfm_df["RFM_Score"] = rfm_df["R"].astype(str) + rfm_df["F"].astype(str) + rfm_df["M"].astype(str)

    # Classify segments based on RFM Score
    rfm_df["Segment"] = rfm_df["RFM_Score"].apply(
        lambda x: 'Champion' if x == '555' else
                  'Loyal' if x[1] == '5' else
                  'At Risk' if x[0] == '1' else
                  'Big Spenders' if x[2] == '5' else
                  'Lost' if x == '111' else
                  'Potential Loyalist' if x[1] in ['2', '3'] and x[0] in ['4', '5'] else
                  "Can't Lose Them" if x[0] == '1' and x[2] in ['4', '5'] else
                  'Others'
    )


# ------------------------------
# VISUALIZE SEGMENTS
# ------------------------------
def plot_segment_distribution(rfm_df):
    # Count customers in each segment
    segment_counts = rfm_df['Segment'].value_counts()

    # Define consistent colors for each segment
    segment_colors_map = {
        'Champion': '#2ca02c',             # Green
        'Loyal': '#1f77b4',                # Blue
        'At Risk': '#ff7f0e',              # Orange
        'Big Spenders': '#9467bd',         # Purple
        'Lost': '#d62728',                 # Red
        'Potential Loyalist': '#17becf',   # Cyan
        "Can't Lose Them": '#e377c2',      # Pink
        'Others': '#7f7f7f'                # Gray
    }

    # Match colors to segment order
    labels = segment_counts.index
    values = segment_counts.values
    colors = [segment_colors_map[label] for label in labels]

    # Create side-by-side bar chart and pie chart
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Bar chart
    axs[0].bar(labels, values, color=colors)
    axs[0].set_title("Customer Segment Distribution (Bar)")
    axs[0].set_ylabel("Number of Customers")

    # Pie chart
    axs[1].pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    axs[1].set_title("Customer Segment Distribution (Pie)")
    axs[1].axis('equal')

    plt.tight_layout()
    plt.savefig("Customer_Segments.png")
    plt.show()
def save_rfm_to_csv(rfm_df, filename):
    # Save the DataFrame
    rfm_df.to_csv(filename, index=False)

# ------------------------------
# RUN MAIN
# ------------------------------
if __name__ == '__main__':
    main()