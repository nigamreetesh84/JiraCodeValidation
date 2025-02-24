API_TOKEN = 'ATATT3xFfGF00XRT7Nau4T26Mj_d1cOiOEsIcgnMWvDeKAmiTvYRk_ecXw1jlevIYkksnCn0NhVoL_v96FvWBGDgwG_seNgnqfB4-T6RG6ompX-x2mwXSN7NeO__TrXXhZCJE6ZU25EqF8xKymwx4ftLWNSd7Ux6OLpPgReRdEuRV7rBPPJTB90=F6D7CB0B'

EMAIL_ID = 'nigambhanu@gmail.com'
from jira import JIRA
from transformers import pipeline
import re
import warnings
from jira import JIRA
from transformers import pipeline
import re
import warnings
from jira import JIRA
from transformers import pipeline
import re
import warnings

# Suppress FutureWarning to clean output for demo
warnings.filterwarnings("ignore", category=FutureWarning)

# Initialize Jira and DistilBERT
jira = JIRA(server="https://pythonlearning.atlassian.net", basic_auth=(EMAIL_ID, API_TOKEN))
nlp = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Correct code to validate (ensures all criteria are met)
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

def extract_acceptance_criteria(description):
    """Parse acceptance criteria from Jira description with flexible regex for # format."""
    if not description:
        return []
    
    # Normalize line breaks (Windows/Unix compatibility)
    description = description.replace('\r\n', '\n').replace('\r', '\n')
    
    # Match '*Acceptance Criteria*:' (case-insensitive) followed by lines starting with #
    match = re.search(r'\*Acceptance Criteria\*:?\s*\n+(.*?)(?:\n\n|$)', description, re.DOTALL | re.IGNORECASE)
    if match:
        criteria_text = match.group(1).strip()
        # Extract lines starting with # and containing quoted text (straight or curly quotes)
        criteria = re.findall(r'^\#\s*["“]([^"”]+)["”]', criteria_text, re.MULTILINE)
        return criteria
    return []

def validate_criteria_with_ai(criteria_list, code):
    """Validate code against criteria using DistilBERT, focusing on key sections."""
    report = []
    # Extract just the function body for better context handling (remove import and whitespace)
    function_code = re.search(r'def fetch_student_details$$ url $$:.*?(?=\n\n|\Z)', code, re.DOTALL)
    if function_code:
        function_code = function_code.group(0).strip()
        # Remove leading/trailing whitespace and ensure no extra lines
        function_code = '\n'.join(line.strip() for line in function_code.split('\n') if line.strip())
    else:
        function_code = code.strip()  # Fallback to full code if function not found

    for criterion in criteria_list:
        # Try with function code first
        try:
            result = nlp(question=criterion, context=function_code)
            is_met = result["score"] > 0.7
            evidence = result["answer"] if is_met else "No evidence found"
            confidence = result["score"]
        except Exception as e:
            print(f"Error processing criterion '{criterion}': {e}")
            is_met = False
            evidence = "Error in processing"
            confidence = 0.0

        # Fallback: Use full code if function code fails and full code is longer
        if not is_met and len(code.strip()) > len(function_code):
            try:
                result_full = nlp(question=criterion, context=code.strip())
                if result_full["score"] > 0.7:
                    is_met = True
                    evidence = result_full["answer"]
                    confidence = result_full["score"]
            except Exception as e:
                print(f"Fallback error for criterion '{criterion}': {e}")

        report.append({
            "criterion": criterion,
            "confidence": confidence,
            "met": "Yes" if is_met else "No",
            "evidence": evidence
        })
    return report

def generate_report(issue_key, report):
    """Generate a demo-friendly report."""
    print(f"\n=== Validation Report for {issue_key} ===")
    for entry in report:
        status = "✅" if entry["met"] == "Yes" else "❌"
        print(f"{status} Criterion: {entry['criterion']}")
        print(f"   Confidence: {entry['confidence']:.2f}")
        print(f"   Status: {entry['met']}")
        print(f"   Evidence: {entry['evidence']}")
    all_met = all(r["met"] == "Yes" for r in report)
    print(f"\nDecision: {'✅ ACCEPTED' if all_met else '❌ REJECTED'}")

def main():
    # Test DistilBERT before validation
    def test_distilbert():
        result = nlp(question="What fields are fetched?", context=CODE)
        print(f"DistilBERT Test: {result}")
        return result["score"] > 0.7

    if not test_distilbert():
        print("DistilBERT test failed. Check model or environment.")
        return

    # Fetch issue details
    issue_key = "LOG-1"
    issue = jira.issue(issue_key)

    # Print basic details
    print(f"Summary: {issue.fields.summary}")
    print(f"Description: {issue.fields.description}")
    print(f"Status: {issue.fields.status.name}")

    # Extract and validate acceptance criteria
    criteria = extract_acceptance_criteria(issue.fields.description)
    if not criteria:
        print("No acceptance criteria found in description. Check formatting.")
        return

    print("\nExtracted Acceptance Criteria:")
    for c in criteria:
        print(f"- {c}")

    # Validate code against criteria
    report = validate_criteria_with_ai(criteria, CODE)
    generate_report(issue_key, report)

if __name__ == "__main__":
    main()