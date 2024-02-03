import re

import requests
import os

from bs4 import BeautifulSoup
import csv


from secret_key import ik_key

token_api=ik_key


# Check if the API key is present
if not token_api:
    raise ValueError("API key not found. Make sure to set the IK_API_KEY environment variable.")

headers = {
            'authorization': f"Token {token_api}"
        }


def remove_text(input_string, start_constant, end_constant):
    pattern = re.escape(start_constant) + r".*?" + re.escape(end_constant)
    output_string = re.sub(pattern, '', input_string)
    return output_string


def clean_text(res):
    documenttext = res['doc']
    html_string = str(documenttext)
    escaped_string = bytes(html_string, 'utf-8').decode('unicode-escape')
    soup = BeautifulSoup(escaped_string, "html.parser")
    attachments_spans = soup.find_all('span', class_='akn-attachments')
    for span in attachments_spans:
        span.extract()
    modified_html = str(soup)
    soup2 = BeautifulSoup (modified_html, 'html.parser')
    text = str(soup2.get_text())
    initialremove = remove_text(text, start_constant="{'tid", end_constant="'doc': '")
    secondremove = remove_text(initialremove, start_constant="'numcites': ", end_constant="'courtcopy': ")
    return secondremove, modified_html

def extract_sections(modified_html):
    soup = BeautifulSoup(modified_html, 'html.parser')

    # Find all <section> elements with id="section_<number between 1 to 1000>"
    sections = soup.find_all('section', id=lambda x: x and x.startswith('section_'))

    # Create a CSV file
    csv_filename = 'sections.csv'

    with open(csv_filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
    
        # Write CSV header
        writer.writerow(['Section Title', 'Nested Content'])
        
        # Iterate through <section> elements and write to CSV
        for section in sections:
            section_title_init = section.find(['h2', 'h3'])

            if section_title_init:
                section_title = section_title_init.text.strip()
            else:
                pass
            
            # Check if there is nested content
            nested_content_spans = section.find_all('span', class_='akn-p')
            nested_contents = []
            for span in nested_content_spans:
                nested_content = span.text.strip()
                nested_contents.append(nested_content)
            
            writer.writerow([section_title, ', '.join(nested_contents)])

def extract_text(doc_number):
    url = f'https://api.indiankanoon.org/doc/{doc_number}/'
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Checks for HTTP request errors

        res = response.json()

        cleaned_text, modified_html = clean_text(res)

        extract_sections(modified_html)

        '''with open("cleaned_text.txt", "w") as file:
            file.write(cleaned_text)

        with open("Response.txt", "w") as file:
            file.write(str(res))
        '''

        #return res

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print(extract_text(69243531))
    #print(extract_text(159820889))
    '''with open('Response.txt', 'r') as html_file:
        html_contents=html_file.read()

    extract_sections(html_contents)
    '''
