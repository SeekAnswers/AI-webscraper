#This is where the scraping code is. Basically for easier navigation
#We would be importing Selenium modules and/or classes we need to use
#We would be creating a function that takes a website url and returns the content from the site

# Importing Necessary Modules
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
import time

# Setting Up WebDriver URL
SBR_WEBDRIVER = 'https://brd-customer-hl_2c88f0f3-zone-ai_scraper:wr3eaoi1r2rc@brd.superproxy.io:9515'

# Function to Scrape Website Content
def scrape_website(website):
    print('Launching chrome browser...')

# def main():
#     print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        # print('Connected! Navigating to https://example.com...')
        driver.get(website)
        # CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
        print('Waiting captcha to solve...')
        solve_res = driver.execute('executeCdpCommand', {
            'cmd': 'Captcha.waitForSolve',
            'params': {'detectTimeout': 10000},
        })
        print('Captcha solve status:', solve_res['value']['status'])
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html
    
# Function to Extract Body Content from HTML
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ''

# Function to Clean Extracted Body Content
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')

    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator='\n')
    cleaned_content = '\n'.join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

# Function to Split DOM Content into Chunks
def split_dom_content(dom_content, max_length=6000):
    return[
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
        ]


# if __name__ == '__main__':
#     main()
