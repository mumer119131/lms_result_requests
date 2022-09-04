from email import header
from urllib import request
import requests
import re
from bs4 import BeautifulSoup
BASE_URL = "http://lms.uaf.edu.pk/login/index.php"
def getResult(ag):
    response = requests.get(BASE_URL)

    token_id = re.findall("token.*;", response.text)[0][15:-2]
    session_id = response.cookies["MoodleSession"]

    url = "http://lms.uaf.edu.pk/course/uaf_student_result.php"

    result_request = requests.post(url, data={"token":token_id, "Register":ag}, cookies={"MoodleSession":session_id},verify=False)

    result_soup = BeautifulSoup(result_request.text, 'html.parser')

    single_results = result_soup.find_all('tr')
    name = single_results[1].find_all("td")[1].getText().strip()
    ag = single_results[0].find_all("td")[1].getText()
    overall_res = {"details":{"student_details":[name, ag ],"cgpa":{}}}

    for row in single_results[3:]:
        single_res_list = []
        cols = row.find_all("td")
        for col in cols:
            single_res_list.append(col.getText().strip())
            try:
              overall_res[str(cols[1].getText().strip())][str(cols[3].getText().strip())] = single_res_list
            except:
                overall_res[str(cols[1].getText())] = {}
                overall_res[str(cols[1].getText().strip())][str(cols[3].getText().strip())] = single_res_list
                
    return overall_res


def cgpaCal(overall_res):
    oneCreditSet =[ [8, 1], [9, 1.5], [10, 2], [11, 2.33], [12, 2.67], [13, 3], [14, 3.33],
                    [15, 3.67], [16, 4]
            ]
    twoCreditSet =[ [16, 2], [17, 2.5], [18, 3], [19, 3.5], [20, 4], [21, 4.33], [22, 4.67],
                    [23, 5], [24, 5.33], [25, 5.67],
                    [26, 6], [27, 6.33], [28, 6.67], [29, 7], [30, 7.33], [31, 7.67], [32, 8]
            ]

    threeCreditSet = [ [24, 3],
            [25, 3.5], [26, 4], [27, 4.5], [28, 5], [29, 5.5], [30, 6], [31, 6.33], [32,
            6.67],
            [33, 7], [34, 7.33], [35, 7.67], [36, 8],
            [37, 8.33], [38, 8.67], [39, 9], [40, 9.33], [41, 9.67], [42, 10], [43,
            10.33],
            [44, 10.67], [45, 11], [46, 11.33], [47, 11.67],
            [48, 12]
    ]

    fourCreditSet = [ [32, 4],
            [33, 4.5], [34, 5], [35, 5.5], [36, 6], [37, 6.5], [38, 7], [39, 7.5], [40,
            8],
            [41, 8.33], [42, 8.67], [43, 9], [44, 9.33],
            [45, 9.67], [46, 10], [47, 10.33], [48, 10.67], [49, 11], [50, 11.33], [51,
            11.67],
            [52, 12], [53, 12.33],
            [54, 12.67], [55, 13], [56, 13.33], [57, 13.67], [58, 14], [59, 14.33], [60,
            14.67],
            [61, 15], [62, 15.33], [63, 15.67],
            [64, 16]
    ]

    fiveCreditSet = [ [40, 5], [41, 5.5], [42, 6], [43, 6.5], [44, 7], [45, 7.5], [46, 8],
                    [47, 8.5],
                    [48, 9], [49, 9.5], [50, 10], [51, 10.33], [52, 10.67], [53, 11], [54,
                    11.33],
                    [55, 11.67], [56, 12], [57, 12.33], [58, 12.67],
                    [59, 13], [60, 13.33], [61, 13.67], [62, 14], [63, 14.33], [64, 14.67], [65,
                    15],
                    [66, 15.33], [67, 15.67], [68, 16], [69, 16.33],
                    [70, 16.67], [71, 17], [72, 17.33], [73, 17.67], [74, 18], [75, 18.33], [76,
                    18.67],
                    [77, 19], [78, 19.33], [79, 19.67],
                    [80, 20]
            ]
    
    for semester, semester_result in overall_res.items():
        total_qp =float()
        total_credits = int()
        cgpa = float()
        if semester == "details":
            continue
        for result in semester_result.values():
            marks = int(result[10])
            credit_hr = int(result[5][0])
            print(marks, credit_hr)

            total_credits += credit_hr

            if credit_hr == 1:
                total_qp = total_qp + qpCalculator(marks,oneCreditSet)
                continue
            elif credit_hr == 2:
                total_qp = total_qp + qpCalculator(marks,twoCreditSet)
                continue 
            elif credit_hr == 3:
                total_qp = total_qp + qpCalculator(marks,threeCreditSet)
                continue
            elif credit_hr == 4:
                total_qp = total_qp + qpCalculator(marks,fourCreditSet)
                continue
            elif credit_hr == 5:
                total_qp = total_qp + qpCalculator(marks,fiveCreditSet)
                continue

            
        cgpa = float(total_qp/total_credits)
        overall_res["details"]["cgpa"][semester] = round(cgpa, 2)
    
    return overall_res


def qpCalculator(marks,set_qp):
     qp = float()
     if marks < set_qp[0][0]:
        qp = 0
     elif marks > set_qp[1][0] and marks <= set_qp[len(set_qp)-1][0]:
        for i in range(0,len(set_qp)):
            if marks == set_qp[i][0]:
                qp = set_qp[i][1]
                break    
     elif marks > set_qp[len(set_qp)-1][0]:
             qp = set_qp[len(set_qp)-1][1]
     
     return qp
cgpaCal(getResult("2019-ag-6081"))
