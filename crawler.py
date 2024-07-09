from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def fetch_posts(query, num_posts=10, output_file="output.json", by_hashtag=False):
    # Correct way to initialize ChromeDriver using ChromeDriverManager
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service)

    # Open Instagram hashtag or profile page
    if by_hashtag:
        driver.get(f"https://www.instagram.com/explore/tags/{query}/")
    else:
        driver.get(f"https://www.instagram.com/{query}/")
    
    time.sleep(3)  # wait for page to load

    # Scroll to load posts
    for _ in range(5):  # adjust range for more posts
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # wait for loading

    # Fetch posts
    posts = []
    post_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")[:num_posts]
    for post in post_elements:
        post_url = post.get_attribute("href")
        posts.append(post_url)

    # Fetch additional details for each post
    post_details = []
    for post_url in posts:
        driver.get(post_url)
        time.sleep(3)  # wait for page to load

        try:
            username_element = driver.find_element(By.XPATH, "//a[contains(@class, '_acan') and contains(@role, 'link')]")
            username = username_element.text
        except:
            username = "unknown"

        try:
            likes_element = driver.find_element(By.XPATH, "//article//section//span[contains(text(), ' likes')]/span")

            likes = int(likes_element.text.replace(',', ''))
        except:
            likes = 0
        
        

        post_details.append({
            "url": post_url,
            "username" : username,
            "likes": likes,
        })

    ranked_posts = sorted(post_details, key=lambda x: x['likes'], reverse=True)

    # Save posts to a JSON file
    with open(output_file, "w") as file:
        json.dump(ranked_posts, file, indent=4)

    driver.quit()
    print(f"Fetched {len(ranked_posts)} posts from {'#' if by_hashtag else '@'}{query} and saved to {output_file}")

if __name__ == "__main__":
   
    # fetch_posts("ai", num_posts=10, output_file="output_ai.json", by_hashtag=True)
    fetch_posts("web3", num_posts=10, output_file="output_web3.json", by_hashtag=True)
