from bs4 import BeautifulSoup
import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service

def get_comments(url):
    """
    This function uses Selenium to load the dynamic content of the webpage (the comments).
    Selenium is used to handle JavaScript and load the comments that are dynamically added to the webpage.
    """
    service = Service('C:/Codes/msedgedriver.exe')

    driver = webdriver.Edge(service=service)

    driver.get(url)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    comments = []
    
    for comment in soup.find_all('div', {'class': 'issue-data-block'}):
        text = comment.find('div', {'class': 'action-body'}).get_text(separator=' ', strip=True)
        comments.append(text)

    driver.quit()

    return comments

def scrape_jira_issue(url):
    """
    This function uses BeautifulSoup to parse the static HTML content of the webpage.
    It extracts the required fields and then calls the get_comments function to extract the comments.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48'
    }

    response = requests.get(url, headers=headers)  
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the required fields
    issue_type = soup.find('span', {'id': 'type-val'}).text.strip()
    assignee = soup.find('span', {'id': 'assignee-val'}).text.strip()
    created = soup.find('span', {'id': 'created-val'}).text.strip()
    description = soup.find('div', {'class': 'user-content-block'}).get_text(separator=' ', strip=True)
    comments = get_comments(url)

    print(comments)

    with open('jira_issues.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Type", "Assignee", "Created", "Description", "Comments"])
        writer.writerow([issue_type, assignee, created, description, comments])

# Example 
scrape_jira_issue('https://issues.apache.org/jira/browse/CAMEL-10597')
print('Finished')
