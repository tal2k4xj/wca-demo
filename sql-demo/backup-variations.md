# BACKUP / VARIATIONS

## More than 3 or 4 Joins in a Query

### Variation: Implicit Cross-Join
--- 
Analyze the following SQL query to determine if it is generating a Cartesian product (unintentional cross join). A Cartesian product occurs when tables are joined without proper join conditions, resulting in every row from one table being matched with every row from another.

For Each Query:

- Examine all JOIN clauses – Ensure each JOIN has an explicit and correct ON or USING condition.
- Check for implicit cross joins – Detect if tables are listed in the FROM clause without proper join conditions.
- Verify WHERE clause filters – Ensure that conditions in the WHERE clause are not accidentally replacing proper JOIN logic.
- Evaluate subqueries and derived tables – Confirm that subqueries or CTEs are correctly joined to the main query.
- Assess query logic – If a Cartesian product is intentional (rare), highlight it and suggest whether it’s necessary.

Expected Output:

- Flag any potential Cartesian products with an explanation.
- Suggest fixes (e.g., adding missing join conditions).
- Estimate the impact (e.g., "This would multiply 1000 rows × 500 rows = 500,000 rows").

Provide optimized alternatives if applicable.

Please analyze my query step by step and provide actionable feedback:
```
SELECT *FROM orders, customers
WHERE orders.order_date > '2023-01-01';
```

### Assess Postgres query plans for efficiency

*This does: Assesses the efficiency of a SQL Query Plan   
This uses: Query Plan output  
This varies by:  The efficiency of a query plan.  *

### Variation: Very Inefficient Query (sorting, merging, indexes, full-text searching)
--- 
You are a developer examining the output of a sql query plan. Evaluate this SQL query plan to determine if it is efficient for executing the intended queries. If the SQL query plan is not efficient, please provide suggestions for improving its efficiency.

For Each SQL Query Plan:

- Return Step by Step Analysis - Analyze the SQL query plan and provide a step by step explanation 
- Determine Query Plan Efficiency – Examine the SQL Query Plan and determine if this SQL query plan is efficient or inefficient for executing the intended queries. 
- Highlight Inefficiencies - If the SQL query plan is inefficient, explain each part that is inefficient 
- Provide efficient query plan - If the SQL query plan is inefficient, provide formatted examples to improve the efficiency of the plan’s steps
- Provide general suggestions - In addition to any examples to improve the sql query plan, provide general suggestions to improve the query’s performance

Expected Output:

- Provide a step by step explanation of the SQL query plan
- Determine if they SQL query plan is efficient or inefficient for executing the intended queries. 
- Highlight and explain the specific inefficiencies.
- Provide efficient query plan.
- Provide general suggestions for improving the query’s performance. 

Please analyze the SQL query plan step by step and provide actionable feedback:
```
"Limit  (cost=197282.90..197283.48 rows=5 width=124)"
"  ->  Gather Merge  (cost=197282.90..200252.97 rows=25456 width=124)"
"        Workers Planned: 2"
"        ->  Sort  (cost=196282.88..196314.70 rows=12728 width=124)"
"              Sort Key: ranking, population DESC NULLS LAST, density DESC NULLS LAST"
"              ->  Parallel Seq Scan on city_search  (cost=0.00..196071.47 rows=12728 width=124)"
"                    Filter: (to_tsvector('english'::regconfig, display_name) @@ '''leander'':*'::tsquery)"
"JIT:"
"  Functions: 3"
"  Options: Inlining false, Optimization false, Expressions true, Deforming true"
```

### Variation: Control - Efficient Query
---
You are a developer examining the output of a sql query plan. Evaluate this SQL query plan to determine if it is efficient for executing the intended queries. If the SQL query plan is not efficient, please provide suggestions for improving its efficiency.

For Each SQL Query Plan:

- Return Step by Step Analysis - Analyze the SQL query plan and provide a step by step explanation 
- Determine Query Plan Efficiency – Examine the SQL Query Plan and determine if this SQL query plan is efficient or inefficient for executing the intended queries. 
- Highlight Inefficiencies - If the SQL query plan is inefficient, explain each part that is inefficient 
- Provide efficient query plan - If the SQL query plan is inefficient, provide formatted examples to improve the efficiency of the plan’s steps

