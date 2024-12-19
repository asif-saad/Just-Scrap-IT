import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_website_to_excel(url, output_file):
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

    # Check if file exists and append data if it does
    try:
        if os.path.exists(output_file):
            existing_df = pd.read_excel(output_file, engine='openpyxl')
            new_df = pd.DataFrame(span_text, columns=["Original Word"])
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.to_excel(output_file, index=False, engine='openpyxl')
            print(f"\nAppended {len(span_text)} words to '{output_file}'.")
            if len(span_text)==0:
                print(url)
        else:
            new_df = pd.DataFrame(span_text, columns=["Original Word"])
            new_df.to_excel(output_file, index=False, engine='openpyxl')
            print(f"\nSuccessfully wrote {len(span_text)} words to '{output_file}'.")
    except Exception as e:
        print(f"Error writing to Excel file: {e}")



# if __name__ == "__main__":
#     target_url = "https://www.bdword.com/bengali-to-english-dictionary"
#     output_file = "Original_to_Dialect.xlsx"
#     scrape_website_to_excel(target_url, output_file)
