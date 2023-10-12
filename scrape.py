# Import necessary libraries
from bs4 import BeautifulSoup
import requests
import json
import csv
from datetime import datetime

# Specify the URL of the webpage to be scraped
url = 'https://glints.com/id/en/opportunities/jobs/programming/14c33dd2-6879-46f9-b294-b3b2e9364200?utm_referrer=explore'

# Define the headers to be used in the request
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://glints.com/id/en/lowongan-kerja',
    'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

# Send an HTTP GET request to the URL with the defined headers
response = requests.get(url, headers=headers)

# Check for a valid response
if response.status_code == 200:
    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the script tag with type "application/ld+json"
    script_tag = soup.find('script', {'type': 'application/ld+json'})

    # Load the JSON string from the script tag
    job_data = json.loads(script_tag.string)
    ## Name job
    job_title = job_data['title']
    ## job date posted
    date_str = job_data['datePosted']
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    job_date_posted = date_obj.strftime('%d-%m-%Y')

    ## job city location
    job_location = job_data['jobLocation']['address']['addressLocality']

    ## company hiring name
    company_hiring = job_data['hiringOrganization']['name']

    ## URL job
    # Find the <link> tag with rel="canonical"
    link_tag = soup.find('link', {'rel': 'canonical'})
    # Extract the URL from the href attribute of the <link> tag
    url_job = link_tag['href'] if link_tag else 'URL not found'

    # Now let's create a CSV file
    with open('job_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Job Title', 'Date Posted', 'Company Name', 'Job Location', 'Job URL'])
        # Write the data row
        writer.writerow([job_title, job_date_posted, company_hiring, job_location, url_job])

    print('CSV file has been written successfully.')
else:
    print(f'Failed to retrieve page with status code: {response.status_code}')