Provide general suggestions - In addition to any examples to improve the sql query plan, provide general suggestions to improve the query’s performance

Expected Output:

Provide a step by step explanation of the SQL query plan
Determine if they SQL query plan is efficient or inefficient for executing the intended queries. 

Highlight and explain the specific inefficiencies.
Provide efficient query plan.
Provide general suggestions for improving the query’s performance. 

Please analyze the SQL query plan step by step and provide actionable feedback:
```
"Limit  (cost=143.14..143.14 rows=1 width=59)"
"  ->  Sort  (cost=143.14..143.14 rows=1 width=59)"
"        Sort Key: ranking, population DESC NULLS LAST, density DESC NULLS LAST"
"        ->  Bitmap Heap Scan on city_search ""CitySearch""  (cost=139.11..143.13 rows=1 width=59)"
"              Recheck Cond: ((tokens @@ '''leander'':*'::tsquery) AND (display_name ~~* 'leander%'::text))"
"              ->  BitmapAnd  (cost=139.11..139.11 rows=1 width=0)"
"                    ->  Bitmap Index Scan on ix_city_search_tokens  (cost=0.00..29.72 rows=229 width=0)"
"                          Index Cond: (tokens @@ '''leander'':*'::tsquery)"
"                    ->  Bitmap Index Scan on ix_city_search_display_name  (cost=0.00..109.15 rows=153 width=0)"
"                          Index Cond: (display_name ~~* 'leander%'::text)"
```

### Variation:  Union with Large result set
---
You are a database administrator. Evaluate the output from the following sql query and query plan. Determine if the query plan contains UNION operators that will produce  very large result sets. If the query plan contains UNION operators that will produce very large results set, please provide improvements to the SQL query and query plan that would not lead to very large results sets.

Expected Output:

Determine if the query plan contains UNION operators that would produce a very large resluts set

If the query plan contains UNION operators that will produce very large results set, please provide improvements to the SQL query and query plan that would not lead to very large results set.

Provide optimized alternatives if applicable.
```
select city.id as id, city.name || ', ' || country_division.name || ', ' || country.name AS display_name,
ranking,
population,
density,
to_tsvector('simple', city.name || ', ' || country_division.name || ', ' || country.name) AS tokens
from city
INNER JOIN country ON city.iso3 = country.iso3
INNER JOIN country_division ON city.division_id = country_division.id
where show_division = true and country_division.name is not null
UNION
select city.id as id, city.name || ', ' || country.name AS display_name,
ranking,
population,
density,
to_tsvector('simple', city.name || ', ' || country.name) AS tokens
from city
INNER JOIN country ON city.iso3 = country.iso3
where show_division = true and city.division_id is null
UNION
select city.id as id, city.name || ', ' || country.name AS display_name,
ranking,
population,
density,
to_tsvector('simple', city.name || ', ' || country.name) AS tokens
from city
INNER JOIN country ON city.iso3 = country.iso3
where show_division is null or show_division = false

"Unique (cost=913583.53..946783.08 rows=1897117 width=92)"
" -> Sort (cost=913583.53..918326.32 rows=1897117 width=92)"
" Sort Key: city.id, ((((((city.name)::text || ', '::text) || (country_division.name)::text) || ', '::text) || (country.name)::text)), city.ranking, city.population, city.density, (to_tsvector('simple'::regconfig, (((((city.name)::text || ', '::text) || (country_division.name)::text) || ', '::text) || (country.name)::text)))"
" -> Gather (cost=1006.64..521228.08 rows=1897117 width=92)"" Workers Planned: 2"
" -> Parallel Append (cost=6.64..330516.38 rows=1897117 width=92)"
" -> Hash Join (cost=129.45..132967.20 rows=368322 width=92)"
" Hash Cond: ((city.division_id)::text = (country_division.id)::text)"
" -> Hash Join (cost=6.38..32429.38 rows=368322 width=56)"
" Hash Cond: (city.iso3 = (country.iso3)::bpchar)"
" -> Parallel Seq Scan on city (cost=0.00..26353.21 rows=636421 width=49)"" -> Hash (cost=4.54..4.54 rows=147 width=15)"
" -> Seq Scan on country (cost=0.00..4.54 rows=147 width=15)"
" Filter: show_division"" -> Hash (cost=69.70..69.70 rows=4270 width=16)"" -> Seq Scan on country_division (cost=0.00..69.70 rows=4270 width=16)"
" Filter: (name IS NOT NULL)"
" -> Hash Join (cost=6.64..142400.23 rows=420940 width=92)"
" Hash Cond: (city_1.iso3 = (country_1.iso3)::bpchar)"
" -> Parallel Seq Scan on city city_1 (cost=0.00..26353.21 rows=636421 width=43)"
" -> Hash (cost=4.54..4.54 rows=168 width=15)"
" -> Seq Scan on country country_1 (cost=0.00..4.54 rows=168 width=15)"
" Filter: ((show_division IS NULL) OR (NOT show_division))"
" -> Hash Join (cost=6.38..26692.19 rows=1203 width=92)"
" Hash Cond: (city_2.iso3 = (country_2.iso3)::bpchar)"
" -> Parallel Seq Scan on city city_2 (cost=0.00..26353.21 rows=2079 width=43)"
" Filter: (division_id IS NULL)"
" -> Hash (cost=4.54..4.54 rows=147 width=15)"
" -> Seq Scan on country country_2 (cost=0.00..4.54 rows=147 width=15)"
" Filter: show_division"
"JIT:"
" Functions: 49"
" Options: Inlining true, Optimization true, Expressions true, Deforming true"
```

