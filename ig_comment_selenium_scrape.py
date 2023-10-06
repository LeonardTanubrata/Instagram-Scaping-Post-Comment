# %%
# Import required modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException,NoSuchElementException
from IPython.display import display
import pandas as pd
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import pandas as pd
import time
import openpyxl
#%%
driver = webdriver.Chrome()
driver.get("https://www.instagram.com/accounts/login/")

# Input instagram username and password
username = "kemang.ol"
password = "kemangOlrange@999"

# Input instagram post id. Post id is 11 unique code for every instagram link
# If you want to mined more than one content, then seperate the post id using comma     
post_id = ['CxSSmOUry2W']
                
scroll_count = 10 # You can adjust the number of scrolls as needed.

time.sleep(5)

# Find the username and password elements on the login page, then fill them with your username and password
username_field = driver.find_element(by=By.NAME, value="username")
password_field = driver.find_element(by=By.NAME, value="password")
username_field.send_keys(username)
password_field.send_keys(password)

login_button = driver.find_element(by=By.XPATH, value="//button[@type='submit']")
login_button.click()

time.sleep(5)

df_result = pd.DataFrame()

for post in post_id :
    # Enter the link of the Instagram post you want to scrap
    post_link = f"https://www.instagram.com/p/{post}"
    print(f'Post extracted: {post_link}')

    # Open post link
    driver.get(post_link)

    time.sleep(2)
    # print("the page is scrolling down!")

    # Wait for the comment section element to be visible.
    try:
        comment_section_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='x5yr21d xw2csxc x1odjw0f x1n2onr6']"))
            )
        
        # UnComment this code if you want to put how many scroll

        for _ in range(scroll_count):  
                try :
                    driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", comment_section_element)
                    time.sleep(0.5)
                except :
                     break

        # previous_height = driver.execute_script("return arguments[0].scrollHeight", comment_section_element)
        # print('Scrolling Begin')
        # while True:
        #   driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", comment_section_element)
        #   time.sleep(2.5)
        #   new_height = driver.execute_script("return arguments[0].scrollHeight", comment_section_element)
        #   if new_height == previous_height:
        #        break
        #   previous_height = new_height
        print('Finish Scrolling Go to Next Step')        

        # Wait until the page is completely loaded
        time.sleep(2)

        # Initialize the data list before the loop.
        data = []

        comments = driver.find_elements(By.XPATH, "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']")
    
        for index,comment in enumerate(comments):
            try:
                # Find the username element.
                username_element = comment.find_element(By.XPATH, ".//span[@class='_aacl _aaco _aacw _aacx _aad7 _aade']")
                # username_element = comment.find_element(By.XPATH, ".//span[@class='_aacl _aaco _aacw _aacx _aad7 _aade']//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1")
                username = username_element.get_attribute("textContent").strip()
                print(username)

                # Find the comment text element.
                comment_text_element = comment.find_element(By.XPATH, ".//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1']")
                comment_text = comment_text_element.text.strip()
                print(comment_text)

                # Find the date element and extract the 'title' attribute.
                # date_element = comment.find_element(By.XPATH, """.//time[@class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a9zg _a6hd']""")
                date_element = comment.find_element("xpath", """.//time[@class='x1ejq31n xd10rxx x1sy0etr x17r0tee x1roi4f4 xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6']""")  
                date = date_element.get_attribute("title")
                print(date)

                # Append the extracted data to the list.
                data.append({'Username': username, 'Comment': comment_text, 'Comment_Date' : date})
                # data.append({ 'Comment': comment_text, 'Comment_Date' : date})
            except:
                print('')
        print('Got The Data')
            

        # Create the DataFrame after processing all comments.
        df = pd.DataFrame(data)
        df['Comment_Date'] = pd.to_datetime(df['Comment_Date'])
        df['Post_URL'] = f"https://www.instagram.com/p/{post}"
        df_result = pd.concat([df_result, df], ignore_index=True)

        print('go to the next post!')
        time.sleep(10)
    except Exception as e :
         print(e)

# Display dataframe
display(df_result)

# %%
# Save to CSV File
df_result.to_csv('april.csv', index=False)
# %%
