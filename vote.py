"""

网站投票demo
time: 20220810:17:30
URL: https://www.change.org/p/olympians-support-the-olympic-truce-the-olympic-games-the-paralympics-sign-and-share

"""
import json

from faker import Faker
import  requests
import re
import random
faker = Faker()
#crsf获取网址
BASE_URL = "https://www.change.org/login_or_join?user_flow=nav"
#注册请求的网址
SING_UP_URL = "https://www.change.org/api-proxy/-/users"




#实现请求头格式化
def change_headers_tool(headers_raw):
    if headers_raw is None:
        return None
    headers = headers_raw.splitlines()
    headers_tuples = [header.split(':', 1) for header in headers]

    result_dict = {}
    for header_item in headers_tuples:
        if not len(header_item) == 2:
            continue
        item_key = header_item[0].strip()
        item_value = header_item[1].strip()
        result_dict[item_key] = item_value
    return result_dict

#1.提供随机用户信息模块 姓 名 电子邮箱 密码 四个信息
def fake_info():
    if len(faker.name().split()) == 1:
        first_name = faker.name()
        second_name = faker.name()
    else:
        first_name = faker.name().split()[0]
        second_name = " ".join(faker.name().split()[1:])

    res = {"first_name": first_name,"second_name": second_name,"email"
    :faker.email(),"pwd":faker.password(upper_case= True,lower_case = True,length = random.randint(13,20))}
    print(res)
    return res

csrf_headers  = change_headers_tool(
    """
    authority: www.change.org
method: GET
path: /login_or_join?user_flow=nav
scheme: https
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: max-age=0
referer: https://www.change.org/
sec-ch-ua: ";Not A Brand";v="99", "Chromium";v="94"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.169.400 QQBrowser/11.0.5130.400

    """
)

sign_headers ="""
authority: www.change.org
method: POST
path: /api-proxy/-/users
scheme: https
accept: application/json, text/javascript, */*; q=0.01
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
content-length: 276
content-type: application/json

origin: https://www.change.org
referer: https://www.change.org/login_or_join?user_flow=nav
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36
x-csrf-token: {}
x-requested-with: jquery
"""

vote_headers= """
authority: www.change.org
method: POST
path: /api-proxy/graphql/signPetition/31990371
scheme: https
accept: application/json
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5
content-length: 1558
content-type: application/json
origin: https://www.change.org
referer: https://www.change.org/p/olympians-support-the-olympic-truce-the-olympic-games-the-paralympics-sign-and-share
sec-ch-ua: "Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47
x-requested-with: http-link
"""

def vote(s):
    data = json.loads(
    r"""{"operationName":"SignatureSharedCreateSignature","variables":{"shouldRewardShareBandit":false,"rewardShareBanditInput":{"banditId":"","variantName":""},"signatureInput":{"petitionId":"31990371","city":"","countryCode":"TW","firstName":"Monica","lastName":"Bell","email":"qolson@example.com","reasonForSigning":null,"stateCode":null,"postalCode":null,"shareInfoWithOrganization":false,"public":true,"marketingCommsConsent":null,"recaptchaResponse":null,"smsCommsConsent":null,"whatsappCommsConsent":null,"sourceLocation":null,"algorithm":null,"inviteRecruiterUuid":null,"inviteRecruiterId":null,"inviteRequestedAt":null,"trafficMetadata":{"currentSource":null,"currentMedium":null,"referringDomain":null},"mitTrackingValue":null,"fhtTrackingValue":null,"trackingData":{"webapp_name":"corgi"},"recentlySeenMembershipRequest":false,"isMobile":false,"promotionToken":null,"promotionPlacement":null,"pageContext":"petitions_show","resubmit":false,"pendingReason":null,"userSawSignInterrupt":false}},"query":"mutation SignatureSharedCreateSignature($shouldRewardShareBandit: Boolean!, $rewardShareBanditInput: BanditInput!, $signatureInput: SignPetitionInput!) {\n  rewardShareBandit: rewardBandit(input: $rewardShareBanditInput) @include(if: $shouldRewardShareBandit)\n  signPetition(input: $signatureInput) {\n    __typename\n    ... on SignPetitionMutationSuccess {\n      redirectUrl\n    }\n    ... on SignPetitionMutationGuestSignByExistingUserFailure {\n      user {\n        id\n        connectedToFacebook\n        passwordSet\n      }\n    }\n  }\n}\n"}""")
    print(data)
    input()
    res = s.post("https://www.change.org/api-proxy/graphql/signPetition/31990371",headers = change_headers_tool(vote_headers),data =data )
    print(res.text)
    print(res.status_code)
