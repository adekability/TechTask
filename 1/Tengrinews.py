from selenium import webdriver
import re, datetime, json

json_format = dict()
verify = False
driver = webdriver.Chrome()
driver.get("https://tengrinews.kz/news")
el = driver.find_elements_by_class_name("tn-article-item")
links = []
for i in el:
    elems = driver.find_elements_by_css_selector(".tn-article-grid [href]")
    links = [elem.get_attribute("href") for elem in elems]
    break
ids = [i.split("-")[len(i.split("-"))-1].replace("/","") for i in links]

def get_title():
    for title in driver.find_elements_by_xpath('.//h1[@class = "tn-content-title"]'):
        return title.text


def get_publish_date():
    adate = driver.find_element_by_xpath('.//div[@class = "tn-content"]')
    dates = adate.find_element_by_xpath('.//ul[@class = "tn-data-list"]')
    date_text = dates.text.split(", ")
    if date_text[1].__contains__("\n"):
        date_text[1] = date_text[1][:-5]
    # TODAY
    if date_text[0] == "сегодня":
        return str(datetime.datetime.today())[:10] + " " + date_text[1]
    # YESTERDAY
    elif date_text[0] == "вчера":
        return str(datetime.datetime.today() - datetime.timedelta(days=1)) + " " + date_text[1]


def get_comments():
    for i in range(len(links)):
        dictionary = dict()
        people, messages, times = [], [], []
        driver.get(links[i])
        driver.implicitly_wait(10)

        for elem in driver.find_elements_by_xpath('.//span[@class = "tn-user-name"]'):
            people.append(elem.get_attribute("innerHTML"))
            if len(people)==100:
                verify = True
                break
        for elem in driver.find_elements_by_xpath('.//div[@class = "tn-comment-item-content-text"]'):
            messages.append(str(elem.get_attribute("innerHTML")).replace("<p>","").replace("</p>",""))
            if len(messages)==100:
                break
        for elem in driver.find_elements_by_tag_name('time'):
            timeis = str(elem.get_attribute("innerHTML"))
            timeis2 = timeis.split(", ")
            if re.search('[а-яА-Я]', timeis2[0]) is None:
                times.append(timeis)
            if len(times) == 100:
                break
        for y in range(len(people)):
            dictionary[i+1] = [people[y], messages[y], times[y]]
        json_format[get_title()] = [{"date":get_publish_date()},{"Комментарии":dictionary}]
        print(json_format)
    return json_format


with open('result.json', 'w',encoding="utf-8") as fp:
    json.dump(get_comments(), fp, ensure_ascii=False)
driver.close()