### Variation:  Control - no unions (but could be made more efficient)
---

You are a database administrator. Evaluate the output from the following sql query and query plan. Determine if the query plan contains UNION operators that will produce  very large result sets. If the query plan contains UNION operators that will produce very large results set, please provide improvements to the SQL query and query plan that would not lead to very large results sets.

Expected Output:

Determine if the query plan contains UNION operators that would produce a very large resluts set

If the query plan contains UNION operators that will produce very large results set, please provide improvements to the SQL query and query plan that would not lead to very large results set.

Provide optimized alternatives if applicable.
```
select city.id as id, city.name || ', ' || country_division.name || ', ' || country.name AS display_name,
ranking,
population,
density,
to_tsvector('simple', city.name || ', ' || country_division.name || ', ' || country.name) AS tokens
from city
INNER JOIN country ON city.iso3 = country.iso3
INNER JOIN country_division ON city.division_id = country_division.id
where show_division = true and country_division.name is not null;

" Workers Planned: 2"
" -> Hash Join (cost=129.45..132967.20 rows=368322 width=92)"
" Hash Cond: ((city.division_id)::text = (country_division.id)::text)"
" -> Hash Join (cost=6.38..32429.38 rows=368322 width=56)"
" Hash Cond: (city.iso3 = (country.iso3)::bpchar)"
" -> Parallel Seq Scan on city (cost=0.00..26353.21 rows=636421 width=49)"
" -> Hash (cost=4.54..4.54 rows=147 width=15)"
" -> Seq Scan on country (cost=0.00..4.54 rows=147 width=15)"
" Filter: show_division"" -> Hash (cost=69.70..69.70 rows=4270 width=16)"
" -> Seq Scan on country_division (cost=0.00..69.70 rows=4270 width=16)"" Filter: (name IS NOT NULL)"
"JIT:"
" Functions: 22"
" Options: Inlining false, Optimization false, Expressions true, Deforming true"
```

## Quality/portability of SQL (IBM initial recommendation)

Database specific SQL (portability and maintainability, e.g. Is the following SQL compatible with Postgres)

*This does: Examines a query to determine if it is compatible for a given database platform  
This uses: An SQL query  
This varies by: TSQL, Postgresql, MySQL, Agnostic*

### Variation: Control
---
Answer yes or no. Is the following valid T-SQL?  If not, re-write for T-SQL.
```
SELECT TOP 10 (*) FROM users ORDER BY age;
```

### Variation: MySQL
---
Answer yes or no. Is the following valid for a MySQL database?  If not, re-write for MySQL.
```
SELECT TOP 10 (*) FROM users ORDER BY age;
```

