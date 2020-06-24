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


def store_mysql(title,href,name):
    try:
   
        
        cursor = connection.cursor()
        mySql_insert_query = 'INSERT INTO singers(title,href,name) values("{0}","{1}","{2}")'.format(title,href,name)
        cursor.execute(mySql_insert_query)
        connection.commit()
 
    except mysql.connector.Error as error:
        print("Failed to insert {}".format(error))
       
 


def read_singers():
    # try:
                f= requests.get("https://wikimezmur.org/am/Gospel_Singers")   
                if(f.status_code==200):
                    # print(f.text.encode('utf-8'))
                    response=f.text.encode('utf-8')
                    soup = BeautifulSoup(response,"lxml")
                    tables=soup.findAll("table")
                    for rows in tables:
                        link= rows.findAll('a')
                        for singer in link:
                            # print(singer.text.encode('utf-8'))
                            # print(singer['href'])
                            # print(singer['title'])
                            store_mysql(singer['title'],singer['href'],singer.text.encode('utf-8'))
 
      
    # except Exception as e:
    #     print(e)

    
              
       
def main():
    read_singers()

if __name__ == "__main__":
    main()