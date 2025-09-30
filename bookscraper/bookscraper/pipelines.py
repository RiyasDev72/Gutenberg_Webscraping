# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        return item


import mysql.connector


class MySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
              user="root",  # Add your MySQL username here
              password="root",  # Add your MySQL password here
              database="scrapy"
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                url TEXT,
                about_product TEXT,
                price VARCHAR(50)
            )
        """
        )

    def process_item(self, item, spider):
        self.cursor.execute(
            """
            INSERT INTO books (name, url, about_product, price) 
            VALUES (%s, %s, %s, %s)
        """,
            (item["name"], item["url"], item["about_product"], item["price"]),
        )
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
