## Pair Programming Challenges and Solutions
##### Challenge 1: 
Jaakulan is a novice at PostgreSQL queries especially the various methods on joining table together, so when updating his tables with new CSV info, the results were undesirable. For instance, when updating with data that already existed but was newly updated on the CSV that was being uploaded, the newly updated data did not appear.
##### Solution 1:
Alexandra was the driver in a peer-programming session with Jaakulan on a PSQL shell and showed him the errors he was making. She was able to teach him commands like "\dt, \dt, INSERT, UPDATE, ALTER" and how to set schema paths. She also showed him the various methods Jaakulan should think about when using SQL such as creating two tables and subtracting to get the differences which was very helpful in updating tables.
##### Reflection 1:
After Alexandra helped Jaakulan with PostgreSQL in correlation to this assignement, Jaakulan was able to help make better queries into the database he had created. He was able to take this thoughts on how to construct tables and apply that logic in properly creating and updating a table in the joint database.

##### Challenge 2: 
Jaakulan was inserting data that was completely new and additional to the data that already existed. He noticed that when he inserted the data, the run time was extremely long, this was a major problem especially in the testing cases where we insert only completely new data and alot of it.
##### Solution 2:
Alexandra looked through Jaakulan's code for updating a table and they found that the run time was increasing for the individual insert statements and parsing with Python with each data point. She showed him a way to manipulate the data using an extra table and then inserting the non-existent data into the original table that is show cased for the queries. The extra table was then dropped. She told him that when we sacrifice the space complexity by using the extra table, we can exponentially increase run-time by using SQL tables which are much faster due to the way these tables store data.
##### Reflection 2:
Jaakulan was able to learn something new about both how taxing PostgreSQL insert statements can be over a large database, but also how to batch his inserts into new table, so that he only making one modification for his updating functions.

##### Challenge 3:
Alexandra did not know how to make tests for her API requests. She knew only how to send her requests though Postman, because that's what she saw in class. However, she didn't know how to start writing tests for her post requests for testing.

##### Solution 3:
Jaakulan had written a few tests and showed Alexandra the tools she needs to write tests. Jaakulan had used a library called "requests" on Python and was able to open files from a folder called "csvExamples" first into Python and then to the server with the requests library. Alexandra listened to Jaakulan explain the tools she needs. From there, they paired programmed a query Alexandra had wrote in Postman and send that same request through a test.

##### Reflection 3:
After Alexandra had some guidance from Jaakulan on how to turn Postman requests into requests used in unittests, she was able to apply the same formula of creating the request, sending the request and comparing the output she expected to other queries, adding files and updating databases.

## Design Process
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
