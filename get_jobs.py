
from bs4 import BeautifulSoup
import requests


jobs: dict = {}


def get_soup(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }
    web_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_page.text, 'html.parser')
    return soup


def collect_jobstreet_jobs(term: str):
    base_url = 'https://www.jobstreet.com.sg'
    url = f"{base_url}/en/job-search/{term}-jobs/"
    soup = get_soup(url)
    articles = soup.find(id='contentContainer').find(
        'div', attrs={'data-automation': 'jobListing'}).find_all('article', {'recursive': False})
    jobs = []
    for article in articles:
        h1 = article.find('h1')
        info = h1.parent.find_all('span', {'recursive': False})
        link = base_url + h1.find('a')['href']
        title = info[0].get_text().strip().replace(',', '.').replace('\n', '')
        company = info[1].get_text().strip().replace(
            ',', '.').replace('\n', '')
        jobs.append({'title': title, 'company': company, 'link': link})
    return jobs


def collect_remoteok_jobs(term: str):
    base_url = 'https://remoteok.com'
    url = f"{base_url}/remote-{term}-jobs"
    soup = get_soup(url)
    jobs_list = soup.find('table', {'id': 'jobsboard'}).find_all(
        'tr', {'class': 'job', 'recursive': False})
    jobs = []
    for job in jobs_list:
        company = job.find('td', {'class': 'company'})
        name = company.find(
            attrs={'itemprop': 'hiringOrganization'}).find(attrs={'itemprop': 'name'}).get_text().strip().replace(',', '.').replace('\n', '')
        title = company.find(
            attrs={'itemprop': 'title'}).get_text().strip().replace(',', '.').replace('\n', '')
        link = company.find('a', attrs={'itemprop': 'url'})['href']
        jobs.append({'title': title, 'company': name, 'link': link})
    return jobs


def collect_wwr_jobs(term: str):
    base_url = 'https://weworkremotely.com'
    url = f"{base_url}/remote-jobs/search?utf8=%E2%9C%93&term={term}"
    soup = get_soup(url)
    job_sections = soup.find_all('section', {'class': 'jobs'})
    jobs = []
    for section in job_sections:
        job_lists = section.find('article').find(
            'ul').find_all('li', {'class': 'feature', 'recursive': False})
        for li in job_lists:
            job = li.find_all('a', {'recursive': False})[1]
            if not job.find('span', {'class': 'title'}) or not job.find('span', {'class': 'company'}):
                continue
            title = job.find('span', {'class': 'title'}
                             ).text.strip().replace(',', '.').replace('\n', '')
            company = job.find('span', {'class': 'company'}).text.strip().replace(
                ',', '.').replace('\n', '')
            link = base_url + (job['href'] or '')
            jobs.append({'title': title, 'company': company, 'link': link})
    return jobs


def get_jobs(term: str):
    print("\033c")
    global jobs
    jobs_list = []
    wwr = jobs.get('wwr')
    if not wwr:
        jobs['wwr'] = collect_wwr_jobs(term)
    jobs_list.extend(jobs['wwr'])
    remoteok = jobs.get('remoteok')
    if not remoteok:
        jobs['remoteok'] = collect_remoteok_jobs(term)
    jobs_list.extend(jobs['remoteok'])
    jobstreet = jobs.get('jobstreet')
    if not jobstreet:
        jobs['jobstreet'] = collect_jobstreet_jobs(term)
    jobs_list.extend(jobs['jobstreet'])
    return jobs_list

