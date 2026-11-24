# Runs the app on Vercel as a container (project framework "Container"; Vercel builds this file on deploy).
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# only what the app reads at run time
COPY sellers_app.py sellers.xlsx ./

# Vercel sends traffic to port 80 unless PORT is set in the project settings
CMD ["sh", "-c", "streamlit run sellers_app.py --server.port=${PORT:-80} --server.address=0.0.0.0 --server.headless=true"]
