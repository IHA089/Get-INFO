import pyshorteners
import re, sys, socket


def internet_connection():
    try:
        socket.gethostbyname("www.google.com")
        return True
    except socket.gaierror:
        return False


def validate_phishing_keyword(keyword):
    pattern = re.compile(r'^[a-zA-Z0-9-_]+$')

    if pattern.match(keyword):
        return True
    else:
        return False

def shorting_url(short_obj, url):
    try:
        short_url =  short_obj.short(url)
        return short_url
    except:
        return "error"

def shortener_service(url):
    shortner = pyshorteners.Shortener()
    shorter1 = shortner.tinyurl
    shorter2 = shortner.dagd
    shorter3 = shortner.clckru
    s1 = shorting_url(shorter1, url)
    s2 = shorting_url(shorter2, url)
    s3 = shorting_url(shorter3, url)
    dbd = []
    if s1 != "error":
        dbd.append(s1)
    if s2 != "error":
        dbd.append(s2)
    if s3 != "error":
        dbd.append(s3)

    return dbd

def combiner(masked_url, domain_name, phishing_keyword):
    mskd = masked_url.split("://")
    url_header = mskd[0]
    url_tail = mskd[1]
    if phishing_keyword == "":
        result = url_header+"://"+domain_name+"@"+url_tail
    else:
        result = url_header+"://"+domain_name+"-"+phishing_keyword+"@"+url_tail

    return result

def urlmasker(original_url):
    masked_url = shortener_service(original_url)
    try:
        domain_name = input("Enter what domain you want to set[Ex. google.com, facebook.com]:")
    except KeyboardInterrupt:
        print("\nExit by user")
        return 0

    try:
        phishing_key = input("Do you want to enter phising keyword[yes/no]:")
    except KeyboardInterrupt:
        print("\nExit by user")
        return 0

    if phishing_key == "yes" or phishing_key == "YES":
        try:
            phishing_keyword = input("Enter phishing keyworkd[Ex: free, login]:")
        except KeyboardInterrupt:
            print("\nExit by user")
            return 0
        phishing_keyword = phishing_keyword.lower()
        if not validate_phishing_keyword(phishing_keyword):
            print("please enter valid phishing keyword that include alphbats, number, '-' and '_'symbol")
            return 0
    else:
        phishing_keyword = ""
    
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Unmasked URL ::: {}".format(original_url))
    for new_url in masked_url:
        result = combiner(new_url, domain_name, phishing_keyword)
        print("Masked URL:::{}".format(result))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")
    
