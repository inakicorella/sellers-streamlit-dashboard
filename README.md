# Sellers dashboard (Streamlit)

Individual activity: a simple Streamlit app for `sellers.xlsx` (52 sellers in the NORTE, SUR, ESTE and OESTE regions).

What it shows:
- A table of sellers filtered by region, with a CSV download
- Charts of units sold, total sales and sales average
- One seller's data, picked from a list

## Run it

```bash
pip install -r requirements.txt
streamlit run sellers_app.py
```

`sellers.xlsx` must stay in the same folder as `sellers_app.py`.

`Sellers_Dashboard_Screenshots.pdf` has screenshots of the running app.
