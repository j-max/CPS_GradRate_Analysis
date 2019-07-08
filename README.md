

# Summary

> I completed the project outlined below for the Metis Data Science Bootamp. I chose to analyze Chicago Public Schools high school graduation rates via linear regression.  I am aware that graduation rates are not the be all end all as a metric for school quality. Like test scores, graduation rates are just numbers. No matter how hard one tries, numbers can never capture the full picture of a student's education. Nonetheless, a linear regression study requires a continuous target variable, and graduation rate fits the bill.

---

# Data Sources
> The  Chicago Data Portal School Profile csv files are the main data source for this project. The current version of this project focuses on the 2016-17 and 2017-18 school years.

> 1. [School Year 2016-17](https://data.cityofchicago.org/Education/Chicago-Public-Schools-School-Profile-Information-/8i6r-et8s)
> 2. [School Year 2017-18](https://data.cityofchicago.org/Education/Chicago-Public-Schools-School-Profile-Information-/w4qj-h7bg)

> I supplimented the Data Portal data with mean incomes associated with each school's zipcode.  I used Selenium to scrape income data from the [census]( https://factfinder.census.gov). The code for the scrape can be found in the Jupyter notebook found in the [data/]('data') folder.

> To help organize the data, I loaded raw and processed data into a Postgres database, and used psycopg2 to pull it into pandas data frames.

---

# Feature Engineering

> Both the 2016-17 and 2017-18 original datasets from the data portal dataset includes 661 total schools and 184 high schools.  Of those 184 high schools, 121 in  2016-17 and 124 in 2017-18 had non-null graduation rates.  A histogram of the graduation rates across both years is left-skewed.
![left-skewed histogram of CPS high school graduation rates](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiIHN0YW5kYWxvbm)
> The features are not consistent across years; for 2016-17 there are 91 feature columns, and for 2017-18 there are 92. The following is a list of the features I analyzed.


