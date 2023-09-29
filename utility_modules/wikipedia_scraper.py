import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


def extract_wikipedia_content(url, language='en', section=None, extract=None):
    """
    Extracts the main content from a Wikipedia page.

    Args:
    - url (str): The URL of the Wikipedia page.
    - language (str): The language of the Wikipedia page. Defaults to 'en'.
    - section (str): The section of the Wikipedia page to extract. Defaults to None (i.e. the entire page).
    - extract (list): A list of options to extract. Valid options are 'images' and 'links'. Defaults to None.

    Returns:
    - str: The extracted content.
    """
    # Validate input URL
    parsed_url = urlparse(url)
    if parsed_url.netloc != f"{language}.wikipedia.org" or not parsed_url.path.startswith("/wiki/"):
        print("Error: Invalid Wikipedia page URL.")
        return None

    try:
        with requests.get(url) as response:
            response.raise_for_status()  # Raise an exception for HTTP errors

            soup = BeautifulSoup(response.content, 'html.parser')

            content_div = soup.find('div', class_='mw-parser-output')
            if content_div is None:
                print("Error: No content found on the page.")
                return None

            if section:
                section_heading = content_div.find('span', {'id': section})
                if section_heading is None:
                    print(f"Error: Section '{section}' not found on the page.")
                    return None
                content_elements = []
                for sibling in section_heading.find_next_siblings():
                    if sibling.name and sibling.name.startswith('h'):
                        break
                    content_elements.append(sibling)
                content = "\n".join(element.get_text() for element in content_elements)
            else:
                paragraphs = content_div.find_all('p')
                content = "\n".join(p.get_text() for p in paragraphs)

            if extract:
                if 'images' in extract:
                    images = content_div.find_all('img', src=True)
                    image_urls = [img['src'] for img in images]
                    content += "\n\n" + "\n".join(image_urls)

                if 'links' in extract:
                    links = content_div.find_all('a', href=True)
                    link_urls = [link['href'] for link in links]
                    content += "\n\n" + "\n".join(link_urls)

            return content

    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/OpenAI"
    content = extract_wikipedia_content(url, language='en')
    if content:
        # Remove any images or links from the content
        content = re.sub(r'\[\d+\]', '', content)
        if content:
            print(content[:1000])  # Print the first 1000 characters for testing
        else:
            print("No content extracted.")
        print(content[:1000])  # Print the first 1000 characters for testing
    else:
        print("No content extracted.")
