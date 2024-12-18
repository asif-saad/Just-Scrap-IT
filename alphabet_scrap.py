import requests
from bs4 import BeautifulSoup

def scrape_website(url):
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
    buttons = fieldset.find_all('button')
    
    button_texts = []
    for idx, button in enumerate(buttons, 1):
        button_text = button.get_text(strip=True)
        button_texts.append(f"{idx}. {button_text}")
        print(f"{idx}. {button_text}")
    
    # Define the output file path using a relative path
    output_file = "button_texts.txt"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for text in button_texts:
                file.write(text + '\n')
        print(f"\nSuccessfully wrote {len(button_texts)} button texts to '{output_file}'.")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    target_url = "https://www.bdword.com/bengali-to-english-dictionary-letter-%E0%A6%85"
    scrape_website(target_url)
