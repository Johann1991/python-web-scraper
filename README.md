# Web Scraper Application

## Overview

This is a Python-based web scraping application designed to analyze web pages for various characteristics. It can extract text, detect common web technologies (such as libraries and plugins), count images, detect social media links, and analyze the most used keywords on a website. The application aims to help web developers and researchers gather insights about a website's structure and content.

## Features

- **Text Extraction**: Extracts and combines all text content from the web pages.
- **Technology Detection**: Identifies common libraries, plugins, and server-side technologies used on the website.
- **Image Counting**: Counts all images, including those set as background images in inline styles.
- **Social Media Links Detection**: Detects links to major social media platforms.
- **Keyword Analysis**: Analyzes the most frequently used keywords on the website.
- **Performance Metrics**: Measures the total runtime and bandwidth used during the scraping process.

## Benefits

- **Comprehensive Analysis**: Provides a detailed analysis of web pages, helping developers understand the technologies and content used.
- **Easy Integration**: Can be integrated into other applications or services to automate web analysis tasks.
- **Customizable**: Easily extendable to include more features or support additional technologies.
- **Informative**: Provides insights into the web page's structure and content, aiding in research and development.

## Libraries Used

- `requests`: For making HTTP requests.
- `beautifulsoup4`: For parsing HTML and XML documents.
- `nltk`: For natural language processing tasks, including stopwords and keyword analysis.
- `urllib3`: For handling URL operations and suppressing insecure request warnings.

## Requirements

- **Python Version**: Python 3.6 or higher
- **Pip Version**: Pip 19.0 or higher

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/web-scraper.git
    cd web-scraper
    ```

2. **Create a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Application**:
    ```bash
    python web_summary.py
    ```

2. **Modify Start URL**:
    - Update the `start_url` variable in `web_summary.py` to the desired URL to be scraped.

3. **View Results**:
    - The application will output the analysis results directly in the terminal, including detected technologies, social media links, keyword analysis, and performance metrics.

## Example Output

```
Visiting: https://www.example.com/
Found 10 links on https://www.example.com/
Detected plugins or libraries:
- WordPress
- Bootstrap
- jQuery
- PHP
Most used keywords:
example: 10
website: 8
content: 7
page: 5

Total URLs detected: 10
Total runtime: 3.25 seconds
Total bandwidth used: 0.12 MB
Total images found: 20
Social media links found:
- Facebook: https://www.facebook.com/example
- Twitter: https://www.twitter.com/example
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements, bug fixes, or suggestions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- The `requests` library for making HTTP requests.
- The `beautifulsoup4` library for parsing HTML and XML documents.
- The `nltk` library for natural language processing.
- The `urllib3` library for URL handling.
