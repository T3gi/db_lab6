## Requirements

- Python 3.9+
- MySQL 5.7 або вище
- pip

## Installation

1. Clone repo:
   ```bash
   git clone https://your-repo-url.git
   cd your-repo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
  
3. Set connection to MySQL in database.py:
   ```
   DATABASE_URL = "mysql+pymysql://<user>:<password>@localhost/<dbname>"
   ```
  
4. Create MySQL database:
   ```
   CREATE DATABASE your_db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```


5. Start the server:
   ```
   uvicorn main:app --reload
   ```

6. Check your server on the `http://127.0.0.1:8000`