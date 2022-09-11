import requests
from bs4 import BeautifulSoup
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from model import Appartment, Base


def parse_data():  
    url = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273'
    store_ = []
    html_doc = requests.get(url)    
    if html_doc.status_code == 200:        
        soup = BeautifulSoup(html_doc.text, 'lxml')
        appartments = soup.find_all('div', class_='clearfix')
        for appartment in appartments:        
            img_url = str(appartment.find('img')).split(' data-src=')[-1].split(' src=')[0][1:-1]
            title = str(appartment.find('img')).split(' data-src=')[0][10:-1]
            date =getattr(appartment.find('span', class_="date-posted"), 'text', None)  
            if date!=None:
                if len(date)==10:
                    date2 = datetime.strptime(date, "%d/%m/%Y").date() 
                elif date=='Yesterday':
                    date2=(datetime.today() - timedelta(days=1)).date()
                else:
                    date2=datetime.today().date()
            else: date2 =None
            city =appartment.find('span', class_="").text.strip()            
            bed =str(getattr(appartment.find('span', class_="bedrooms"), 'text', None)).strip().replace((" ")*53, "").replace("\n", " ")
            description =str(getattr(appartment.find('div', class_="description"), 'text', None)).strip().split("   ")[0].replace("\n", "")
            price =str(getattr(appartment.find('div', class_="price"), 'text', None)).strip()
            store_.append({
                'img_url': img_url,
                'title': title,
                'date': date2, 
                'city': city,'bed':bed, 
                'description': description,
                'price': price
            })    
    return store_[1:]


if __name__ == '__main__':
    store = parse_data()
    engine = create_engine("sqlite:///my_appartments.db")
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    session = Session()
    for el in store:
        appartment = Appartment(img_url=el.get('img_url'), title =el.get('title'), date =el.get('date'), city =el.get('city'), bed = el.get('bed'), description = el.get('description'), price= el.get('price'))
        session.add(appartment)
    session.commit()
    session.close()