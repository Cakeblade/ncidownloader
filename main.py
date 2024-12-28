import argparse
import time
import os
import pyperclip
import random
import requests
import sys
from concurrent import futures
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm


flag = True
download_path = os.getcwd() + '\\download\\'
naver_login_url = "https://nid.naver.com/nidlogin.login"


def make_env():
    try:
        print("id : ", end='')
        input_id = input()
        print("pw : ", end='')
        input_pw = input()

        with open(os.getcwd() + '\\.env', 'w') as file:
            file.write("NAVER_ID = '" + input_id + "'\n")
            file.write("NAVER_PW = '" + input_pw + "'")

    except:
        print("make_env")
        return


def paste(str):
    try:
        tmp = pyperclip.paste()
        pyperclip.copy(str)
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        time.sleep(random.randint(0, 2) + random.random())
        pyperclip.copy(tmp)
        
    except:
        print("paste")
        return


def login():
    try:
        driver.get(naver_login_url)
        time.sleep(1)

        id_input = driver.find_element(By.ID, 'id')
        id_input.click()
        paste(id)

        pw_input = driver.find_element(By.ID, 'pw')
        pw_input.click()
        paste(pw)

        driver.find_element(By.ID, 'log.login').click()

        time.sleep(2);
        pyperclip.copy('')
    
    except Exception:
        print("login")
        return


def get_image():
    try:
        global flag
        print("URL : ", end='')
        url = input()

        if 'exit' == url:
            flag = False
            return

        if 'cafe.naver.com/' not in url:
            print("Error")

        driver.get(url)

        driver.implicitly_wait(10)
        driver.switch_to.frame('cafe_main')
        imgs = driver.find_elements(By.CLASS_NAME, 'se-image-resource')

        img_url = []

        for img in imgs:
            iu = str(img.get_attribute('src'))
            if iu.endswith("?type=w1600"):
                img_url.append(iu.replace('?type=w1600', ''))

        return img_url

    except Exception:
        print("get_image")
        return
    
    

def download_image(url, path):
    try:
        global download_path
        filename = str(url).split('/')[-1]
        response = requests.get(url)
        if response.status_code == 200:
            with (open(download_path + path + "\\" + filename, 'wb')) as file:
                file.write(response.content)
        else:
            print("Error")
            print(response)
            
    except:
        print("download_image")
        return


def main():
    try:
        global flag

        imgs = get_image()
        if flag is False:
            return
        
        date = str(now.date()) + "-" + str(now.hour) + str(now.minute) + str(now.second)
        if not os.path.isdir(download_path + date + "\\"):
            os.mkdir(download_path + date + "\\");
        
        print("Download Start...")

        if not args.thread:
            # Download One by One
            for img in tqdm(imgs, desc='Downloaded Images', total=len(imgs)):
                download_image(img, date)
        
        else:
            executor_class = futures.ThreadPoolExecutor
            
            with executor_class(max_workers=os.cpu_count()) as executor:
                future_to_url = {executor.submit(download_image, img, date): img for img in imgs}
                for future in tqdm(futures.as_completed(future_to_url), desc='Downloaded Images', total=len(imgs)):
                    url = future_to_url[future]
                    try:
                        future.result()
                    except Exception as e:
                        print(f"Error downloading {url}: {str(e)}")

        print("Download Complete!")

        while True:
            print("Enter a URL for the new download? (y/n) ", end='')
            f = input()
            if f == 'y':
                return
            
            elif f == 'n':
                flag = False
                return
            
    except:
        print("main")
        flag = False
        return


if __name__ == '__main__':
    argv = sys.argv
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', help=' : Running debug mode', default=False)
    parser.add_argument('--headless', help=' : Running headless mode', default=True)
    parser.add_argument('--setenv', help=' : Setting .env', default=False)
    parser.add_argument('--thread', help=' : Using thread', default=True)
    args = parser.parse_args()

    if args.setenv:
        make_env()

    if not os.path.isfile(os.getcwd() + '\\.env'):
        print(".env not found. Making .env file...")
        make_env()

    load_dotenv()
    id = os.environ.get('NAVER_ID')
    pw = os.environ.get('NAVER_PW')

    if len(id) == 0 or len(pw) == 0:
        print("Id or Password is empty. Making .env file...")
        make_env()

    print("Starting...")

    if not os.path.isdir(os.getcwd() + "\\download"):
        os.mkdir(os.getcwd() + "\\download")

    options = Options()
    if not args.debug:
        options.add_argument('--log-level=1')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if args.headless:     
        options.add_argument('--headless=new')

    driver = webdriver.Chrome(options=options)
    login()

    flag = True
    while flag:
        now = datetime.now()
        main()

    print("Gracefull Exit...")
    driver.close()