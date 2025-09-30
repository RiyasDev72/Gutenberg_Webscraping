from Utils.Book_processing import book_processing


def main():
    print("Hello World!")


if __name__ == "__main__":
    book_processer = book_processing(
        folder="gutenberg_Books", csv_file=r"bookscraper\bookscraper\spiders\library.csv"
    )
    book_processing.download(book_processer)
    book_processing.remove_empty_files(book_processer)