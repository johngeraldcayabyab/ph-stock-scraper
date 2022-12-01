# import requests
from urllib.request import Request, urlopen

# response = requests.get('https://www.google.com')
# print(response)

headers = {
    "accept": 'application/json, text/plain, */*',
    "accept-encoding": 'gzip, deflate, br',
    "accept-language": 'en-US,en;q=0.9',
    "domain-id": 'ph',
    "origin": 'https://ph.investing.com',
    "referer": 'https://ph.investing.com/',
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": '?0',
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": 'empty',
    "sec-fetch-mode": 'cors',
    "sec-fetch-site": 'same-site',
    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}
#
# response = requests.get(
#     'https://api.investing.com/api/financialdata/historical/102326?start-date=2021-01-01&end-date=2021-12-01&time-frame=Daily&add-missing-rows=false',
#     headers)
#
# print(response)


# headers = {
#     ':authority': 'ph.investing.com',
#     ':method': 'GET',
#     ':path': '/equities/transasia-oil-historical-data',
#     ':scheme': 'https',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'en-US,en;q=0.9',
#     'cache-control': 'max-age=0',
#     'cookie': 'udid=4bba8fdd4af6786ad9320ce805c0cd2e; pm_score=clear; _hjSessionUser_174945=eyJpZCI6ImRiOWM2YjUwLTRjYmUtNTIyNi1iMjgxLWJkNzQ1ZGRiZTMwYyIsImNyZWF0ZWQiOjE2NjczNTU0MzI4ODUsImV4aXN0aW5nIjp0cnVlfQ==; __gads=ID=417c30b4a4746791:T=1667359362:S=ALNI_MawYGl4WUrT_w7fVA24xuA_BSrbhA; _pbjs_userid_consent_data=3524755945110770; _lr_env_src_ats=false; _cc_id=49bdfad65a1b49598c8264bcc197f832; SideBlockUser=a%3A1%3A%7Bs%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A2%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A102326%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A23%3A%22%2Fequities%2Ftransasia-oil%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A102293%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A23%3A%22%2Fequities%2Fphil-stk-exch%22%3B%7D%7D%7D%7D; gcc=JP; gsc=; smd=4bba8fdd4af6786ad9320ce805c0cd2e-1669855692; __cflb=02DiuF9qvuxBvFEb2qB1U5CGcm1MTgrGUTys2Mgb7mfsS; _hjIncludedInSessionSample=0; _hjSession_174945=eyJpZCI6IjcyMmY4NzQxLTRmMWMtNDQwZi04MWM3LTEyMmUwMDYyYzI1MCIsImNyZWF0ZWQiOjE2Njk4NTU2OTQzODgsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; user-browser-sessions=2; browser-session-counted=true; _gid=GA1.2.139876124.1669855697; __gpi=UID=00000b732e14d2b6:T=1667359362:RT=1669855696:S=ALNI_MYPRFpBUSdEOXRLwfRgqYST9yHC6w; _lr_retry_request=true; pbjs-unifiedid=%7B%22TDID%22%3A%22df0425fd-0b31-4f4a-bbbd-3f9af4aa8d51%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222022-11-01T00%3A48%3A21%22%7D; pbjs-unifiedid_last=Thu%2C%2001%20Dec%202022%2000%3A48%3A21%20GMT; panoramaId_expiry=1670460501506; panoramaId=d837c27f79438022b6f9f61188d316d539380cc201d85b3af9a5dfb97c808161; __cf_bm=5GP9mNnDzf7ALugLsQFTrFvyhJCVCHAxCL0ScJa6MEI-1669856729-0-AfceWR2W2yad50+fHR9uqla59tSNixhyezc8kQ/ADIN/kT6cxr+eccP2HDsZPrGFEWxQHBRpIPi2OETwSdJP1CM=; page_view_count=4; _ga_C4NDLGKVMK=GS1.1.1669855696.4.1.1669856731.58.0.0; _ga=GA1.1.2147102530.1667359362; _dd_s=logs=1&id=4a788481-9b19-4c00-91a6-d86234db3527&created=1669855696175&expire=1669857749947',
#     'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"macOS"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
# }
#
# response = requests.get('https://ph.investing.com', headers={'User-Agent': 'Mozilla/5.0'})
# print(response)


req = Request(
    url='https://api.investing.com/api/financialdata/historical/102326?start-date=2021-01-01&end-date=2021-12-01&time-frame=Daily&add-missing-rows=false',
    headers=headers
)
webpage = urlopen(req).read()

print(webpage)
