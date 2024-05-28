import requests
from bs4 import BeautifulSoup, Comment
from collections import Counter
import nltk
from nltk.corpus import stopwords
from urllib.parse import urljoin, urlparse
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Download stopwords and punkt if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')

# Suppress only the single InsecureRequestWarning from urllib3
warnings.simplefilter('ignore', InsecureRequestWarning)

# Social media platforms to detect
social_media_platforms = {
    'Facebook': re.compile(r'facebook\.com', re.I),
    'Twitter': re.compile(r'twitter\.com', re.I),
    'LinkedIn': re.compile(r'linkedin\.com', re.I),
    'Instagram': re.compile(r'instagram\.com', re.I),
    'YouTube': re.compile(r'youtube\.com', re.I),
    'Pinterest': re.compile(r'pinterest\.com', re.I),
    'TikTok': re.compile(r'tiktok\.com', re.I),
    'Reddit': re.compile(r'reddit\.com', re.I)
}

# Create a session with retry strategy
def create_session_with_retries():
    session = requests.Session()
    retry = Retry(
        total=5,
        read=5,
        connect=5,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504)
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    })
    return session

# Function to get all links from a webpage
def get_all_links(url, domain, session):
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Join relative URLs with base URL
            full_url = urljoin(url, href)
            # Check if the link belongs to the same domain
            if urlparse(full_url).netloc == domain:
                links.add(full_url)
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching links from {url}: {e}")
        return set()
    except Exception as e:
        print(f"Unexpected error while fetching links from {url}: {e}")
        return set()

# Function to extract text from a webpage
def extract_text(url, session):
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        texts = soup.stripped_strings
        return ' '.join(texts)
    except requests.exceptions.RequestException as e:
        print(f"Error extracting text from {url}: {e}")
        return ''
    except Exception as e:
        print(f"Unexpected error while extracting text from {url}: {e}")
        return ''

# Function to count images on a webpage
def count_images(url, session):
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        # Count background images in inline styles
        style_tags = soup.find_all(style=True)
        background_images = sum('background-image' in style.get('style', '') for style in style_tags)
        return len(img_tags) + background_images
    except requests.exceptions.RequestException as e:
        print(f"Error counting images on {url}: {e}")
        return 0
    except Exception as e:
        print(f"Unexpected error while counting images on {url}: {e}")
        return 0

# Function to analyze most used keywords
def analyze_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    counter = Counter(words)
    return counter.most_common(10)

