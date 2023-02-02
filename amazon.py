from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import pandas as pd

csv = []
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})





# def pages(url):
    
#     for i in range(1,21):
#         url_str = 'https://www.amazon.in/s?k=bags&page={}&qid=1675229585&ref=sr_pg_4'.format(i)


def getall(soup, lin):
    temp=""
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.string
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
        
    try:
        price = soup.find(
            "span", attrs={'class': 'a-offscreen'}).string.strip()
    except AttributeError:
        try:
            price = soup.find(
                "span", attrs={'class': 'a-offscreen'}).string.strip()
        except:
            price=""
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        
        try:
            rating = soup.find(
                "span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating=" "
    try:
        asin = soup.find(id="productDetails_detailBullets_sections1").find_all("tr")[0].find_all("td")[1].text
    except :
        asin=" "
    temp={"title":title_string,"link":lin,"price":price,"rarting":rating,"asin":asin
        
    }
    
    return(temp)

  
        
            
        
        

         
def page(url):   
       
    webpage = requests.get(url, headers=HEADERS)
    soup=BeautifulSoup(webpage.content,"lxml")
    links = soup.find_all("a", attrs={
                        'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    links_list = []
    for link in links:
        links_list.append(link.get('href'))
    
    for link in links_list[:20]:
        tempo = "https://www.amazon.in"+link

        new_webpage = requests.get(tempo, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "lxml")
        lis=getall(new_soup,tempo )
        print("progress....."+tempo)
        csv.append(lis)
        

if __name__ == '__main__':
    url = 'https://www.amazon.in/s?k=bags&page=9&qid=1675229585&ref=sr_pg_4'
    
    for i in range(1,20):
        urlt = 'https://www.amazon.in/s?k=bags&page={}&qid=1675229585&ref=sr_pg_4'.format(i)
        page(urlt)
        
    df = pd.DataFrame(csv)
    print(df.head())

    df.to_csv('amazon.csv', index=False)
    
    
    

    
    
    

