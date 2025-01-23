from word_scrap import scrape_website_to_excel

# Function to read URLs starting from a specified line
def read_urls_from_line(file_path, start_line):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # Ensure the starting line is within the range of the file
        if start_line > len(lines):
            raise ValueError("Start line exceeds the number of lines in the file.")
        return lines[start_line - 1:]  # Adjust for zero-based index

# Specify the start line (e.g., line 3)
start_line = 838  # Modify this variable as needed

# Read URLs from the file starting from the specified line
urls = read_urls_from_line('prefix_urls.txt', start_line)

# Initialize a counter for the number of URLs traversed
line_number = start_line

# Loop through each URL in the list
for url in urls:
    # Clean up any surrounding whitespace or newline characters
    target_url = url.strip()  # Adjust this line based on the actual structure of the URLs
    output_excel_file = "Original_to_Dialect.xlsx"  # Static output file name, can be dynamic if needed

    # Call the function to scrape the website and save the data to Excel
    scrape_website_to_excel(target_url, output_excel_file)

    # Print the current line number being traversed
    print(f"Processing line: {line_number}")

    # Increment the line number
    line_number += 1

# Print the total number of URLs traversed
# print(f"Total URLs traversed: {line_number - start_line}")
