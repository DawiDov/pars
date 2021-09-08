from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options


class Reverb():

    chrome_options = Options()
    chrome_options.headless = True
    #что бы не открывало бразуер
    driver = wd.Chrome(
        executable_path=
        "/Users/arturdavidov/Documents/work/selenium/chromedriver/chromedriver",
        options=chrome_options)

    def category_select(self, category):
        #выбор категории в новостях
        search_category = '+'.join(category.split())
        self.url = (
            'https://reverb.com/news?category_name=') + f'{search_category}'
        Reverb.driver.get(url=self.url)
        return self.url

    def pagination(self, url):
        #делает ссылку для перелистывания на след. страницу
        print(self.url)
        self.new_url = self.url + '&page='
        return self.new_url

    def post(self, input):
        #парсинг
        self.url = self.category_select(input)
        new_url = self.pagination(self.url)
        Reverb.driver.implicitly_wait(5)
        title = Reverb.driver.find_element_by_class_name('tiles')
        page = 2
        while True:
            try:
                Reverb.driver.get(new_url + str(page))
                page += 1
                Reverb.driver.implicitly_wait(4)
                print('_________NEXT PAGE_________')
                title = Reverb.driver.find_element_by_class_name('tiles')
                print(title.text)
                if title.text:
                    print(title.text)
                else:
                    print('done')
                    break
            except:
                break


r = Reverb()
r.post("Gear History")