### Variation: Postgres
---
Answer yes or no. Is the following valid postgresql?  If not, re-write for postgresql.,
```
SELECT TOP 10 (*) FROM users ORDER BY age;
```

## Non-compliant stored procedure (how well written)

### Variation: Control (well-written)
---
Evaluate the attached DDL to determine if it is well-written. Answer with "Yes" or "No" and provide specific reasons for your evaluation based on:

Clarity in Intent: Does the stored procedure achieve its intended purpose effectively?  
Variable Names: Are variable names clear and descriptive, enhancing code readability?  
Readability and Structure: Is the SQL code easy to read with proper indentation, comments, and logical grouping of operations?  
Parameter Types and Usage: Are parameters correctly defined and used appropriately in queries and logic?  
Documentation: Does the procedure include a comprehensive docblock explaining its role in the application?  
Error Handling: Does the stored procedure handle potential errors gracefully without causing database crashes or application failures?  
Input Validation: Are inputs validated to meet expected formats, data types, or constraints?  
Logic Flow: Is the control flow clear and intuitive, avoiding unnecessary complexity or hard-to-follow logic patterns?  
Compliance with Standards: Does the stored procedure adhere to SQL Server best practices regarding efficiency, scalability, and maintainability?  

Provide a "Yes" answer if all aspects are well-written, explaining why it is correct. Provide a "No" answer if there are issues, detailing the reasons.
```
-- Function to capture order changes in a history table 
CREATE OR REPLACE FUNCTION capture_order_changes()

RETURNS TRIGGER AS $$
DECLARE 
    v_operation text;
    v_old_order_data json;
    v_new_order_data json;

BEGIN
    -- Determine the operation type (INSERT, UPDATE, DELETE) v_operation := TG_OP;
    -- Store old order data in JSON format v_old_order_data := row_to_json(OLD);
    -- Store new order data in JSON format if applicable 
    IF v_operation = 'INSERT' THEN 
        v_new_order_data := row_to_json(NEW); 
    ELSIF v_operation = 'UPDATE' THEN 
        v_new_order_data := row_to_json(NEW); 
    END IF;
    -- Insert a record into the order_history table for each order change
    -- The operation column indicates whether the change was an insert, update, or delete 
    -- The old_value column stores the previous state of the order for update and delete operations
    -- The new_value column stores the new state of the order for insert operations 
    IF v_operation = 'DELETE' THEN 
        INSERT INTO order_history (order_id, customer_id, operation, old_value) VALUES (OLD.order_id, OLD.customer_id, v_operation, v_old_order_data);
    ELSIF v_operation = 'UPDATE' THEN 
        INSERT INTO order_history (order_id, customer_id, operation, old_value, new_value) VALUES (OLD.order_id, OLD.customer_id, v_operation, v_old_order_data, v_new_order_data);
    ELSIF v_operation = 'INSERT' THEN 
        INSERT INTO order_history (order_id, customer_id, operation, new_value) VALUES (NEW.order_id, NEW.customer_id, v_operation, v_new_order_data);
    END IF;
    -- Return NULL to indicate that the trigger has executed successfully RETURN NULL; EXCEPTION
    -- Handle any errors that may occur during execution 
    WHEN OTHERS THEN 
        RAISE NOTICE 'An error occurred in the capture_order_changes trigger: %', SQLERRM;
    RETURN NULL;
 END;
 $$ LANGUAGE plpgsql;
 ```

### Variation: DDL is not well-written (requires dedicated chat session)
--- 
Evaluate the attached DDL to determine if it is well-written. Answer with "Yes" or "No" and provide specific reasons for your evaluation based on:

Clarity in Intent: Does the stored procedure achieve its intended purpose effectively?  
Variable Names: Are variable names clear and descriptive, enhancing code readability?  
Readability and Structure: Is the SQL code easy to read with proper indentation, comments, and logical grouping of operations?  
Parameter Types and Usage: Are parameters correctly defined and used appropriately in queries and logic?  
Documentation: Does the procedure include a comprehensive docblock explaining its role in the application?  
Error Handling: Does the stored procedure handle potential errors gracefully without causing database crashes or application failures?  
Input Validation: Are inputs validated to meet expected formats, data types, or constraints?  
Logic Flow: Is the control flow clear and intuitive, avoiding unnecessary complexity or hard-to-follow logic patterns?  
Compliance with Standards: Does the stored procedure adhere to SQL Server best practices regarding efficiency, scalability, and maintainability?  

