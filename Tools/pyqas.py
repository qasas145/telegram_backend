def Remove_Duplicates(lst) :
    lst_no_duplicates=[]
    for el in lst:
        if el not in lst_no_duplicates :
            lst_no_duplicates.append(el)
    return lst_no_duplicates
def Reverse_Lst(lst) :
    lst_reversed=[]
    for el in range(1,  len(lst)+1) :
        lst_reversed.append(lst[-el])
    return lst_reversed
def Get_Counts(list, el) :
    list_counts=[]
    for item in list:
        if item==el :
            list_counts.append(item)
    return len(list_counts)
def Order_Nums(list) :
    list_orderd=[]
    boolean_list=[]
    for num in list :
        if len(list_orderd)==1 :
            if num>=list_orderd[0] :
                list_orderd.append(num)
                list_orderd=Reverse_Lst(list_orderd)
            else :
                list_orderd.append(num)
                
        elif len(list_orderd) > 1 :
            boolean_list.clear()
            for i in range(0, len(list_orderd)) :
                if num >= list_orderd[i] :
                    boolean_list.append(True)
                else :
                    boolean_list.append(False)
            counts_False=Get_Counts(boolean_list, False)
            counts_True=Get_Counts(boolean_list, True)
            if counts_False==0 :
                list_orderd.append(num)
                for i in range(1, len(list_orderd)) :
                    list_orderd[-i]=list_orderd[-i-1]
                list_orderd[0]=num
            if counts_True==0 :
                list_orderd.append(num)
            if counts_False==len(list_orderd)-1 and counts_True==1:
                list_orderd.append(num)
                list_orderd[-1]=list_orderd[-2]
                list_orderd[-2]=num
            if counts_False!=0 and counts_True!=0 and  counts_False!=len(list_orderd)-1 and counts_True!=1:
                list_orderd.append(num)
                for i in range(1, counts_True+1) :
                    list_orderd[-i]=list_orderd[-i-1]
                list_orderd[counts_False]=num
        else :
            list_orderd.append(num)
    return list_orderd
def Max_Value(lst) :
    ordered_nums=order_nums(lst)
    return ordered_nums[0]
def Remove_word(text, word) :
    text_words=text.split()
    str_after="".join(f'{wrd} ' for wrd in text_words if wrd!=word)
    return str_after
def Replace_word(text, word, new_word) :
    text_words=text.split()
    str_after=""
    for item in text_words:
        if item==word :
            str_after="".join(new_word)
            lst.append(str_after)
        else :
            
            str_after="".join(item)
            lst.append(str_after)
    nw_str="".join(f'{i} ' for i in lst)
    return nw_str
def Paste_text() :
    import pandas as pd
    copied_data = pd.read_clipboard() 
    return(copied_data.columns[0])
    # or 
    # import clipboard
    # text = clipboard.paste()
    # print(text)
# download sound from sound cloud 
def download_sound_from_sound_cloud() :
    import time
    from pyqas import Remove_word
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    driver.get("https://www.soundcloudme.com/")
    links_list=[]
    with open('snd_cld_lnks.txt', 'r') as line :
        line_txt=line.readlines()
        links_list=line_txt
    url=driver.find_element_by_name("url")
    form_download=driver.find_element_by_id("soundcloud_form")
    for i in range(151, len(links_list)+1) :
        url=driver.find_element_by_name("url")
        form_download=driver.find_element_by_id("soundcloud_form")
        url.clear()
        nw_lnk=Remove_word(links_list[i], '\n')
        url.send_keys(nw_lnk)
        form_download.submit()
        time.sleep(2)
        btn=driver.find_element_by_class_name('btn.single-download')
        btn.click()
        driver.get("https://www.soundcloudme.com/")
        time.sleep(5)
        print('the first link is being downloaded')
# get the links of the sounds from the sound_cloud
def get_links_of_the_sounds_from_sound_cloud(user_name) :
    import clipboard
    import time
    from pyqas import Remove_word
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    # first clear the file of the links if it was found or create it if not found
    with open('snd_cld_lnks.txt', 'w') :
        pass
    # end of that 
    driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    driver.implicitly_wait(10)
    driver.get(f"https://soundcloud.com/{user_name}/likes")
    accept_btn=driver.find_element_by_id("onetrust-accept-btn-handler")
    accept_btn.click()
    time.sleep(1)
    driver.implicitly_wait(10)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True
    driver.implicitly_wait(20)
    time.sleep(2)
    likes_tracks=driver.find_elements_by_class_name('soundList__item')
    for i in range(1, len(liked_tracks)+1) :
        driver.implicitly_wait(20)
        time.sleep(3)
        more_btn=driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/ul/li[{i}]/div/div/div/div[2]/div[4]/div[1]/div/div/button[4]')
        driver.implicitly_wait(20)
        time.sleep(3)
        more_btn.click()
        driver.implicitly_wait(20)
        time.sleep(1)
        copy_btn=driver.find_element_by_class_name("sc-button-copylink")
        copy_btn.click()
        time.sleep(1)
        lst=[]
        text = clipboard.paste()
        lst.clear()
        lst.append(text)
        lst.append('\n')
        lnk_mod="".join(item for item in lst)
        with open('snd_cld_lnks.txt', 'a') as line:
            line.write(lnk_mod)
    driver.close()