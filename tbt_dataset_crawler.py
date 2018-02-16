#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon
# =================================================================
# this crawler wiritten to crawl a dataset website http://tbt.testrust.com/

import urllib.request, urllib.parse, urllib.error
import threading
import time, re, os
from bs4 import BeautifulSoup

# setting regex 
circular_member_word = '>(.*?)<'                
num_word = r'\d+\.?\d*'                         # match number 
span_word = '</span><span>(.*?)</span>'
spanh_word = '</span(.*?)</span></h1>'
spans_word = '</span(.*?)</span>'
# compile all regex
circular_member_pattern = re.compile(circular_member_word, re.I)
num_pattern = re.compile(num_word, re.I)
span_pattern = re.compile(span_word, re.I)
spanh_pattern = re.compile(spanh_word, re.I)
spans_pattern = re.compile(spans_word, re.I)

# generate info file
info_file_path = 'E:\\Workstation\\TBTDataCrawler\\tbt_dataset.txt'
if os.path.exists(info_file_path):
    os.remove(info_file_path)

total_elapsedtime = 0

def crawl_one_page_target(i, sub_url_list, num2_list):
    '''Crawl one page in main website
        
        :param i            url index
        :param sub_url_list sub-url list
        :param num2_list    sub-url with num list
        :return:            none
    '''
    global total_elapsedtime
    # set one url
    print('No.%d page check, waiting...' % i) 
    response = urllib.request.urlopen(
        r'http://tbt.testrust.com/notify/tbt------' + str(i) + r'.html')  
    if response.getcode() == 200:
        print('Webpage response successfully')
    else:
        print('Webpage response fatal')
    web_src = response.read().decode("UTF-8", "ignore")
    # collect the need url list
    soup = BeautifulSoup(web_src, 'lxml')
    member_list = circular_member_pattern.findall(
        str(soup.find_all(width="121")))[::2]
    num_list = num_pattern.findall(
        str(soup.find_all(width="161")))
    for i in enumerate(num_list):
        if '.' in i[1]:
            num2_list.append(i[1])

    # collect all of sub-url and their circular number
    for i in range(len(member_list)):
        if member_list[i] == r'美国':
            sub_url_list.append(
                r'http://tbt.testrust.com/notify/tbt/detail/' 
                    + num2_list[i] + r'html')
        else:
            pass
    
    if len(sub_url_list) != 0:
        for i in enumerate(sub_url_list):
            # log elapsed time
            starttime = time.time()
            response = urllib.request.urlopen(i[1])  
            web_src = response.read().decode("UTF-8", "ignore") 
            soup = BeautifulSoup(web_src, 'lxml')
            circular_number = str(soup.find_all(id="Title"))[43:-8]
            avisodate = str(soup.find(id="AvisoDate"))[46:-8]
            # save all info list in a txt document
            agency_bs4 = soup.find(id='trAgency')
            try:
                agency = span_pattern.findall(str(agency_bs4))[0]
            except:
                agency = ''

            temp_bs4 = soup.find(id='trProduct')
            try:
                temp = span_pattern.findall(str(temp_bs4))
                cover_product = temp[0]
                cover_product_hs = temp[1]
                cover_product_ics = temp[2]
            except:
                cover_product = ''
                cover_product_hs = ''
                cover_product_ics = ''

            purpose_reason_bs4 = soup.find(id='trObjectReason')
            try:
                purpose_reason = span_pattern.findall(str(purpose_reason_bs4))[0]
            except:
                purpose_reason = ''

            circular_title_bs4 = soup.find(id='trnotititle')
            try:
                circular_title \
                    = spanh_pattern.findall(str(circular_title_bs4))[0][22:]
            except:
                circular_title = ''

            relate_file_bs4 = soup.find(id='trLanguage')
            try:
                relate_file = span_pattern.findall(str(relate_file_bs4))[0]
            except: 
                relate_file = ''

            view_feedback_deadline_bs4 = soup.find(id='trEndDate')
            try:
                view_feedback_deadline \
                    = span_pattern.findall(str(view_feedback_deadline_bs4))[0]
            except:
                view_feedback_deadline = ''

            content_resume_bs4 = soup.find(id='trContent')
            try:
                content_resume = span_pattern.findall(str(content_resume_bs4))[0]
            except:
                content_resume = ''

            temp_bs4 = soup.find(id='trAdoptionDate')
            try:
                temp = spans_pattern.findall(str(temp_bs4))
                approval_date = temp[0][7:]
                entry_date = temp[1][30:]
            except:
                approval_date = ''
                entry_date = ''

            # write content into file
            content = ("\n%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" 
                % (circular_number, avisodate, agency, cover_product, 
                cover_product_hs, cover_product_ics, purpose_reason, 
                circular_title, relate_file, view_feedback_deadline, 
                content_resume, approval_date, entry_date))
            info_file = open(info_file_path, 'a+', encoding="utf-8")
            info_file.write(content)
            info_file.close()
            endtime = time.time()
            elapsed_time = endtime - starttime
            total_elapsedtime += elapsed_time
            print('Gather this item all info complete, elapsed time %.2fs' 
                % elapsed_time)
        print('Gather this page complete, next page')
    else:
        print('None of need info in this page, next page')

