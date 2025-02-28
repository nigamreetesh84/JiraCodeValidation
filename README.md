# AI-Powered Code Validation System

## Overview

This project automates the validation of newly written code against predefined acceptance criteria using AI/ML. It utilizes the **microsoft/codebert-base** model to measure similarity between the acceptance criteria and the provided code, ensuring that the implementation meets the required standards.

## Features

- **AI-Based Code Comparison**: Uses CodeBERT to compute similarity scores between acceptance criteria and new code.
- **Validation Threshold**: Ensures code meets a minimum similarity score (default: 0.60).
- **Use Cases**:
  - Fetching specific columns from an API response.
  - Writing structured data to a CSV file.
  - Inserting data into an SQLite database.
- **Automated Reporting**: Displays whether the new code meets the acceptance criteria.

## Installation

### Prerequisites

Ensure you have **Python 3.x** installed along with the required dependencies.

### Setup

```sh
# Clone the repository
git clone https://github.com/nigamreetesh84/AI-Code-Validation.git
cd AI-Code-Validation

# Install required dependencies
pip install -r requirements.txt
```

## Usage

Run the script to validate code snippets against their respective acceptance criteria:

```sh
python jira_util_chatgpt.py
```

## Example Validation Output

```sh
No sentence-transformers model found with name microsoft/codebert-base. Creating a new one with mean pooling.
Similarity Score: 0.89
✅ New code meets the acceptance criteria.
```

## File Structure

```
AI-Code-Validation/
│-- jira_util_chatgpt.py  # Main script for validation
│-- requirements.txt      # Required dependencies
│-- README.md             # Project documentation
│-- output.csv            # Generated CSV file (if applicable)
```

## Technologies Used

- **Python**
- **SentenceTransformers (CodeBERT)**
- **SQLite** (for database validation)
- **CSV Handling** (for file validation)
- **Requests** (for API data fetching)

## Contributing

If you'd like to contribute, fork the repository and create a pull request with your improvements.

## Author

**User:** [Reetesh Nigam](https://github.com/nigamreetesh84)

## License

This project is licensed under the MIT License.