Provide a "Yes" answer if all aspects are well-written, explaining why it is correct. Provide a "No" answer if there are issues, detailing the reasons.
```
SET SERVEROUTPUT ON
DECLARE 
  result PLS_INTEGER := 0;
  counter PLS_INTEGER := 1;
BEGIN
  <>  
  result := result + counter;
  counter := counter + 1;
  IF counter <= 9 THEN
    GOTO loop;
  END IF;
  DBMS_OUTPUT.PUT_LINE('Sum from 1 to 9 is ' || result); -- Displays 1 + 2 + ... + 8 + 9 = 45
END;
```

## SQL ***and*** either the code or schema

## Uses Schema: Use of proper foreign keys

*This does:  Provides advice, generates DDL for creating foreign keys  
This uses: Schema file in the local file system  
This varies by: Whether you look at the query against the schema, or just the schemaLimitations: Don’t ask for missing foreign keys.*

### Variation: Finds foreign key violation

using @schema.sql as reference, what tables could cause have a foreign key constraint violation?
```
 delete from country where iso3='USA';
```

### Variation: Recommends updates to the schema
---
using @Schema.sql as reference, should I add a foreign key to in the city table referencing the country table? 

## Uses Code: Avoid changing session variables 

*This does:  We will identify session variables in stored procedures and detect if the value(s) of those session variables are changed.  
This uses: we use a simple prompt to do a static code inspection on a code block containing a stored procedure  
This varies by: Session variable placement*

### Variation: session variable is found and is changed
---
You are a mysql developer, please review the following stored procedure. Identify only the session variables in the code and report only session variables that are changed in the stored procedure. Here is an example of a session variable @session_var. Your output will look look like this: "The session variable @session_var is changed because it is assigned to another value".
```
DELIMITER //
CREATE PROCEDURE `GenerateSalesReport`(IN start_date DATE,IN end_date DATE)BEGINSET @var1 := 0;
SELECT @totalSales := 0;
SELECT SUM(sales_amount) INTO @totalSales FROM sales;
SET @var1 := @totalSales*1.1;
SELECT @totalSales As total_sales;
END //
```

### Variation: Two session variables are found, and were used in the SP but one of them it was not changed
---
You are a mysql developer, please review the following stored procedure. Identify only the session variables in the code and report only session variables that are changed in the stored procedure. Here is an example of a session variable @session_var and. Your output will look look like this: "The session variable @session_var is changed because it is assigned to another value"

The following is the stored procedure:
```
DELIMITER //
CREATE PROCEDURE getCustomerLevel(
IN customerId int)
BEGINDECLARE testvar int;
SET testvar := @var1;
select creditLimit into credit_limit from customers where customerNumber = customerId;
IF credit_limit < 10000 THEN
    SET @customer_level = "Silver";
ELSEIF credit_limit >= 10000 AND credit_limit <= 50000 THEN
    SET @customer_level = "Gold";
ELSE
    SET @customer_level = "Diamond";
END IF;
END //
```

## Avoid begin(start) transaction

*This does:  We will identify if explicit transaction code block is properly constructed in a stored procedure.  
This uses: we use a simple prompt to do a static code inspection on a explicit transaction code block in a stored procedure  
This varies by: Code block construction*

### Variation: Control - No explicit transaction used in stored procedure; 

*Explicit transaction code in a stored procedure should commit changes and handle exceptions to rollback changes. If stored procedure ends without committing changes, it will leave the transaction hanging.*
---
As a mysql developer, analyze the following stored procedure.

Answer yes or no by check if explicit transaction is used in the stored procedure. 

If explicit transaction is used, answer yes or no with one sentence explanation for each of the following: 

1) if exceptions are handled
2) if transaction is rolled back when an exception is thrown
3) if transaction has a explicit commit; statement. If explicit transaction is not used, just answer no.