class _MultiThreading(threading.Thread):
    """Overrides its run method by inheriting the Thread class

    This class can be placed outside the main class, you can also put inside
    Threads are the smallest unit of program execution flow
    That is less burdensome than process creation
    Internal call
    """

    # handle thread max limit
    queue_t = []
    event_t = threading.Event()     # use event let excess threads wait

    def __init__(self, lock, i, sub_url_list, num2_list, thmax):
        """Provide class arguments

        :param lock:            object lock
        :param i:               url index
        :param sub_url_list     sub-url list
        :param num2_list        sub-url with num list
        :param thmax:           thread queue max count
        """

        threading.Thread.__init__(self)     # callable class init
        self.lock = lock
        self.i = i
        self.sub_url_list = sub_url_list
        self.num2_list = num2_list
        self.thmax = thmax

    def run(self):
        """Overwrite threading.thread run() method

        :return:    none
        """
        try:
            # create a new thread
            crawl_one_page_target(self.i, self.sub_url_list, self.num2_list)
        except Exception as e:
            print('Threading occur error:', str(e))

        self.lock.acquire()
        if len(self.queue_t) == self.thmax - 1:
            self.event_t.set()
            self.event_t.clear()
        self.queue_t.remove(self)       # remove end thread from list       
        self.lock.release()

    def create(self):
        """Create a new thread

        It can handle more over threads create
        :return:    none
        """
        self.lock.acquire()
        self.queue_t.append(self)
        self.lock.release()
        self.start()                    # finally call start() method

_alivethread_counter = 0
first_push_stack = 500

# ergodic all website 
for i in range(1, 406):
    sub_url_list = []
    num2_list = []
    aliveThreadCnt = queueLength = 405
    # first push N tasks to stack 
    if queueLength > first_push_stack:
        thread_max_count = queueLength - first_push_stack 
    else:
        thread_max_count = queueLength
    # create overwrite threading.Thread object
    lock = threading.Lock()
    # handle thread create max limit
    lock.acquire()
    # if now all of threads count less than limit, ok
    if len(_MultiThreading.queue_t) \
            > thread_max_count:
        lock.release()
        # wait last threads work end
        _MultiThreading.event_t.wait()
    else:
        lock.release()
    # continue to create new one
    sub_thread = _MultiThreading(lock, i, sub_url_list, 
        num2_list, thread_max_count)
    # set every download sub-process is non-daemon process
    sub_thread.setDaemon(False)
    sub_thread.create()
    # parent thread wait all sub-thread end
    while aliveThreadCnt > 1:
        # global variable update
        _alivethread_counter = threading.active_count()
        # when alive thread count change, print its value
        if aliveThreadCnt != _alivethread_counter:
            # update alive thread count
            aliveThreadCnt = _alivethread_counter
            
print('Gather all tbt data complete, elapsed time %.2fs' % total_elapsedtime)
print('Crawler has completed work')
print('code by </MATRIX>@Neod Anderjon(LeaderN)')

# =================================================================
# code by </MATRIX>@Neod Anderjon
