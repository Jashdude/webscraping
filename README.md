Assignment Coverage: Web Scraping, NumPy
Introduction
Below are questions related to recent Web scraping and NumPy course work. You are to complete the questions using what you have learned from the readings and by completing the lab work. Do not attempt to solve these problems until you have successfully completed all related lab work.
Question 1 - Book Data Scraper
You have been asked to collect some price data about books from the Books to Scrape website. Specifically, you are to scrape and capture the following book related information - book category, book title, star rating and price. Once captured, you are to output your results to a CSV file.
Script Name Requirement: book_scraper.py
Input Used: http://books.toscrape.com/
Output: book_data.csv
Requirements Overview
1. Examine the HTML returned from the Books to Scrape top-level URL. Your objective is to identify and extract book category and the book category URL information from this page.
2. For each book category URL, follow the URL to the book category page. You may restrict your data scraping to the first page of books returned for the category URL.
3. For each of the books on a category page, capture the book title, star rating and price.
4. Convert the ordinal star rating data to a numeric scale. For example, the string ‘star-rating One’ would be converted to the number 1, ‘star-rating Two’ would be converted to 2, and so on.
5. For each book, output one line containing the book category, title, numeric star rating and price to a CSV file.
Challenge
Book data in a category is returned 20 books at a time from the category URLs. If there more than 20 books in category, a Next link appears at the bottom of the HTML page. Modify your solution to follow the Next page links located at the bottom of a category page. When the list of books in a category has been exhausted, ie., when the last category page has been reached, the Next link will no longer appear on the page.
Page – 2
Question 2 - Rabbit Island Data
There is a small island in the Seto Inland Sea called Ōkunoshima, two miles off the coast of the Japanese city of Takehara, in Hiroshima Prefecture. These days, though, it’s most often referred to by its nickname Usagi Jima, which translates to Rabbit Island and is so named for the feral rabbits that call it home.
You are to examine some population data of the furry inhabitants of rabbit island. The csv input file contains rabbit population data by year for 3 rabbit breeds. FYI, while rabbit island is real, this data is fictitious.
Script Name Requirement: rabbit_pop.py
Input Used: rabbit_population_1900_2019.csv
Output: print statements
Requirements Overview
Complete each of the following steps using the NumPy library. For all computational steps, display your results via print. By default, NumPy will print abbreviated array data where appropriate– which is what we want.
1. Review the documentation for the np.loadtext() constructor. Load the csv data into an NumPy array using np.loadtext().
2. What is the mean population for each breed?
3. What is the standard deviation of the population for each breed?
4. In which year did each breed experience their maximum populations? ( Hint: consider np.argmax)
5. Which breed has the largest population for each year. ( Hint: consider np.argsort and fancy indexing)
6. In which years are any of the populations greater than 50000. (Hint: consider logical comparisons and np.any )
7. In which 2 years did each breed experience their minimum population levels. ( Hint: consider np.argsort and fancy indexing )
8. Rely on broadcasting to mean center all of the population columns. Your solution should simultaneously center all 3 columns. Print the resulting array.
9. Rely on broadcasting to normalize the population columns to the number of standard deviations from the mean. Your solution should simultaneously normalize all 3 columns. Print the resulting array.
Assignment Deliverables
Once you have completed the tasks above, create a single ZIP file containing the contents of the folder that holding all of your solution scripts and any output files (ie, your project workspace). You may upload your ZIP file solutions as many times as necessary. FAVOR: your workspace folder (and thus your ZIP file) should not contain sub-folders.
