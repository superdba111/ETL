# ETL/ELT
informatica/ODI/Pendaho/Talend/Tableau Prep

I ever used all of them in the different years in the companies, Did Exercises and posted them on their folder

Tableau Prep can do the following, Data clean, combine, aggregate, workflow, pivot, union, join, filter etc. This Feb(2018) I gave my feedback to Tableau Beta support on no rep and JVM performance issue for large data etc, suggestions--the user can turn off/on some calculations like data distribution etc

Besides aboves, all ETL/ELT tool can do lookup, router, sorter, rank, data validation etc.

tried other ETL tools like datastage, babelway, boomi but gave them up

Python with Airflow ETL is located in DS folder, here are all tools 

Here are some checklist for your ETL testing plan,

### Data Completeness: ensures that all the data from the source are loaded into the target destination.
### Data Correctness: ensures that all the data is accurately transformed and loaded from the source to the target destination.
### Performance Testing: ensures if an ETL system can handle an expected load of multiple users and transactions.
### Metadata Testing: checks whether data retains its integrity up to the metadata level, It involves validating the source and the target table structure w.r.t. the mapping document. The mapping document contains all the fields that define the structure of tables in the source and the target systems like length, data type, index etc.
### Syntax Testing: checks for poor data due to invalid characters and incorrect character cases.
### Data Validation: checks whether the values of the data post-transformation are the same as their expected values with respect to the the source values.

Reusability--- use ETL Templates and Packages for handling Common functions

Auditability--- Track input and output records at Every step - (ETL Process iD)

Change Data Capture:  Process new, Changed or Deleted Data only 

Data staging:  record of Data that will be - and was - Loaded

Data Consistency:  Ensure Consistency/Conformity of Target Data

Load Lockout mgmt:  Prevent user access to inconsistent Data During Load Cycle

Data Profiling:  Check validity of source Data

recovery and restart:  Logic is graceful at Preventing Data Deduplication 

Data validation:  Provide Data accounting from source to Targets

Error handling:  graceful Termination with notification to a Consistent Data state

fit for function:  adopt Design Practices that Best fit the functional goals    



