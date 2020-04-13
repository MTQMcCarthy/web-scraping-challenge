# import all dependencies
# if __name__ == "__main__":
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import requests
#import request as req

def init_browser():
    executable_path = {'executable_path':'C:/bin/chromedriver.exe'} 
    browser = Browser('chrome', **executable_path, headless=False)

def scrape ():    
    browser = init_browser()
    mars_data = {}

    # visit the NASA Mars News site and scrape headlines
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    
    time.sleep(1)
    
    # scrape to soup
    browser_html = browser.html
    news_soup = bs(browser_html, "html.parser")
    
    # Get most recent headline

    news_list = nasa_soup.find('ul', class_='item_list')
    first_item = news_list.find('li', class_='slide')
    news_headline = first_item.find('div', class_='content_title').text
    news_teaser = first_item.find('div', class_='article_teaser_body').text
    mars_data["nasa_headline"] = news_headline
    mars_teaser["nasa_teaser"] = news_teaser

    # visit the JPL website and scrape the featured image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    try:
        expand = browser.find_by_css('a.fancybox-expand')
        expand.click()
        time.sleep(1)

        jpl_html = browser.html
        jpl_soup = bs(jpl_html, 'html.parser')

        img_relative = jpl_soup.find('img', class_='fancybox-image')['src']
        image_path = f'https://www.jpl.nasa.gov{img_relative}'
        mars_data["feature_image_src"] = image_path
    except ElementNotVisibleException:
        image_path = 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA01320_ip.jpg'
        mars_data["feature_image_src"] = image_path
        
    # visit the mars weather report twitter and scrape the latest tweet
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    time.sleep(1)
    mars_weather_html = browser.html
    mars_weather_soup = bs(mars_weather_html, 'html.parser')

    latest_tweet = mars_weather_soup.find('ol', class_='data-testid')
    #mars_weather = latest_tweet.find('p', class_='tweet').text
    print(mars_weather_url)

    # visit space facts and scrap the mars facts table
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    time.sleep(1)
    mars_facts_html = browser.html
    mars_facts_soup = bs(mars_facts_html, 'html.parser')

    fact_table = mars_facts_soup.find('table', class_='tablepress tablepress-id-p-mars')
    column1 = fact_table.find_all('td', class_='column-1')
    column2 = fact_table.find_all('td', class_='column-2')

    # I needed help with this-found an example online
    facets = []
    values = []

    for row in column1:
        facet = row.text.strip()
        facets.append(facet)

    for row in column2:
        value = row.text.strip()
        values.append(value)

    mars_facts = pd.DataFrame({
        "Facet":facets,
        "Value":values
        })

    mars_facts_html = mars_facts.to_html(header=False, index=False)
    mars_facts

    browser.quit()

    return mars_data