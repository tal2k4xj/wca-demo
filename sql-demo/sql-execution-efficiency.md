# SQL Execution Efficiency (based on Query Plans)

## Assess T-SQL / Azure SQL (MSSQL or SQL Server) query plans for efficiency

### Variation: T-SQL  Inefficient query
---
You are a developer examining the output of a SQL query plan. Evaluate this SQL query plan for efficiency of the query. An efficient query will have a relatively low execution cost, number of operations, and using indexes effectively. If the query is efficient answer "Yes", otherwise answer "No". Provide a step by step explanation of the SQL query plan If there are inefficiencies, highlight and explain them. Provide optimized alternatives if applicable. Provide general suggestions for improving the query's performance.

Use the query plan file: @T-SQL-QueryPlan-Inefficient.xml

### Variation: T-SQL Control
---
You are a developer examining the output of a SQL query plan. Evaluate this SQL query plan for efficiency of the query. An efficient query will have a relatively low execution cost, number of operations, and using indexes effectively. If the query is efficient answer "Yes", otherwise answer "No". Provide a step by step explanation of the SQL query plan If there are inefficiencies, highlight and explain them. Provide optimized alternatives if applicable. Provide general suggestions for improving the query's performance.

Use the query plan file: @T-SQL-QueryPlan-Control.xml 

## Assess T-SQL / Azure SQL (MSSQL or SQL Server) query plans for Unions with big result sets

### Variation: T-SQL (with Union in SQL)

---
You are a database administrator. Evaluate the output from the following sql query and query plan. Determine if the query plan contains UNION operators that will produce very large result sets. If the query plan contains UNION operators that will produce very large results set, please provide improvements to the SQL query and query plan that would not lead to very large results sets.

 Expected Output:
- Determine if the query plan contains UNION operators that would produce a very large resluts set
- If the query plan contains UNION operators that will produce very large results set, please provide improvements to the SQL query and query plan that would not lead to very large results set.

Provide optimized alternatives if applicable.

 Here is the query plan file @T-SQL-with-Union.xml

### Variation: T-SQL Control (no Union in SQL) - Control
---
You are a database administrator. Evaluate the output from the following sql query and query plan. Determine if the query plan contains UNION operators that will produce very large result sets. If the query plan contains UNION operators that will produce very large results set, please provide improvements to the SQL query and query plan that would not lead to very large results sets.

Expected Output:  
- Determine if the query plan contains UNION operators that would produce a very large resluts set
- If the query plan contains UNION operators that will produce very large results set, please provide improvements to the SQL query and query plan that would not lead to very large results set.

Provide optimized alternatives if applicable.

Here is the query plan file @T-SQL-Union-Control.xml

### Variation: (Analyzing the Query Plan from the WCA recommended SQL from above)   
***OPTIONAL***

NEW - Show the recommended SQL is indeed an improvement from the SQL using UNION  

---
You are a database administrator. Evaluate the output from the following sql query and query plan. Determine if the query plan contains UNION operators that will produce very large result sets. If the query plan contains UNION operators that will produce very large results set, please provide improvements to the SQL query and query plan that would not lead to very large results sets.

Expected Output:
- Determine if the query plan contains UNION operators that would produce a very large resluts set
- If the query plan contains UNION operators that will produce very large results set, please provide improvements to the SQL query and query plan that would not lead to very large results set.

Provide optimized alternatives if applicable.

Here is the query plan file @T-SQL-UNION-wca-change.xml