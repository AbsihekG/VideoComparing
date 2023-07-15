import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import random
import pytest

@pytest.fixture
def driver():
    # Set Chrome options with headless false and a timeout of 10 seconds
    chrome_options = Options()
    chrome_options.headless = False
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--window-size=1600,1200')
    chrome_options.add_argument('--use-fake-ui-for-media-stream')
    chrome_options.add_argument('--use-fake-device-for-media-stream')
    chrome_options.add_argument('--use-file-for-fake-video-capture=/Users/digitalsupplier/videoy4m.y4m')
    prefs = {"profile.default_content_setting_values.notifications": 1}
    chrome_options.add_experimental_option("prefs", prefs)
    # Start the webdriver with the Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    # Set the timeout for the webdriver to 30 seconds
    driver.set_page_load_timeout(500000)
    yield driver
    # Quit the webdriver
    driver.quit()

def test_video_comparison(driver):
    # Navigate to the webpage
    driver.get('https://www.hippovideo.io/video-templates/record/744531/one_card_video_flow_001?api_key=5EY0i8mD46BMmohMPWiNRgtt&email=deepa%2Btestingtemplatebuilder%40hippovideo.io')
    print("!!!!!!!!!!!!!!!!!!")
    wait = WebDriverWait(driver, 800)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='vfSlide-1']//div[@class='vf-card-list__card']/img[@alt='Camera Only']")))
    #time.sleep(5)
    firstcardWebcamRecord = driver.find_element(By.XPATH,"//div[@id='vfSlide-1']//div[@class='vf-card-list__card']/img[@alt='Camera Only']") 
    firstcardWebcamRecord.click()
    print("@@@@@@@@@@@@@@@@@@")
    time.sleep(10)

    mirror_video_btn = driver.find_element(By.XPATH, "//span[text()='Mirror Video']")
    #mirror_video_btn.click()
    print('mirror webcam applied')
    time.sleep(3)

    startrecordingbtn = driver.find_element(By.XPATH, '//*[@id="hvRecorderSdkContainer"]/div[1]/div[3]/div[2]/div[2]/div/div')
    startrecordingbtn.click()
    print("######################")
    time.sleep(13)
    stoprecordingbtn = driver.find_element(By.XPATH, '//*[@id="hvRecorderSdkContainer"]/div/div[2]/div[2]/div[2]/div/div[1]')
    stoprecordingbtn.click()
    print("recordingstopped")
    time.sleep(15)
    firstcardvideopreview = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='videoPreviewSdk-1']//div[@id='preview-video']")))
    print("preview Loaded sucessfully")

    vbg_apply = wait.until_not(EC.presence_of_element_located((By.XPATH, "//div[@class='video-player-footer__right']/div[1]/span")))
    print("vbg applied")
    time.sleep(20)
    previewvideosrc = driver.find_element(By.XPATH, "//video[@id='primary-video']")
    previewvideourl  = previewvideosrc.get_attribute("src")

    print('Preview src = ' + previewvideourl)
    print("preview video src getted")

    #getting preview video path 
    asset_folder_path = os.path.abspath('/Users/digitalsupplier/VideoComparingTest')
    subfolder = 'Asset'  
    video_filename = 'vbgvideoflow.mp4'  
    video_file_path = os.path.join(asset_folder_path, subfolder, video_filename)

    video1 = cv2.VideoCapture(video_file_path)
    print('original video getted')

    #while True:
    ret1, frame1 = video1.read()
    print('video one readed')
    ret2, frame2 = cv2.VideoCapture(previewvideourl).read()
    print('video two captured and readed')

    #if not ret1 or not ret2:
        #break
    # resize the frames to the same size
    frame1 = cv2.resize(frame1, (640, 480))
    frame2 = cv2.resize(frame2, (640, 480))
    difference = cv2.subtract(frame1, frame2)
    result = np.any(difference)
    non_zero_pixels = np.count_nonzero(difference)
    total_pixels = difference.shape[0] * difference.shape[1] * difference.shape[2]
    difference_percentage = (non_zero_pixels / total_pixels) * 100
    print("Difference Percentage:", difference_percentage)
    cv2.imshow("Frame Difference", difference)
    cv2.waitKey(10)
    # Press 'Esc' to exit
    if difference_percentage == 0.0:
        print("both videos are same")

    else:
        print("preview is different")
        raise AssertionError("video is different")

    save_and_nextbtn = driver.find_element(By.XPATH, "//div[@class='vf-slide-bottom__options']//button")
    save_and_nextbtn.click()

    progressbar = wait.until_not(EC.presence_of_element_located((By.XPATH, "//div[@class='progress-section']")))

    VideoName_text_area = driver.find_element(By.XPATH, "//input[@name='video_name']")
    VideoName_text_area.click()
    VideoName_text_area.send_keys("video flow video with vbg")
    VideoName_text_area.click()
    random_numbers = random.sample(range(10), 2)  # Generate two unique random numbers from 0 to 9
    number_string = ''.join(str(number) for number in random_numbers)  # Concatenate the numbers without a space
    VideoName_text_area.send_keys(number_string)

    videoflow_video_tile = VideoName_text_area.get_attribute("value")
    print(videoflow_video_tile)

    save_nextbtn = driver.find_element(By.XPATH, "//div[@class='sidebar-inner__footer']//button")
    save_nextbtn.click()

    wait.until(EC.presence_of_element_located((By.ID, "footerSettingsSaveText")))
    salespage_save_and_next_btn = driver.find_element(By.ID, "footerSettingsSaveText")
    salespage_save_and_next_btn.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='table_action_icon previewIcon']")))
    sharesPreviewbtn = driver.find_element(By.XPATH, "//a[@class='table_action_icon previewIcon']")
    sharesPreviewbtn.click()
    driver.switch_to.window(driver.window_handles[1])

    #getting delivery video path 
    asset_folder_path = os.path.abspath('/Users/digitalsupplier/VideoComparingTest')
    subfolder = 'Asset'  
    video_filename = 'videoflowvideowithvbg.mp4'  
    delivery_video_file_path = os.path.join(asset_folder_path, subfolder, video_filename)
    video4 = cv2.VideoCapture(delivery_video_file_path)

    wait.until(EC.presence_of_element_located((By.XPATH, "//video[@id='preview-video-player']")))

    deliveryvideosrc = driver.find_element(By.XPATH, "//video[@id='preview-video-player']")
    deliveryvideourl  = deliveryvideosrc.get_attribute("src")
    print('delivery src = ' + deliveryvideourl)
    print("delivery video src getted")

    ret3, frame3 = cv2.VideoCapture(deliveryvideourl).read()
    ret4, frame4 = video4.read() 

    print('video two captured and readed')

    #if not ret1 or not ret2:
        #break
    # resize the frames to the same size
    frame4 = cv2.resize(frame4, (640, 480))
    frame3 = cv2.resize(frame3, (640, 480))
    deliveryVideoDifference = cv2.subtract(frame4, frame3)
    result = np.any(deliveryVideoDifference)
    non_zero_pixels = np.count_nonzero(deliveryVideoDifference)
    total_pixels = deliveryVideoDifference.shape[0] * deliveryVideoDifference.shape[1] * deliveryVideoDifference.shape[2]
    difference_percentage = (non_zero_pixels / total_pixels) * 100
    print("Difference Percentage:", difference_percentage)
    cv2.imshow("Frame Difference", deliveryVideoDifference)
    cv2.waitKey(25)
    # Press 'Esc' to exit
    if difference_percentage == 0.0:
        print("both videos are same")
    else:
        print("videos are different")
        raise AssertionError("delivery video is different")