Example output should be like this "Explicit transaction control is not used in this stored procedure.", or "yes, the store procedure does not contain a commit statement.". Be brief and no need to make any suggestions. Here is the stored procedure code:
```
DELIMITER //
CREATE PROCEDURE `GenerateSalesReport`(IN start_date DATE,IN end_date DATE)
BEGIN 
SET @var1 := 0;
SELECT @totalSales := 0;
SELECT SUM(sales_amount) INTO @totalSales FROM sales;
SET @var1 := @totalSales*1.1;
SELECT @totalSales As total_sales;
END //
```

### Variation: Properly constructed TXN code block (with exception handling, commit and rollback)

*Explicit transaction code in a stored procedure should commit changes and handle exceptions to rollback changes. If stored procedure ends without committing changes, it will leave the transaction hanging.*

---
As a mysql developer, analyze the following stored procedure.

Answer yes or no by check if explicit transaction is used in the stored procedure. 
If explicit transaction is used, answer yes or no with one sentence explanation for each of the following: 

1) if exceptions are handled
2) if transaction is rolled back when an exception is thrown
3) if transaction has a explicit commit; statement. If explicit transaction is not used, just answer no.

Example output should be like this "Explicit transaction control is not used in this stored procedure.", or "yes, the store procedure does not contain a commit statement.". Be brief and no need to make any suggestions. Here is the stored procedure code:
```
DELIMITER //
CREATE PROCEDURE sp_delete_users_till_date(location_id INT, till_date DATE)
BEGIN
DECLARE track_no INT DEFAULT 0;
DECLARE EXIT HANDLER FOR SQLEXCEPTION, NOT FOUND, SQLWARNING
BEGIN
ROLLBACK;
GET DIAGNOSTICS CONDITION 1 @`errno` = MYSQL_ERRNO, @`sqlstate` = RETURNED_SQLSTATE, @`text` = MESSAGE_TEXT;
SET @full_error = CONCAT('ERROR ', @`errno`, ' (', @`sqlstate`, '): ', @`text`);
SELECT track_no, @full_error;
END;
START TRANSACTION;
SET FOREIGN_KEY_CHECKS = 0;
SET track_no = 1;
DELETE FROM users WHERE users.location_id = location_id AND DATE(users.created_at) <= till_date;
SET track_no = 2;
SET FOREIGN_KEY_CHECKS = 1;
SET track_no = 3;
SELECT track_no, 'Congrates!, successfully executed.';
COMMIT;
END; //
DELIMITER ;
```

### Variation: TXN Code Block - missing commit statement in the stored procedure

*Explicit transaction code in a stored procedure should commit changes and handle exceptions to rollback changes. If stored procedure ends without committing changes, it will leave the transaction hanging.*

---
As a mysql developer, analyze the following stored procedure.
Answer yes or no by check if explicit transaction is used in the stored procedure. 

If explicit transaction is used, answer yes or no with one sentence explanation for each of the following: 

1) if exceptions are handled
2) if transaction is rolled back when an exception is thrown
3) if transaction has a explicit commit; statement. If explicit transaction is not used, just answer no.

Example output should be like this "Explicit transaction control is not used in this stored procedure.", or "yes, the store procedure does not contain a commit statement.". Be brief and no need to make any suggestions. Here is the stored procedure code:
```
DELIMITER //
CREATE PROCEDURE sp_delete_users_till_date(location_id INT, till_date DATE)
BEGIN
DECLARE track_no INT DEFAULT 0;
DECLARE EXIT HANDLER FOR SQLEXCEPTION, NOT FOUND, SQLWARNING
BEGIN
ROLLBACK;
GET DIAGNOSTICS CONDITION 1 @`errno` = MYSQL_ERRNO, @`sqlstate` = RETURNED_SQLSTATE, @`text` = MESSAGE_TEXT;
SET @full_error = CONCAT('ERROR ', @`errno`, ' (', @`sqlstate`, '): ', @`text`);
SELECT track_no, @full_error;
END;
START TRANSACTION;
SET FOREIGN_KEY_CHECKS = 0;
SET track_no = 1;
DELETE FROM users WHERE users.location_id = location_id AND DATE(users.created_at) <= till_date;
SET track_no = 2;
SET FOREIGN_KEY_CHECKS = 1;
SET track_no = 3;
SELECT track_no, 'Congrates!, successfully executed.';
END; //
DELIMITER ;
```