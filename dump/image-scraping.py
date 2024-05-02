import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
service = Service(executable_path=ChromeDriverManager().install())
wd = webdriver.Chrome(service=service, options=options)

curly_hairs_url = "https://www.google.com/search?sca_esv=421bbcb432c7b64f&sxsrf=ACQVn08LVp_e-Cn1bzHBzE0k4peylYOLxQ:1713093490593&q=curly+hair&uds=AMwkrPvxSHE1JOQc6Rm4P_TBX_BldwBdIq0z6GyHw4DDiz04zGPReCmxGDzuSLajdtd9kC5AsDydgAW_KmE7zFXKbW1RjDtXLZ9XeaI6N-o0MB_b16u8231TwatOiM54lV-Z4Zz2hzEswu3vwSoLhOryEAYSlmQOuWVdtkR7Ri976NUyBHW51kJsF8f1DTYjSWgP3K8WC8VxFRaiSpYHlyFBdDmSqGcU8_SKiLM6lv5tm8MSOxxAOdU4LLBCmoO4l17xpYSD5Ut322F_RiXJ2wsBLglDFrDuEBSn1tUqTkOTyKfByO8NQ6c&udm=2&prmd=isvnmbtz&sa=X&ved=2ahUKEwjg6eTHysGFAxX_TGwGHZNuCiIQtKgLegQIEBAB&biw=1150&bih=943&dpr=1"
curly_hairs_thumbnail_class = "YQ4gaf"
curly_hairs_img_class = "sFlh5c pT0Scc iPVvYb"

straight_hairs_url = "https://www.google.com/search?q=straight+hair&sca_esv=421bbcb432c7b64f&udm=2&biw=1150&bih=943&sxsrf=ACQVn0_TcXZ5b4AJl3ltwaD-rNqFP8LHLg%3A1713093611692&ei=67sbZq35KezXseMP3oir6AU&ved=0ahUKEwjtmsSBy8GFAxXsa2wGHV7ECl0Q4dUDCBA&uact=5&oq=straight+hair&gs_lp=Egxnd3Mtd2l6LXNlcnAiDXN0cmFpZ2h0IGhhaXIyBBAjGCcyCBAAGIAEGLEDMgUQABiABDIIEAAYgAQYsQMyBRAAGIAEMgsQABiABBixAxiDATIFEAAYgAQyBBAAGAMyBRAAGIAEMggQABiABBixA0iPDVAAWNoJcAB4AJABAJgBWaABsgeqAQIxM7gBA8gBAPgBAZgCDaAC8AfCAgoQABiABBiKBRhDmAMAkgcCMTOgB-lT&sclient=gws-wiz-serp"
straight_hairs_thumbnail_class = "YQ4gaf"
straight_hairs_img_class = "sFlh5c pT0Scc iPVvYb"

wavy_hairs_url = "https://www.google.com/search?sca_esv=421bbcb432c7b64f&sxsrf=ACQVn08GCLo7L8CrWEu6bvnaHmpMQVt8RA:1713093610293&q=wavy+hair&uds=AMwkrPs_hVtukA3OtiDLQGFhPeVLQHFVKsLZI6FFN0p1Xm-FBhUN7Qyz9Ab_96Ow-Y_PMmEPEdjRbu8htJY14pHQBJMy0O9Ff12oxfNWpDKjItwjPW2hx-vu9ziX67P-oOyVpD6F1rZLJ_KRH2bpE6PsmHtl10D07hLR5qBUuinvmJMGA01PFlvSeKfiLcxlf9oy9aPbNkn2lu8XSza-wAA7m8TV6u3mweVKLQ3-0u-9wWPpN-gbyb6W0KhyNUHSSQz9Dnf08hCsK5F6UtD0oqdZlZ6VtI3UhzjXfVsID072a0MFS5orsbg&udm=2&prmd=isvnmbtz&sa=X&ved=2ahUKEwjC4u6Ay8GFAxUrRmwGHcuPAD0QtKgLegQIERAB&biw=1150&bih=943&dpr=1"
wavy_hairs_thumbnail_class = "YQ4gaf"
wavy_hairs_img_class = "sFlh5c pT0Scc iPVvYb"

def scroll_down(wd):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

def get_images_from_google(wd, delay, max_images, hair_url, thumbnail_class, img_class):
    wd.get(hair_url)
    image_urls = set()
    thumbnails_checked = set()  # Keep track of checked thumbnails

    try:
        while len(image_urls) < max_images:
            thumbnails = wd.find_elements(By.CLASS_NAME, thumbnail_class)
            for img in thumbnails:
                img_id = img.get_attribute('id')
                if img_id in thumbnails_checked:
                    continue  # Skip thumbnails already checked
                
                try:
                    img.click()
                    time.sleep(delay)
                    thumbnails_checked.add(img_id)  # Mark this thumbnail as checked
                except Exception as e:
                    print(f"Failed to click thumbnail")
                    continue
                
                images = wd.find_elements(By.CLASS_NAME, img_class)
                for image in images:
                    src = image.get_attribute('src')
                    if src and 'http' in src and src not in image_urls:
                        image_urls.add(src)
                        print(f"Found {len(image_urls)} unique images")
                        if len(image_urls) >= max_images:
                            return image_urls
                scroll_down(wd)  # Scroll down after processing thumbnails
            
            print("No new thumbnails found, end of page reached.")
            break

    except Exception as e:
        print(f"An error occurred:")
                    
    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content 
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name
        
        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
            
        print("Success")
    except Exception as e:
        print("FAILED - ", e)
    

straight_hair_urls = get_images_from_google(wd=wd, delay=5, max_images=10, hair_url=straight_hairs_url, thumbnail_class=straight_hairs_thumbnail_class, img_class=straight_hairs_img_class)

for i, url in enumerate(straight_hair_urls):
    download_image("images/Straight_Hair", url, str(i) + ".jpg")

wd.quit()