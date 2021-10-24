def LocalizeObject(image):
    img = image
    h, w, channels = img.shape
    part = h // 3
    local = ['Up', 'Middle', 'Down']
    C_array = []
    for i in range(1, 4, 1):
        _, C = topN_colors(img[(part*(i-1)+1):(part*i - 1)], 1)
        C_array.append(C[0])
    
    # Локализация обуви
    print(local[np.argmin(C_array)])
    h, w, channels = image.shape
    if (np.max(C_array)//np.min(C_array) == 1): # Если фон немонотонный
        return
    if local[np.argmin(C_array)] == 'Up':
        return image[:w]
    elif local[np.argmin(C_array)] == 'Down':
        return image[(h-w):]
    elif local[np.argmin(C_array)] == 'Middle':
        return image[((h - w)//2):-((h - w) - (h-w)//2)]



# Функция для нахождение популярных цветов
def topN_colors(img, N = 1, flag = False):
    """
        N - количество самых популярных цветов на изображении
    """
    img = img.astype(np.uint8)
    unqc,C = np.unique(img.reshape(-1,img.shape[-1]), axis=0, return_counts=True)
    topNidx = np.argpartition(C,-N)[-N:]
    
    if flag: return unqc, C
    return unqc[topNidx], C[topNidx]


# Прокручивание сайта
def ScrollDocument(driver, path_kedy = 'D:\MyProjects\KedyKrossy\kedy'):
    SCROLL_PAUSE_TIME = 0.2

    last_height = driver.execute_script("return document.body.scrollHeight")
    new_height = 0
    
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
        new_height += 200

        time.sleep(SCROLL_PAUSE_TIME)

        if new_height >= last_height:
            break

def LoadKrossy(url_base, subject, count_in_catalog):
    """
        subject - номер типа вещи
        url_base - url сайта с каталогом товара
    """
    
    count = 4100
    k = 41
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        
    while True:
        url = url_base + 'page=' + str(k) + '&xsubject=' + str(subject)

        driver.get(url)
        ScrollDocument(driver)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source)

        shoes = soup.find_all('div', class_ = 'product-card j-card-item')
        print(len(shoes))
        if len(shoes) < count_in_catalog: break
        for s in shoes:
            img_url = s.find('img').get('src')
            if not('https' in img_url): img_url = 'https:' + img_url
            print(img_url, '\n')
            
            response = requests.get(img_url, timeout=5)
            img = Image.open(BytesIO(response.content))
            img = np.array(img)

            img = LocalizeObject(img)
            if type(img) != type(None):
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                cv2.imwrite(path_krossy+'\\' + str(count) + '.png', img)
                count += 1
                if count == 461: break
                print('count = ', count)
                
        
        k+=1
    
    
    driver.quit()
