from bs4 import BeautifulSoup
import os

def find_js_css_files(html_file):
    # Check if the file exists
    if not os.path.exists(html_file):
        print("File not found:", html_file)
        return set(), set()
    
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8-sig') as f:
        html_content = f.read()
    
    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all <script> tags with src attribute
    js_files = set([tag['src'] for tag in soup.find_all('script', src=True)])
    
    # Find all <link> tags with rel="stylesheet" attribute
    css_files = set([tag['href'] for tag in soup.find_all('link', rel='stylesheet')])
    
    # Find all <script> tags with type="rocketlazyloadscript" attribute
    rocketlazyload_js_files = set([tag['data-lazy-src'] for tag in soup.find_all('script', {'type':'rocketlazyloadscript'}, data=True)])
    
    js_files.update(rocketlazyload_js_files)
    
    return js_files, css_files

def write_to_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8-sig') as file:
        for item in data:
            file.write("%s\n" % item)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower() == "index.html":
                html_file = os.path.join(root, file)
                js_files, css_files = find_js_css_files(html_file)
                
                # Append JavaScript URLs to js_files_set
                js_files_set.update(js_files)
                
                # Append CSS URLs to css_files_set
                css_files_set.update(css_files)

if __name__ == "__main__":
    # Initialize sets to store unique JavaScript and CSS file URLs
    js_files_set = set()
    css_files_set = set()
    
    # Process the current working directory and its subdirectories
    process_directory(os.getcwd())
    
    # Write JavaScript URLs to js_files.txt
    js_file_path = "js_files.txt"
    write_to_file(js_file_path, js_files_set)
    print(f"JavaScript URLs written to {js_file_path}")
    
    # Write CSS URLs to css_files.txt
    css_file_path = "css_files.txt"
    write_to_file(css_file_path, css_files_set)
    print(f"CSS URLs written to {css_file_path}")
