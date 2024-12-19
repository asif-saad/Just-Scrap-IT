import requests
from bs4 import BeautifulSoup

def scrape_website(url, output_file):
    # Define headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return
    
    # Ensure the response is decoded using UTF-8
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate the <fieldset> tag with class "main-area1"
    fieldset = soup.find('fieldset', class_='main-area1')
    if not fieldset:
        print("No <fieldset> tag with class 'main-area1' found on the page.")
        return
    
    # Find all <button> tags within the <fieldset>
    buttons = fieldset.find_all('button', {'class': 'btn_default4 bdr_radius2'})
    
    urls = []
    for idx, button in enumerate(buttons, 1):
        onclick_content = button.get('onclick', '')
        if "location.href=" in onclick_content:
            url = onclick_content.split("'")[1]  # Extract the URL enclosed in single quotes
            urls.append(url)
            # print(f"{url}")
    
    try:
        with open(output_file, 'a', encoding='utf-8') as file:  # Append to the file
            for url in urls:
                file.write(url + '\n')
        # print(f"\nSuccessfully wrote {len(urls)} URLs to '{output_file}'.")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    input_file = "letter_urls.txt"  # File containing all the URLs
    output_file = "prefix_urls.txt"  # File to save the results

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            urls = file.readlines()  # Read all lines from the input file
        
        for url in urls:
            target_url = url.strip()  # Remove leading/trailing whitespace
            # print(f"Processing URL: {target_url}")
            scrape_website(target_url, output_file)
    
    except FileNotFoundError:
        print(f"The file '{input_file}' was not found.")
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
