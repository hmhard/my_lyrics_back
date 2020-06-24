from bs4 import BeautifulSoup
import requests

 
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import datetime

connection = mysql.connector.connect(host='localhost',
                                            database='mylyrics',
                                            user='root',
                                            password='')

song_id=0
album_id=0

def store_singers(title,href,name):
    try:
   
        
        cursor = connection.cursor()
        mySql_insert_query = 'INSERT INTO singers(title,href,name) values("{0}","{1}","{2}")'.format(title,href,name)
        cursor.execute(mySql_insert_query)
        connection.commit()
 
    except mysql.connector.Error as error:
        print("Failed to insert {}".format(error))
def store_albums(singer_id,volume,year,title,href,name,name_eng,photo):
    try:
   
        
        cursor = connection.cursor()
        mySql_insert_query = 'INSERT INTO albums(singer_id,volume,year,title,href,name,name_eng,photo) values({0},"{1}","{2}","{3}","{4}","{5}","{6}","{7}")'.format(singer_id,volume,year,title,href,name,name_eng,photo)
        cursor.execute(mySql_insert_query)
        connection.commit()
 
    except mysql.connector.Error as error:
        print("Failed to insert {}".format(error))

def store_songs(album_id,number,title,href,name,length):
    try:
   
        
        cursor = connection.cursor()
        mySql_insert_query = 'INSERT INTO songs(album_id,number,title,href,name,length) values({0},"{1}","{2}","{3}","{4}","{5}")'.format(album_id,number,title,href,name,length)
        cursor.execute(mySql_insert_query)
        connection.commit()
 
    except mysql.connector.Error as error:
        print("Failed to insert {}".format(error))
       
 
def store_tracks(song_id,content):
    try:
   
        
        cursor = connection.cursor()
        mySql_insert_query = 'INSERT INTO tracks(song_id,content)values({0},"{1}")'.format(song_id,content)
        cursor.execute(mySql_insert_query)
        connection.commit()
 
    except mysql.connector.Error as error:
        print("Failed to insert {}".format(error))
       
 

 
def read_track(href):
    try:
        global song_id
        f= requests.get("https://wikimezmur.org{0}".format(href))   
        if(f.status_code==200):
            # print(f.text.encode('utf-8'))
            response=f.text.encode('utf-8')

            soup = BeautifulSoup(response,"lxml")
            print("track: {}".format(song_id))
            # print(soup.find('h1',{'id':'firstHeading'}).text.encode('utf8'))
            
            table=soup.findAll("table")[1]
            
            # print(table.text.encode('utf-8'))
            store_tracks(song_id,str(table.text.replace('"','\\"').replace("'","\\'").encode('utf-8')))

    except Exception as e:
        print(e)

          


def read_albums(count,href):
    try:
        global song_id
        global album_id
        f= requests.get("https://wikimezmur.org{0}".format(href))   
        if(f.status_code==200):
            # print(f.text.encode('utf-8'))
            response=f.text.encode('utf-8')

            soup = BeautifulSoup(response,"lxml")
            
            print(soup.find('h1',{'id':'firstHeading'}).text.encode('utf8'))
            tables=soup.findAll("table",{'align':"right"})
            
            for trs in tables:
                print("Total album:    {}".format(album_id+1))
                print("Total tracks:   {}".format((song_id+1)))
                year=""
                title=""
                href=""
                name=""
                name_eng=""
                photo=""
                album_id+=1
                tri=0
                tr=trs.findAll('tr')

                for lis in tr:
                    
                    
                    tri+=1
                    th= lis.findAll('th')
                    tdi=0
                    for album in th:
                        tdi=tdi+1
                        if tdi==2:
                            if album.find('a'):
                                # print(album.find('a').text.encode('utf8'))
                                # print(album.find('a')['href'])
                                # print(album.find('a')['title'])
                                title=album.find('a')['title']
                                href=album.find('a')['href']
                                name=album.find('a').text.encode('utf8')
                        else:
                            # print(album.text.encode('utf8'))
                            volume=album.text.encode('utf8')
                
                    if tri==2:
                        td= lis.findAll('td')
                        for album in td:
                                # print(album.find('img')['src'])
                                photo=album.find('img')['src']
                    if tri==3:
                        if len(tr)==4:
                            td= lis.findAll('td')
                            # print(td[1].text.encode('utf8'))
                            year=td[1].text.encode('utf8')

                store_albums(count,volume,year,title,href,name,name_eng,photo)
                    
                main_table = trs.find_next_siblings('table')[0]
                dds = main_table.findAll("dd")

                
                for dd in dds:
                    song_id+=1
                    

                    # print(str(dd.text.encode('utf8').split(') ')[0]))
                    # if dd.find('a',{'class':'new'}):
                        # print(str(dd.find('a').text.encode('utf8')))
                        # print(dd.find('a')['href'])
                        # print(dd.find('a')['title'])
                        # print(str(dd.find('span').text))
                    number=str(dd.text.encode('utf8').split(') ')[0])
                    name=str(dd.find('a').text.encode('utf8'))
                    href=str(dd.find('a')['href'].encode('utf8'))
                    length=""
                    if dd.find('a', attrs={'class': 'new'}) is not None:
                        href=""
                    if href!="":    
                        read_track(href)



                    title=str(dd.find('a')['title'].encode('utf8'))
                    if dd.find('span') is not None:
                        length=str(dd.find('span').text.encode('utf8'))
                    # print("number: {0} name:{1} href:{2} length:{3} ".format(number,name,href,length))
                    store_songs(album_id,number,title,href,name,length)

                            
                        
                    # store_mysql(count,album.find('span',{'class':'toctext'}).text.encode('utf8'))
            
            # divs=soup.findAll("div",{'class':"toc"})
            # for lis in divs:
            #     if  lis.find('li',{"class":'tocsection-1'}):
            #         link= lis.findAll('li',{"class":'toclevel-2'})
            #         for album in link:
            #             print(album.find('span',{'class':'tocnumber'}).text.encode('utf8'))
            #             print(album.find('span',{'class':'toctext'}).text.encode('utf8'))
            #             store_mysql(count,album.find('span',{'class':'toctext'}).text.encode('utf8'))
            #     else:
            #         link= lis.findAll('li',{"class":'toclevel-1'})
            #         for album in link:
            #             print(album.find('span',{'class':'tocnumber'}).text.encode('utf8'))
            #             print(album.find('span',{'class':'toctext'}).text.encode('utf8'))
            #             store_mysql(count,album.find('span',{'class':'toctext'}).text.encode('utf8'))
    except Exception as e:
        print(e)



def read_singers():
    try:
        global album_id

        f= requests.get("https://wikimezmur.org/am/Gospel_Singers")   
        if(f.status_code==200):
            # print(f.text.encode('utf-8'))
            response=f.text.encode('utf-8')
            soup = BeautifulSoup(response,"lxml")
            tables=soup.findAll("table")
            i=0
            for rows in tables:
                
                link= rows.findAll('a')
                for singer in link:
                    i=i+1
                    
                    store_singers(singer['title'],singer['href'],singer.text.encode('utf-8'))
                    
                    read_albums(i,singer['href'])
                    # read_albums(i,"/am/Tamrat_Haile")
                    # if i==10:
                    # break
                        
                # break

        
    except Exception as e:
        print(e)

    
              
       
def main():
    read_singers()

if __name__ == "__main__":
    main()