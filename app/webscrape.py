import json
from parsel import Selector
from playwright.sync_api import sync_playwright
import time

script = """
function waitCss(selector, n=1, require=false, timeout=5000) {
  console.log(selector, n, require, timeout);
  var start = Date.now();
  while (Date.now() - start < timeout){
  	if (document.querySelectorAll(selector).length >= n){
      return document.querySelectorAll(selector);
    }
  }
  if (require){
      throw new Error(`selector "${selector}" timed out in ${Date.now() - start} ms`);
  } else {
      return document.querySelectorAll(selector);
  }
}

var results = waitCss("div[role*=article]>a", n=10, require=false);
return Array.from(results).map((el) => el.getAttribute("href"))
"""


def search(query, page):
    url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}/?hl=en"
    page.goto(url)
    urls = page.evaluate("() => {" + script + "}")
    return urls or [url]

def parse_place(selector):
    """parse Google Maps place"""

    def aria_with_label(label):
        """gets aria element as is"""
        return selector.css(f"*[aria-label*='{label}']::attr(aria-label)")

    def aria_no_label(label):
        """gets aria element as text with label stripped off"""
        text = aria_with_label(label).get("")
        return text.split(label, 1)[1].strip()

    result = {
        "name": "".join(selector.css("h1 ::text").getall()).strip(),
        "category": selector.css("button[jsaction='pane.rating.category']::text").get(),
        "address": aria_no_label("Address: "),
        "website": aria_no_label("Website: "),
        "phone": aria_no_label("Phone: "),
    }
    return result

def parse_reviews(selector):
    """parse Google Maps reviews"""

    def aria_with_label(label):
        """gets aria element as is"""
        return selector.css(f"*[aria-label*='{label}']::attr(aria-label)")

    def aria_no_label(label):
        """gets aria element as text with label stripped off"""
        text = aria_with_label(label).get("")
        return text.split(label, 1)[1].strip()

    result = {
        "review": clean(selector.css('.wiI7pd::text').getall()),
    }
    return result

def clean(test):
    cleaned_1 = []
    cleaned_2 = []
    cleaned_3 = []
    for review in test:
        cleaned_1.append(review.replace("/n", ""))
    for review in cleaned_1:
        cleaned_2.append(review.replace("\\n", " "))
    for review in cleaned_2:
        cleaned_3.append(review.replace("\n", " "))
    return cleaned_3

    
urls = ["https://www.google.com/maps/place/Encik+Tan/@1.356499,103.8461772,11z/data=!4m10!1m2!2m1!1sEncik+Tan!3m6!1s0x31da3d12670e2fd1:0x99e1c1951d45340a!8m2!3d1.3529604!4d103.9403451!15sCglFbmNpayBUYW4iA4gBAVoLIgllbmNpayB0YW6SARBoYWxhbF9yZXN0YXVyYW504AEA!16s%2Fg%2F11dxlg38fy",
    "https://www.google.com/maps/place/Buddy+Hoagies+Caf%C3%A9+%26+Grill/@1.3424411,103.9510012,17z/data=!3m1!4b1!4m5!3m4!1s0x31da3d3cd376ea91:0x382039825a06483d!8m2!3d1.3424411!4d103.9531845",
    "https://www.google.com/maps/place/Spize+@+Bedok/@1.3313414,103.9457261,17z/data=!3m1!4b1!4m5!3m4!1s0x31da3d31eda46eb3:0xec1c90d65bc5e8de!8m2!3d1.3313414!4d103.9479094",
    "https://www.google.com/maps/place/The+Tipsy+Cow+@+Katong/@1.3060298,103.8939135,17z/data=!3m1!4b1!4m5!3m4!1s0x31da186b6eeccb17:0xb3ef6f5cdf2507f6!8m2!3d1.3060199!4d103.8960717",
    "https://www.google.com/maps/place/Starbucks/@1.3060298,103.8960968,15z/data=!3m1!5s0x31da1871a40e3bad:0xe35907eccab30f20!4m10!1m2!2m1!1sstarbucks!3m6!1s0x31da18719a1765d9:0xbd6a9159dd45236f!8m2!3d1.3020241!4d103.905097!15sCglzdGFyYnVja3MiA4gBAVoLIglzdGFyYnVja3OSAQRjYWZl4AEA!16s%2Fg%2F1thr4ppm"]
places = []

def main():
    output = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for url in urls:
            page.goto(url)
            page.wait_for_selector("button[jsaction='pane.rating.category']")
            result = parse_place(Selector(text=page.content()))

        
            #locates more reviews button and clicks it
            page.wait_for_selector('button[jsaction="pane.reviewChart.moreReviews"]')
            more_reviews_button = page.locator('button[jsaction="pane.reviewChart.moreReviews"]')
            more_reviews_button.click()
        

            total_reviews_on_page = page.locator("span[class='wiI7pd']").count()

            view_more = page.locator('button[jsaction="pane.review.expandReview"]').count()
            for l in range(view_more):
                page.wait_for_selector('button[jsaction="pane.review.expandReview"]')
                page.locator('button[jsaction="pane.review.expandReview"]').first.click()
                l+=1

            while True:
                page.mouse.wheel(0, 15000)
                time.sleep(2) 

                #locates expand review button and clicks
                view_more = page.locator('button[jsaction="pane.review.expandReview"]').count()
                for l in range(view_more):
                    page.wait_for_selector('button[jsaction="pane.review.expandReview"]')
                    page.locator('button[jsaction="pane.review.expandReview"]').first.click()
                    l+=1               
            
                total_reviews_on_page = page.locator("span[class='wiI7pd']").count()

                if (total_reviews_on_page < 10):
                    continue  # more items loaded - keep scrolling
                else:
                    break  # no more items - break scrolling loop

            #time.sleep(2)
            result.update(parse_reviews(Selector(text=page.content())))
            places.append(result)
        
        json_1= json.dumps(places, indent=0, ensure_ascii=False)
        json_cleaned = json.loads(json_1.replace("\n", " "))
        output.append(json_cleaned)
        
        return output
