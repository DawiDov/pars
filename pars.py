from driver.chromedriver import driver


class Reverb():
    def create_link(self, category):
        #создание ссылки
        search_category = '+'.join(category.split())
        url = ('https://reverb.com/news?category_name=') + f'{search_category}'

        new_url = url + '&page='
        return new_url

    def pars_posts(self, input):
        #обработка полученного списка постов
        post_list = []
        page = 1
        while True:
            try:
                driver.implicitly_wait(4)
                driver.get(self.create_link(input) + str(page))
                page += 1
                driver.implicitly_wait(4)
                tiles = driver.find_element_by_class_name('tiles')
                print('Parsing...')
                if tiles.text:
                    post_list.append(tiles.text)
                    print(f'Page: {page}')
                else:
                    for post in post_list:
                        print(post)
                        print('____________')
                    print('done')
                    break
            except Exception as ex:
                print(ex)
                break


reverb = Reverb()
if __name__ == "__main__":
    reverb.pars_posts("Gear History")