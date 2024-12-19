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
    fieldset = soup.find_all('fieldset', class_='main-area1')[1]
    if not fieldset:
        print("No <fieldset> tag with class 'main-area1' found on the page.")
        return

    # Find all <button> tags within the <fieldset>
    buttons = fieldset.find_all('button')

    button_urls = []
    for idx, button in enumerate(buttons, 1):
        button_text = button.get_text(strip=True)
        onclick_content = button.get('onclick', '')
        if "location.href=" in onclick_content:
            url = onclick_content.split("'")[1]  # Extract the URL enclosed in single quotes
            button_urls.append(f"{url}")
            print(f"{url}")

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for text in button_urls:
                file.write(text + '\n')
        print(f"\nSuccessfully wrote {len(button_urls)} button URLs to '{output_file}'.")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    target_url = "https://www.bdword.com/bengali-to-english-dictionary"
    output_file = "letter_urls.txt"
    scrape_website(target_url, output_file)
