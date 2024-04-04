from django.shortcuts import render, HttpResponse, redirect, reverse
from bs4 import BeautifulSoup
import requests


def newfunction(request):
    if request.method == 'GET':
        return render(request, 'jasim.html')
    elif request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            return HttpResponse("No URL provided.")

        response = requests.get(url)
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        for div in soup.find_all('div'):
            div.unwrap()

        for h2 in soup.find_all('h2'):
            center_tag = soup.new_tag('center')
            h2.wrap(center_tag)

        # Replace '&#8226;' with a bullet point character inside all <p> tags
        for p_tag in soup.find_all('p'):
            if p_tag.string and '&#8226;' in p_tag.string:
                p_tag.string.replace_with(p_tag.string.replace('&#8226;', '•'))

        # Find the <body> tag and get the HTML starting from it
        body_tag = soup.find('body')
        if body_tag:
            body_html = str(body_tag)

            # Remove everything before the <body> tag
            soup.clear()
            soup.append(BeautifulSoup(body_html, 'html.parser'))

            # Wrap text outside of any tags with <p> tags
        for element in soup.find_all(['body', 'html']):
            for child in element.children:
                if child.name is None and child.string:
                    p_tag = soup.new_tag('p')
                    p_tag.string = child.string
                    child.replace_with(p_tag)

        # Remove <p> tags without any text
        for p_tag in soup.find_all('p'):
            if not p_tag.get_text(strip=True):
                p_tag.decompose()

        # Remove <br> tags between <img> and <p> tags
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            next_tag = img_tag.find_next(['p', 'br'])
            while next_tag and next_tag.name != 'p':
                if next_tag.name == 'br':
                    next_tag.decompose()
                    next_tag = next_tag.find_next(['p', 'br'])
        # Remove <br> tags that are not directly within <p> tags
        for br_tag in soup.find_all('br'):
            parent_tag = br_tag.find_parent('p')
            if not parent_tag:
                br_tag.decompose()

        # Remove class="thumbnail" from all elements
        for element in soup.find_all(class_='thumbnail'):
            element.attrs.pop('class', None)

        # Find all elements in the HTML document
        all_elements = soup.find_all()

        # Remove attributes from each element
        for element in all_elements:
            if 'border' in element.attrs:
                del element['border']
                if 'alt' in element.attrs:
                    del element['alt']

        # Remove all occurrences of "&amp;" from the text content of all tags
        for tag in soup.find_all():
            if tag.string:
                tag.string = tag.string.replace('&amp;', '')

        # Remove all <body> tags
        for body_tag in soup.find_all('body'):
            body_tag.unwrap()

        return HttpResponse(str(soup.prettify()))



