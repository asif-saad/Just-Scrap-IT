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
    
    # Locate the <div> tag with class "fieldset_body inner_details"
    div = soup.find('div', class_='fieldset_body inner_details')
    if not div:
        print("Div with class 'fieldset_body inner_details' not found.")
        return

    spans = div.find_all('span')
    
    span_text = []
    for span in spans:
        a_tag = span.find('a')
        if a_tag:
            temp = a_tag.get_text(strip=True)
            span_text.append(temp.split(' ', 1)[1] if ' ' in temp else temp)  # Only the text without numbering
            print(temp)  # Print without numbering
    
    # Define the output file path using a relative path
    output_file = "button_texts.txt"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for text in span_text:
                file.write(text + '\n')
        print(f"\nSuccessfully wrote {len(span_text)} button texts to '{output_file}'.")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    target_url = "https://www.bdword.com/bengali-to-english-dictionary-two-letter-%E0%A6%85%E0%A6%AA"
    scrape_website(target_url)
