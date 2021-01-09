import requests
from bs4 import BeautifulSoup
import json
import os

token = "" #TODO replace with your token
cookies = {'inginious_session_id': token}
url_inginious = "https://inginious.info.ucl.ac.be"
course = "LSINF1101-PYTHON"
course_url = f'{url_inginious}/course/{course}'

saving_directory = 'LINFO1101'

if not os.path.exists(saving_directory):
    os.makedirs(saving_directory)



main_page_course = requests.get(course_url, cookies=cookies).text
soup = BeautifulSoup(main_page_course)

# Find blocks of tasks
question_blocks = soup.find_all("div", {"class": "content list-group list-group-flush tasks-list"})
for block in question_blocks:
    # Find all questions in the current block
    questions = block.find_all("a", {"class": "list-group-item list-group-item-action"})

    for question in questions:
        question_name = question['href']
        question_url = url_inginious + question_name

        question_page = requests.get(question_url, cookies=cookies)
        soup_question_page = BeautifulSoup(question_page.text)
        #Find latest submission 
        submissions = soup_question_page.find("ul", {'id': 'submissions'})
        latest_submission = submissions.find('li')
        # Find the id of the latest submission
        submission_id = latest_submission["data-submission-id"]

        submission_request = requests.post(question_url, cookies=cookies, data={'@action': 'load_submission_input', 'submissionid': submission_id})
        submission = json.loads(submission_request.text)['input']
        with open(f'{saving_directory}/{question_name.split("/")[-1]}', 'w') as f:
            f.write(json.dumps(submission))