import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

def scrapper(soup,images,names,prices,ratings):
    container=soup.find('div',{'class':'o-fzoHFO o-fzoHCA o-fzoHBq'})
    if not container:
        return 
    vehicles=container.find_all('li',{'class':'o-fznJzb o-fHmpzP'})
    for vehicle in vehicles:
        #get image url
        img_url=(vehicle.img.get('src'))
        images.append(img_url)

        #names 
        name=(vehicle.img.get('alt'))
        names.append(name)

        #prices
        price=vehicle.find('span',{'class':'o-cJrNdO o-byFsZJ o-bkmzIL o-bVSleT'}).text
        prices.append(price)

        #ratings
        no_of_rating=vehicle.find('span',{'class':'o-cwUopP o-fzpimR o-KxopV o-sTQWx o-dThPjR'})
        if no_of_rating:
            rating=no_of_rating.text.split()[0]
            ratings.append(rating)
        else:
            ratings.append("N/A")



def main():
    st.title("Bike Wale Scrapper")
    search_options={
        "Scooters":"https://www.bikewale.com/best-scooters-in-india/",
        "Sports Bike": "https://www.bikewale.com/best-sports-bikes-in-india/",
        "Cruise Bike":"https://www.bikewale.com/best-cruiser-bikes-in-india/"
    }
    query=st.selectbox("Select a category to scrape:",options= list(search_options.keys()))
    main_url=search_options[query]
    images=[]
    names=[]
    prices=[]
    ratings=[]

    #get the page html content
    response=requests.get(main_url)
    if response.status_code==200:
        soup=bs(response.content,"html.parser")
        scrapper(soup,images=images,names=names,prices=prices,ratings=ratings)
    else:
        print("Data not available")
        st.markdown("Data not available")
    # name, imageurl, price, ratings
    data={
        "Image":images,
        "Name":names,
        "Price":prices,
        "Rating":ratings
    }
    df=pd.DataFrame(data=data)
    #image
    #data [name'\n\n'price'\n\n'rating ]
    df['information']=df.apply(lambda x:f"{x['Name']}\n\nPrice:{x['Price']}\n\nRating:{x['Rating']}",axis=1)
    print(df)

    # 3 cards -  - -
    #         -  - -

    num_cols=3 
    cols=st.columns(num_cols)
    # 0, 1, 2
    # 3%3=0  4%3=1 5%3=2
    #6%3=0
    for idx, row in df.iterrows():
        col_no=cols[idx%num_cols] #[0,1,2]
        with col_no:
            st.image(row["Image"],width=200)
            st.markdown(row['information'])  #scooty\n\nPrice:850\n\nRating:5
            # Scooty
            # price:850
            # Rating:5

if __name__=="__main__":
    main()



    
    

