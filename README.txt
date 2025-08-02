Customer Segmentation Analysis (RFM Model)
==========================================

This project performs customer segmentation based on transaction data using the RFM method:
- R: Recency — how recently a customer made a purchase
- F: Frequency — how often a customer makes purchases
- M: Monetary — how much money a customer spends

---------------------------------------------------
Data Used:
---------------------------------------------------
- Source File: data.csv
- Columns required: InvoiceNo, InvoiceDate, CustomerID, Quantity, UnitPrice

---------------------------------------------------
Generated Files:
---------------------------------------------------
1. rfm_output.csv     → Main RFM table with scores and customer segments
2. Customer_Segments.png → Bar chart and pie chart showing segment distribution

---------------------------------------------------
Columns in rfm_output.csv:
---------------------------------------------------
- CustomerID: Unique customer identifier
- Recency: Number of days since last purchase
- Frequency: Number of transactions
- Monetary: Total spending (Quantity × UnitPrice)
- R: Recency score (1–5), where 5 = most recent
- F: Frequency score (1–5), where 5 = most frequent
- M: Monetary score (1–5), where 5 = highest spender
- RFM_Score: A string made by combining R, F, and M (e.g., '555')
- Segment: Customer classification based on RFM score

---------------------------------------------------
Customer Segments:
---------------------------------------------------
- Champion: Score '555' — recent, frequent, and high-spending
- Loyal: Frequency = 5 — frequent buyers
- At Risk: Recency = 1 — haven't purchased in a long time
- Big Spenders: Monetary = 5 — spent the most
- Lost: Score '111' — inactive and low value
- Potential Loyalist: R in [4,5] and F in [2,3] — could become loyal
- Can't Lose Them: R = 1 and M in [4,5] — high spenders, now inactive
- Others: Customers who don’t fit the other categories

---------------------------------------------------
Usage:
---------------------------------------------------
1. Place your `data.csv` in the same directory as the script.
2. Run the script: `python Customer Segmentation Analysis.py`
3. View the output files described above.

---------------------------------------------------
Author: Zaid
Date: 2025-07-29