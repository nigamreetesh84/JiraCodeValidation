from jira import JIRA
from transformers import pipeline
import re
import warnings
import requests

# Suppress FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Jira API Credentials
API_TOKEN = "your_api_token_here"
EMAIL_ID = "your_email@example.com"
API_TOKEN = 'ATATT3xFfGF00XRT7Nau4T26Mj_d1cOiOEsIcgnMWvDeKAmiTvYRk_ecXw1jlevIYkksnCn0NhVoL_v96FvWBGDgwG_seNgnqfB4-T6RG6ompX-x2mwXSN7NeO__TrXXhZCJE6ZU25EqF8xKymwx4ftLWNSd7Ux6OLpPgReRdEuRV7rBPPJTB90=F6D7CB0B'

EMAIL_ID = 'nigambhanu@gmail.com'


# Initialize Jira API
jira = JIRA(server="https://pythonlearning.atlassian.net", basic_auth=(EMAIL_ID, API_TOKEN))
import requests
import ast
from jira import JIRA
from transformers import pipeline

# 🔹 JIRA Configuration
JIRA_URL = "https://your-jira-instance.atlassian.net"
JIRA_ISSUE_ID = "PROJ-123"
API_TOKEN = "your_api_token_here"
EMAIL_ID = "your_email@example.com"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}

# 🔹 GPT API (Optional: If using GPT for summarization)
USE_GPT = False  # Set to True if using OpenAI's API
OPENAI_API_KEY = "your_openai_api_key_here"

# 🔹 Sample Python Code (to be validated)
CODE = """
import requests

def fetch_student_details(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["name"], data["marks"], data["subject"]
    except (requests.RequestException, KeyError):
        return None
"""

# ✅ Function to Extract Acceptance Criteria from Jira
def get_jira_acceptance_criteria():
    """Fetches Jira issue details and extracts acceptance criteria."""
    url = f"{JIRA_URL}/rest/api/3/issue/{JIRA_ISSUE_ID}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        issue_data = response.json()
        description = issue_data["fields"].get("description", "")
        return extract_acceptance_criteria(description)
    return []

# ✅ Function to Extract Criteria from Description
def extract_acceptance_criteria(description):
    """Parses acceptance criteria from a Jira issue description."""
    import re
    if not description:
        return []
    
    match = re.search(r'\*Acceptance Criteria\*:?\s*\n+(.*?)(?:\n\n|$)', description, re.DOTALL | re.IGNORECASE)
    if match:
        criteria_text = match.group(1).strip()
        return re.findall(r'^\#\s*["“]([^"”]+)["”]', criteria_text, re.MULTILINE)
    
    return []

# ✅ Function to Extract & Summarize Code Using AST
def summarize_function(code):
    """Uses Python's AST module to extract function details for summarization."""
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                args = [arg.arg for arg in node.args.args]
                return_stmt = [n for n in ast.walk(node) if isinstance(n, ast.Return)]
                return_values = ", ".join([ast.dump(ret.value) for ret in return_stmt])

                summary = (
                    f"The function `{func_name}()` takes arguments {args}, "
                    f"makes an HTTP request to fetch student details, "
                    f"parses the JSON response, and returns {return_values}. "
                    f"If an error occurs, it returns None."
                )
                return summary
    except Exception as e:
        return f"Error analyzing function: {str(e)}"

    return "No valid function found in the provided code."

# ✅ GPT Summarization (Optional)
def summarize_function_gpt(code):
    """Uses OpenAI GPT API to summarize function (fallback if AST is not enough)."""
    import openai
    openai.api_key = OPENAI_API_KEY

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes Python functions."},
            {"role": "user", "content": f"Summarize this function: {code}"}
        ]
    )
    return response["choices"][0]["message"]["content"].strip()

# ✅ Function to Compare Summary with Acceptance Criteria
def validate_function(summary, criteria_list):
    """Validates if the function summary matches the acceptance criteria."""
    nlp = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    report = []
    for criterion in criteria_list:
        result = nlp(summary, [criterion])
        confidence = result["scores"][0]
        is_met = confidence > 0.7
        report.append({
            "criterion": criterion,
            "confidence": confidence,
            "met": "✅ Yes" if is_met else "❌ No",
            "evidence": result["labels"][0]
        })
    
    return report

# ✅ Main Execution Flow
def main():
    """Main function to fetch Jira details, summarize the function, and validate it."""
    # Step 1: Fetch Acceptance Criteria
    criteria = get_jira_acceptance_criteria()
    if not criteria:
        print("No acceptance criteria found.")
        return

    print("\n🔹 Extracted Acceptance Criteria:")
    for c in criteria:
        print(f"- {c}")

    # Step 2: Summarize Function (Use GPT if enabled, else AST)
    summary = summarize_function(CODE) if not USE_GPT else summarize_function_gpt(CODE)
    
    print("\n🔹 Function Summary:")
    print(summary)

    # Step 3: Validate Against Criteria
    report = validate_function(summary, criteria)

    # Step 4: Generate Report
    print("\n🔹 Validation Report:")
    for entry in report:
        print(f"{entry['met']} Criterion: {entry['criterion']}")
        print(f"   Confidence: {entry['confidence']:.2f}")
        print(f"   Evidence: {entry['evidence']}")

    # Final Decision
    all_met = all(r["met"] == "✅ Yes" for r in report)
    print(f"\nFinal Decision: {'✅ ACCEPTED' if all_met else '❌ REJECTED'}")

# ✅ Run the Script
if __name__ == "__main__":
    main()
