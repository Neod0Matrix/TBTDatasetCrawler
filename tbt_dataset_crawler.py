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

# ergodic all website 
for i in range(1, 406):
    sub_url_list = []
    num2_list = []
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
            # log info transfer time
            start_time = time.time()

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
                circular_title 
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
                view_feedback_deadline 
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
            end_time = time.time()
            print('Gather this item all info complete, elapsed time %.2fs'
                % (end_time - start_time))
        print('Gather this page complete, next page')
    else:
        print('None of need info in this page, next page')

print('Crawler has completed work')
print('code by </MATRIX>@Neod Anderjon(LeaderN)')

# =================================================================
# code by </MATRIX>@Neod Anderjon