# Function to detect common plugins and libraries
def detect_plugins(url, session):
    try:
        response = session.get(url, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script', src=True)
            links = soup.find_all('link', href=True)
            patterns = {
                'jQuery': re.compile(r'jquery.*\.js', re.I),
                'Bootstrap': re.compile(r'bootstrap.*\.js', re.I),
                'React': re.compile(r'react.*\.js', re.I),
                'Vue': re.compile(r'vue.*\.js', re.I),
                'Angular': re.compile(r'angular.*\.js', re.I),
                'Ember': re.compile(r'ember.*\.js', re.I),
                'Backbone': re.compile(r'backbone.*\.js', re.I),
                'WordPress': re.compile(r'/wp-content/', re.I),
                'Drupal': re.compile(r'/sites/default/', re.I),
                'Joomla': re.compile(r'/components/com_', re.I),
                'Magento': re.compile(r'/static/frontend/', re.I),
                'Shopify': re.compile(r'cdn.shopify.com', re.I),
                'Squarespace': re.compile(r'squarespace.*\.js', re.I),
                'Wix': re.compile(r'wix.*\.js', re.I),
                'Google Analytics': re.compile(r'google-analytics\.com/ga\.js', re.I),
                'Google Tag Manager': re.compile(r'googletagmanager\.com/gtm\.js', re.I),
                'jQuery UI': re.compile(r'jquery-ui.*\.js', re.I),
                'Moment.js': re.compile(r'moment.*\.js', re.I),
                'D3.js': re.compile(r'd3.*\.js', re.I),
                'Three.js': re.compile(r'three.*\.js', re.I),
                'Chart.js': re.compile(r'chart.*\.js', re.I),
                'Lodash': re.compile(r'lodash.*\.js', re.I),
                'Underscore.js': re.compile(r'underscore.*\.js', re.I),
                'Handlebars.js': re.compile(r'handlebars.*\.js', re.I),
                'TypeScript': re.compile(r'typescript.*\.js', re.I),
                'Babel': re.compile(r'babel.*\.js', re.I),
                'Webpack': re.compile(r'webpack.*\.js', re.I),
                'Grunt': re.compile(r'grunt.*\.js', re.I),
                'Gulp': re.compile(r'gulp.*\.js', re.I),
                'Flask': re.compile(r'flask.*\.js', re.I),
                'Django': re.compile(r'django.*\.js', re.I),
                'Ruby on Rails': re.compile(r'rails.*\.js', re.I),
                'ASP.NET': re.compile(r'aspnet.*\.js', re.I),
                'Spring': re.compile(r'spring.*\.js', re.I),
                'Laravel': re.compile(r'laravel.*\.js', re.I),
                'Symfony': re.compile(r'symfony.*\.js', re.I),
                'CodeIgniter': re.compile(r'codeigniter.*\.js', re.I),
                'CakePHP': re.compile(r'cakephp.*\.js', re.I),
                'PHP': re.compile(r'\.php', re.I)
            }

            detected_plugins = set()
            
            # Check scripts
            for script in scripts:
                src = script['src']
                for plugin, pattern in patterns.items():
                    if pattern.search(src):
                        detected_plugins.add(plugin)
            
            # Check links
            for link in links:
                href = link['href']
                for plugin, pattern in patterns.items():
                    if pattern.search(href):
                        detected_plugins.add(plugin)

            # Look for indicators of server-side technology in comments and meta tags
            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            for comment in comments:
                if 'php' in comment.lower():
                    detected_plugins.add('PHP')

            # Check response headers for server-side technology indications
            server_header = response.headers.get('Server', '').lower()
            if 'php' in server_header:
                detected_plugins.add('PHP')
            
            # Check URL itself for PHP
            if re.search(r'\.php', url, re.I):
                detected_plugins.add('PHP')

            return detected_plugins if detected_plugins else "No common plugins detected. Likely pure HTML, JavaScript, and CSS."
        else:
            return f"Failed to access {url}. Status code: {response.status_code}"
    except Exception as e:
        return f"Error detecting plugins on {url}: {e}"

# Function to detect social media links
def detect_social_media_links(soup):
    social_media_links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        for platform, pattern in social_media_platforms.items():
            if pattern.search(href):
                social_media_links.add((platform, href))
    return social_media_links

# Main function
def main(start_url):
    start_time = time.time()  # Start the timer
    session = create_session_with_retries()

    domain = urlparse(start_url).netloc
    visited = set()
    to_visit = {start_url}

    all_texts = ''
    total_urls_detected = set()  # Store unique URLs
    total_bandwidth = 0  # Initialize total bandwidth consumed
    total_images = 0  # Initialize total images count
    plugins_detected = set()  # Store detected plugins for the domain
    social_media_links_detected = set()  # Store detected social media links

    while to_visit:
        url = to_visit.pop()
        if url not in visited:
            visited.add(url)
            print(f"Visiting: {url}")
            try:
                response = session.get(url)
                response.raise_for_status()  # Raise HTTPError for bad responses
                all_texts += ' ' + extract_text(url, session)
                links = get_all_links(url, domain, session)
                if links:
                    print(f"Found {len(links)} links on {url}")
                to_visit.update(links - visited)
                total_urls_detected.update(links)

                # Count images
                total_images += count_images(url, session)

                # Calculate bandwidth
                if 'Content-Length' in response.headers:
                    total_bandwidth += int(response.headers['Content-Length'])
                else:
                    total_bandwidth += len(response.content)

                # Detect plugins (only once per domain)
                if not plugins_detected:
                    plugins_detected = detect_plugins(url, session)
                    if isinstance(plugins_detected, set):
                        print(f"Detected plugins or libraries:")
                        for plugin in plugins_detected:
                            print(f"- {plugin}")
                    else:
                        print(plugins_detected)

                # Detect social media links
                soup = BeautifulSoup(response.text, 'html.parser')
                social_media_links = detect_social_media_links(soup)
                social_media_links_detected.update(social_media_links)

            except requests.exceptions.HTTPError as e:
                print(f"HTTP error visiting {url}: {e}")
            except requests.exceptions.RequestException as e:
                print(f"Error visiting {url}: {e}")

    # Analyze keywords
    if all_texts:
        keywords = analyze_keywords(all_texts)
        print("Most used keywords:")
        for word, count in keywords:
            print(f"{word}: {count}")

    end_time = time.time()  # End the timer
    total_time = end_time - start_time

    print(f"\nTotal URLs detected: {len(total_urls_detected)}")
    print(f"Total runtime: {total_time:.2f} seconds")
    print(f"Total bandwidth used: {total_bandwidth / (1024 * 1024):.2f} MB")
    print(f"Total images found: {total_images}")
    print(f"Social media links found:")
    for platform, link in social_media_links_detected:
        print(f"- {platform}: {link}")

# Run the scraper
if __name__ == "__main__":
    start_url = "https://www.toris.co.za/"  # Replace with the starting URL
    main(start_url)
