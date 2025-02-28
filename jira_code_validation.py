import requests
import csv
import sqlite3
from sentence_transformers import SentenceTransformer, util

# Load a pre-trained model for text and code embeddings
model = SentenceTransformer('microsoft/codebert-base')

def get_similarity_score(text1, text2):
    """Compute cosine similarity between two texts."""
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    score = util.pytorch_cos_sim(emb1, emb2).item()
    return score

def validate_acceptance_criteria(acceptance_criteria, new_code, threshold=0.60):
    """Checks if the new code aligns with the acceptance criteria."""
    similarity_score = get_similarity_score(acceptance_criteria, new_code)

    print(f"Similarity Score: {similarity_score:.2f}")

    if similarity_score >= threshold:
        print("✅ New code meets the acceptance criteria.\n")
    else:
        print("⚠️ Warning: New code might not fully meet the acceptance criteria.\n")

    return similarity_score  # Return the score for further use if needed

# ===========================================
# ✅ Example 1: Fetch Specific Columns from API
# ===========================================

acceptance_criteria_1 = (
    "Write a function `fetch_users` that calls a REST API "
    "(`https://jsonplaceholder.typicode.com/users`) and extracts only "
    "the `id`, `name`, and `email` fields. Return a list of dictionaries."
)

new_code_1 = """import requests
def fetch_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    users = response.json()
    filtered_users = [{"id": u["id"], "name": u["name"], "email": u["email"]} for u in users]
    return filtered_users"""

api_score = validate_acceptance_criteria(acceptance_criteria_1, new_code_1)
print(f"🔹 API Function Validation Score: {api_score:.2f}\n")

# ===========================================
# ✅ Example 2: Writing Data into a CSV File
# ===========================================

acceptance_criteria_2 = (
    "Write a function `save_to_csv` that takes a list of dictionaries and writes the data "
    "to a CSV file named `output.csv`. The dictionary keys should be used as column headers."
)

new_code_2 = """import csv
def save_to_csv(data, filename='output.csv'):
    if not data:
        return 'No data to write.'
    headers = data[0].keys()
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    return f'Data written to {filename}'"""

csv_score = validate_acceptance_criteria(acceptance_criteria_2, new_code_2)
print(f"🔹 CSV Function Validation Score: {csv_score:.2f}\n")

# ===========================================
# ✅ Example 3: Insert Data into SQLite Database
# ===========================================

acceptance_criteria_3 = (
    "Write a function `insert_into_db` that takes a list of dictionaries and inserts them into an SQLite database."
    " The function should connect to the database, insert the data into a table named `users`, and commit the transaction."
)

new_code_3 = """import sqlite3
def insert_into_db(data):
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    for item in data:
        cursor.execute('INSERT INTO users (id, name) VALUES (?, ?)', (item['id'], item['name']))
    connection.commit()
    cursor.close()
    connection.close()
    return 'Data inserted successfully'"""

db_score = validate_acceptance_criteria(acceptance_criteria_3, new_code_3)
print(f"📊 🔹 Database Function Validation Score: {db_score:.2f}\n")

# ===========================================
# ❌ Example 4: Incorrect API Column Extraction
# ===========================================

acceptance_criteria_4 = (
    "Write a function `fetch_users_incorrect` that calls a REST API "
    "(`https://jsonplaceholder.typicode.com/users`) and extracts only "
    "the `id`, `name`, and `address` fields. Return a list of dictionaries."
)

new_code_4 = """import requests
def fetch_users_incorrect():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    users = response.json()
    filtered_users = [{"id": u["id"], "name": u["name"], "email": u["email"]} for u in users]
    return filtered_users"""

incorrect_api_score = validate_acceptance_criteria(acceptance_criteria_4, new_code_4)
print(f"❌ Incorrect API Function Validation Score: {incorrect_api_score:.2f}\n")

# ===========================================
# ❌ Example 5: Incorrect CSV Column Headers
# ===========================================

acceptance_criteria_5 = (
    "Write a function `save_to_csv_incorrect` that takes a list of dictionaries and writes the data "
    "to a CSV file named `output.csv`. The dictionary keys `first_name` and `last_name` should be used as column headers."
)

new_code_5 = """import csv
def save_to_csv_incorrect(data, filename='output.csv'):
    if not data:
        return 'No data to write.'
    headers = data[0].keys()
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    return f'Data written to {filename}'"""

incorrect_csv_score = validate_acceptance_criteria(acceptance_criteria_5, new_code_5)
print(f"❌ Incorrect CSV Function Validation Score: {incorrect_csv_score:.2f}\n")

# ===========================================
# ❌ Example 6: Incorrect SQLite Table Name
# ===========================================

acceptance_criteria_6 = (
    "Write a function `insert_into_db_incorrect` that takes a list of dictionaries and inserts them into an SQLite database."
    " The function should connect to the database, insert the data into a table named `employees`, and commit the transaction."
)

new_code_6 = """import sqlite3
def insert_into_db_incorrect(data):
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    for item in data:
        cursor.execute('INSERT INTO users (id, name) VALUES (?, ?)', (item['id'], item['name']))
    connection.commit()
    cursor.close()
    connection.close()
    return 'Data inserted successfully'"""

incorrect_db_score = validate_acceptance_criteria(acceptance_criteria_6, new_code_6)
print(f"❌ Incorrect Database Function Validation Score: {incorrect_db_score:.2f}\n")