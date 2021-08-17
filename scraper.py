import requests
import substring
from bs4 import BeautifulSoup
import pymongo
from datetime import datetime
import sched, time
s = sched.scheduler(time.time, time.sleep)

funds_to_insert = []
funds = {}


def run_scraper(interval):
    """
    execute scraper every interval seconds.
    :param interval: example: {interval = 30} scrap function will be executed every 30 seconds.
    :return:
    """
    while True:
        scrap()
        time.sleep(interval)


def scrap():
    """
    This function is a wrapper:
     1.collects data from 6 different funds
     2.update data to the database.
    """
    get_fund_details(URL="https://www.healthwellfoundation.org/fund/acute-myeloid-leukemia-medicare-access/")
    get_fund_details(URL="https://www.healthwellfoundation.org/fund/adrenal-insufficiency/")
    get_fund_details(URL="https://www.healthwellfoundation.org/fund/amyotrophic-lateral-sclerosis/")
    get_fund_details(URL="https://www.healthwellfoundation.org/fund/amyloidosis/")
    get_fund_details(URL="https://www.healthwellfoundation.org/fund/asthma/")
    get_fund_details(URL="https://www.healthwellfoundation.org/fund/anemia-associated-with-chronic-renal-insufficiencyfailure/")
    print(funds)
    update_db()
    # s.enter(1, 1, scrap, (sc,))


def update_db():
    """
    This function connects to Atlas mongoDB and updates status and update time.
    """
    client = pymongo.MongoClient('mongodb+srv://dbUser:12345@cluster0.5iar3.mongodb.net/Funds')
    db = client.db.Funds
   # db.insert_many(funds_to_insert)
    try:
        for fund in funds:
            db.update_one({'fund_name': fund}, {"$set":{'status': funds[fund]["status"], 'last_update': funds[fund]["last_update"]}})
        print(f'updated {len(funds)} funds status data')
    except:
        print('an error occurred funds were not stored to db')
##### optional test ######
# add :
# if fund == "Asthma":
#     funds[fund]["status"] = "Open"
# on row 40


def get_fund_details(url):
    """
    this function parse data from the webpage related to the given url.
    :param url: url to connect to (page of the fund)
    :return: updated funds obj with the fund related to the given URL.
    """
    now = datetime.now()
    fund = dict()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    fund_name = soup.find(id="fund-intro").find("h1").text.strip()
    results = soup.find(id="fund-details")
    status = results.find("div", class_="row clearfix").text.strip().replace(" ", "")[6:12].strip()
    treatment_cover = results.find("div", class_="treatments").text.strip().splitlines()
    max_award = results.find("div", class_="details")
    max_award_value = substring.substringByChar(max_award.text, startChar="$", endChar=" ")
    fund['fund_name'] = fund_name
    fund['status'] = status
    fund['max_award'] = max_award_value
    fund['treatment_cover'] = treatment_cover
    fund['last_update'] = now.strftime("%m/%d/%Y, %H:%M:%S")
    funds[fund_name] = fund
    funds_to_insert.append(fund)


if __name__ == '__main__':
    run_scraper(3600)


