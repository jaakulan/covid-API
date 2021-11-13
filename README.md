## Pair Programming Challenges and Solutions
##### Challenge: 
Jaakulan is a novice at SQL queries especially the various methods on joining table together, so when updating his tables with new CSV info, the results were undesirable. For instance, when updating with data that already existed but was newly updated on the CSV that was being uploaded, the newly updated data did not appear.
##### Solution:
Alexandra peer-programmed with Jaakulan on a PSQL shell and showed him the errors he was making. She also showed him the various methods Jaakulan should think about when using SQL such as creating two tables and subtracting to get the differences which was very helpful in updating tables.


##### Challenge: 
Jaakulan was inserting data that was completly new and addition to the data that already existed. He noticed that when he inserted the data, the run time was extremly long, this was a major problem especially in the testing cases where we insert only completly new data and alot of it.
##### Solution:
Alexandra looked through Jaakulan's update code with him and found that he was increasing run time for the individual insert statements and parsing with python with each data point. She showed him a way to manipulate the data using an extra table and then inserting the non-existent data into the original table that is show cased for the queries. The extra table was then dropped. She told him that when we sacrifice the space complexity using the extra table we can exponentially increase run-time by using SQL tables which are much faster due to the way these tables store data.

## Reflection
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Design Process
##### &nbsp;&nbsp; How to represent objects
 - CSV data 
    - to hold the csv data we thought  of sending it in as a post request where we can later store in a SQL table, we chose sql over NOsql as sql would be easier to run more complex queries and also since we didn't need to store strings, it seemed like a better choice than NOsql.  
 - Queries
    - to create queries from the endpoints we wanted to use query params from the HTTP GET request. We thought this was a better way to create queries with because we can easily manipulate the data wanted in the URL and felt many searches, even in search engines such as Google uses them as well. Also since the queries didn't contain any sensitive information it would be a great choice for query params for the ease and speed of using them.
##### &nbsp;&nbsp; The relationships between objects (coupling, cohesion)
 - Cohesion
    - We had very high cohesion to easily organize all the functions and abstract the information
    - We decided to have the flask server, connected to a cleaning module, which cleaned the queries and a class for the actual queries themselves. The class for the queries had getter and setter kind of functions for the queries where the info given by the server was formatted in a way that the getter and setter can easily interpret and send the appropriate response back.
 - Coupling
   - We had very low coupling to lessen the confusion between modules and functions so we can have clear and exact code
   - We had flask app for the server where all requests were handled. A cleaning module to clean all data coming from a request. As well as a sql Connection module with a class that would handle all the queries and inserting of data. This is very low coupling as each module could is easily differentiable and have their own purpose.

##### &nbsp;&nbsp; Design of functions and your API
 - API
   - To run the REST api backedn we decided on using flask as it deal with python and has very easy implementation. We wanted easy implementation as we had a short deadline and needed the easiest and fastest backend to set up. Also both partners have experience with csv's and python modules that can handle them such as "pandas" where we converted the csv into a dictionary for insertion of data.
   - For the HTTP Requests we used query params because we felt it would be the easiest and most efficient way for a user to get their data. We also thought that many other search engines do the same way so it made more sense for these types of searches.
   - Our API has the following endpoints:
     - Daily Reports uses the prefix '/daily' for all requests to specify the info needs to come from daily report csv's
     ex. "/daily/addNewCSV". The following are the suffixes that follow for the different endpoints:
        - /addNewCSV
        - /updateWithCSV
        - /viewAll
        - /deleteAll
        - /info
    - The API would send these requests to the backend which was connected to a SQL server. We chose SQL over NoSQL for reasons mentioned above in representation of objects for queries. The SQL server was postgreSQL because both partners had previous experience with this database as it was taught in our "Intro to Databases Course" (CSC343). The module we used to create sql statements and send the to the server was psycopg2, which was also because of previous experience for both partners, and was very easy to use, as the SQL statements could be run in a PSQL shell then easily copied for our module to run in the backend.
    - After recieving the data back from the database our API sends a response either as a CSV or JSON using the module json or panda's dataframe to csv conversion. If the data was not possible to get or a bad query was put in the params the API would respond with an error message.
 - Design of functions
   - We designed the functions in our flask app to handle HTTP requests and followed the REST API guidelines from class.
    
##### &nbsp;&nbsp; Using design patterns effectively
