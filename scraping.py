# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deplaoyment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, new_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary 
    data = {
         "news_title": news_title,
         "news_paragraph": news_paragraph,
         "featured_image": featured_image,
         "facts": mars_facts(),
         "last_modified": dt.datetime.now()
         }

# Scrape Mars News
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # OPtional delay for loading page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p


    # Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_title


    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    news_p


# ### Featured Images
def featured_image(browser):

# Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for erro handling
    try: 
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src') 
    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
    # USe 'read_html to scrape the facts table into the dataframe    
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index to dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()
    
    # Stop webdriver and return data
    browser.quit()

    return data