#实现用户的注册
def sign_up():
    user_info = fake_info()

    #注册前先取到crsf特征码
    s = requests.session()

    print("正在搜集csrf码,请稍后")
    res = s.get(BASE_URL,headers= csrf_headers)
    csrf = re.findall('"csrfToken":"(.*?)",',res.text)[0]
    print("csrf码搜集完毕: " ,csrf)
    print(res.cookies.items())
    print("csrf码准备传入注册机..." )
    data = {
    "email": user_info["email"],
"first_name": user_info["first_name"],
"in_sap_flow": "",
"last_name": user_info["second_name"],
"locale": "en-US",
"marketing_comms_consent": None,
"organization_name": "",
"password": user_info["pwd"],
"shouldValidatePassword": True,
"using_pending_petitions": False,
"validateAs": "save"
    }
    data = json.dumps(data)
    # print(data)

    for i,v in res.cookies.items():
        s.cookies[i] = v
    need_cookies = ""

    need_cookies    =     f"""pxcts=efce1f32-1891-11ed-a936-50795375546a; _pxvid=efce13b7-1891-11ed-a936-50795375546a; _ga=GA1.2.336410908.1660125059; _gid=GA1.2.2007200217.1660125059; _gcl_au=1.1.417889450.1660125062; _fbp=fb.1.1660125063214.1101856385; _hjSessionUser_1693228=eyJpZCI6IjViZjMxZDJiLTAyMWItNTMwNi1hZjNlLTFiYTY1NmQ0Y2EzMyIsImNyZWF0ZWQiOjE2NjAxMjUwNjM0OTksImV4aXN0aW5nIjp0cnVlfQ==; _tt_enable_cookie=1; _ttp=ddf7774f-d150-413b-b4f3-a3708baf76fa; browserupdateorg=pause; optimizelyEndUserId=oeu1660125428288r0.8053805594990735; G_ENABLED_IDPS=google; __stripe_mid=09e6ed98-4246-4c8a-a562-89fef55ef55d4da3e8; dont_auto_login_via_facebook=true; _hjIncludedInSessionSample=0; _change_session={res.cookies.items()[2][1]}; __cfruid={res.cookies.items()[0][0]}; _uetsid=f26482b0189111eda92239dd94dd589d; _uetvid=f264f970189111eda9a303a5b9344315; _hjCachedUserAttributes=eyJhdHRyaWJ1dGVzIjp7ImNvdW50cnlDb2RlIjoiSlAiLCJlbnZpcm9ubWVudCI6InByb2R1Y3Rpb24iLCJsb2NhbGUiOiJqYS1KUCIsImxvZ2luU3RhdGUiOiJndWVzdCIsIndlYmFwcE5hbWUiOiJmZSIsIndlYmFwcFZlcnNpb24iOiIyMS4xMzY2LjAifSwidXNlcklkIjpudWxsfQ==; _change_lang={res.cookies.items()[1][1]}; _px3=fb77000ebada5e8525ef573a83b57f38c0ea1c5677aeb3fd7180e10386e876bc:9A1F1Ej01yHl646dBaQBUhvW+b9fPum7iSoxX1MNFYN+/vzXzCdNflLw8IDzJJvTcMNlpYbjW9X5jAYijmOmGQ==:1000:xQyIj5NrO3zbwHVLMHp9o+KnunqLvfE/dGG6SXTaynUC/h9V2whevZLF8VomSrk62oh5L6phGZmxL9UuTb1Ikh0KB9feXFklgoEKV0cE5VTCs4kUHEAfvUKTyce2ITFhMKYP2lyIOYibqdKuS3p2Zv7SmDs9TGo8FudyDDcmrktAyl5I5t3Mni7kbQxTPKkzvByS7vSat12Y6ZS/Dzc+3w=="""
    headers = change_headers_tool(sign_headers.format(csrf))
    # headers["cookie"] = """_change_session=5b7b907701dfa3794fb5bee6cae28c2a; _change_lang=%7B%22locale%22%3A%22en-US%22%2C%22countryCode%22%3A%22TW%22%7D; browserupdateorg=pause; _gcl_au=1.1.316886141.1660131457; _ga=GA1.2.40976423.1660131458; _gid=GA1.2.1762181449.1660131458; _fbp=fb.1.1660131459474.198927234; _tt_enable_cookie=1; _ttp=6357418f-0383-49d1-80b1-b7716c254cd3; _hjIncludedInSessionSample=0; _hjSessionUser_1693228=eyJpZCI6Ijk1YzRkZDhmLTMwODctNTg2Ni04NWY3LTNmMjc4NTZkMmQzYSIsImNyZWF0ZWQiOjE2NjAxMzE0NTk1NjIsImV4aXN0aW5nIjp0cnVlfQ==; pxcts=ece26e2f-18a0-11ed-b352-687a6c4e6651; _pxvid=ece25edd-18a0-11ed-b352-687a6c4e6651; optimizelyEndUserId=oeu1660131498835r0.40017802887169607; G_ENABLED_IDPS=google; __cfruid=af698bc07c29180c5c12be36207034a345237593-1660135106; _pxff_fp=1; _gat=1; _px3=3d1a8e0f7f0bc5650f11399ebdc63447f2182f7afc1ee12a1334ac0551217ddc:h2nzRMB3EUc+9PUjXxHT7LEIBeCh9bXXiEF80G35cknEsylnPZ0E/UdMtiyB5wWy5In6DTBlJrvOcjEGkcvX8A==:1000:ZvM138CXpsvVVZDX9llgtUE8p21H5GR2UoAm0ttJlroBNl4HBHJZK2zarsjUuqEAo9HZBwZBzeLRT3a6yZZhgDgYAl3B2/sXnR8gKAcrOOqDcrKlH/A5ckkRkx5SEPstJIAsQ4Qol9Y6P2UMqEJm4PJkElGAbpBFXimIICcqcwlhGEKFRBCfQG4iDOOkGxM4raVJ57QIzDQiN83jZ4/1bg==; _hjSession_1693228=eyJpZCI6ImQ0ZDY0YjFlLWM2MDEtNDhjOC05YzUzLTM2NmZhYmY2OWFmMiIsImNyZWF0ZWQiOjE2NjAxMzUxMTE5MjUsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _hjCachedUserAttributes=eyJhdHRyaWJ1dGVzIjp7ImNvdW50cnlDb2RlIjoiVFciLCJlbnZpcm9ubWVudCI6InByb2R1Y3Rpb24iLCJsb2NhbGUiOiJlbi1VUyIsImxvZ2luU3RhdGUiOiJndWVzdCIsIndlYmFwcE5hbWUiOiJmZSIsIndlYmFwcFZlcnNpb24iOiIyMS4xMzY2LjAifSwidXNlcklkIjpudWxsfQ==; _uetsid=d5fe2a6018a011ed98faad7f7b2a4394; _uetvid=d5fe7ce018a011edac4c8ff1f08192ec"""


    # print(headers)

    signal = s.post(SING_UP_URL,headers = headers,data = data)
    # print(need_cookies)

    print("注册状态码: ",signal.status_code)
    if signal.status_code == 201:
        print("注册成功，正在进入活动报名页面...")

    #开始正式注册
    print("注册模拟成功 请进行验证")
    return s

s = sign_up()
vote(s)

