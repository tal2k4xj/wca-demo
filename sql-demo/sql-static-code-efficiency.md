# SQL Static Code Efficiency (BuildTime / Inspection)

### Scenarios
- [Inner Queries](#inner-queries-nested-subqueries)
    - [Variation: Nested Subquery in WHERE Clause](#variation-nested-subquery-in-where-clause)
    - [Variation: Nested Subquery in SELECT Clause](#variation-nested-subquery-in-select-clause)
    - [Variation: Control - No subqueries but Multiple Selects](#variation-control---no-subqueries-but-multiple-selects)
- [Use merge instead of update (or insert, or delete)](#use-merge-instead-of-update-or-insert-or-delete)
- [Cartesion Join on Queries](#cartesian-join-on-queries)
    - [Variation: Implicit Cross-Join](#variation-implicit-cross-join)
    - [Variation: Control](#variation-control)
- [More than 3 or 4 Joins in a Query](#more-than-3-or-4-joins-in-a-query)
    - [Variation: Temp Table: 6 join statements and complex schema](#variation-temp-table-6-join-statements-and-complex-schema)
    - [Variation: Redundant Inner Join](#variation-redundant-inner-join)
    - [Variation: Control](#variation-control-1)
- [Set limit on select (no limit clause or limit set too high)](#set-limit-on-select-no-limit-clause-or-limit-set-too-high)



## Inner Queries (Nested Subqueries)

*This does: Analyzes a query to determine if nested subqueries exist and offers solutions to avoid them  
This uses: An SQL query  
This varies by: Differentiates between Subqueries and Nested subqueries, identifying if a subquery is within a subquery*

### Variation: Nested Subquery in WHERE clause  
---
Analyze the following SQL query to ensure it does not contain nested subqueries (subqueries within the SELECT, FROM, WHERE, or HAVING clauses). If nested subqueries exist, suggest optimized alternatives using JOINs, Common Table Expressions (CTEs), or temporary tables to improve readability and performance.

Key Requirements:
Detection: Identify all nested subqueries and label their type (e.g., scalar, inline view, or correlated).
Optimization: Rewrite the query to eliminate nesting while maintaining the same logic. Prefer:
- JOINs for merging tables.
- CTEs (WITH clauses) for breaking down complexity.
- Window functions (if applicable) for row-by-row calculations.
Explanation: Briefly justify why the rewritten query is more efficient (e.g., reduced execution plan complexity, better indexing).

Query:
```
SELECT employee_name, salary  
FROM employees e  
WHERE salary > (SELECT AVG(salary) FROM employees WHERE department_id = e.department_id);
```


### Variation: Nested Subquery in SELECT clause
---
Analyze the following SQL query to ensure it does not contain nested subqueries (subqueries within the SELECT, FROM, WHERE, or HAVING clauses). If nested subqueries exist, suggest optimized alternatives using JOINs, Common Table Expressions (CTEs), or temporary tables to improve readability and performance.

Key Requirements:
Detection: Identify all nested subqueries and label their type (e.g., scalar, inline view, or correlated).

Optimization: Rewrite the query to eliminate nesting while maintaining the same logic. Prefer:
- JOINs for merging tables.
- CTEs (WITH clauses) for breaking down complexity.
- Window functions (if applicable) for row-by-row calculations.

Explanation: Briefly justify why the rewritten query is more efficient (e.g., reduced execution plan complexity, better indexing).

Query:
```
SELECT 
   order_id,  
   (SELECT customer_name FROM customers c WHERE c.customer_id = o.customer_id) AS customer  
FROM orders o;
```

### Variation: Control - No subqueries but Multiple Selects
---
Analyze the following SQL query to ensure it does not contain nested subqueries (subqueries within the SELECT, FROM, WHERE, or HAVING clauses). If nested subqueries exist, suggest optimized alternatives using JOINs, Common Table Expressions (CTEs), or temporary tables to improve readability and performance.

Key Requirements:
Detection: Identify all nested subqueries and label their type (e.g., scalar, inline view, or correlated).

Optimization: Rewrite the query to eliminate nesting while maintaining the same logic. Prefer:
- JOINs for merging tables.
- CTEs (WITH clauses) for breaking down complexity.
- Window functions (if applicable) for row-by-row calculations.

Explanation: Briefly justify why the rewritten query is more efficient (e.g., reduced execution plan complexity, better indexing).

Query:
```
WITH dept_avg AS 
(SELECT department_id, AVG(salary) AS avg_salary 
FROM employees GROUP BY department_id ) 
SELECT e.employee_name, e.salary 
FROM employees e JOIN dept_avg d 
ON e.department_id = d.department_id 
WHERE e.salary > d.avg_salary;
```
## Use merge instead of update (or insert, or delete)

*This does: Analyzes a query for Atomicity and Thread-Safety by determining if it meets the criteria for the UPSERT antipattern, and offers suggestions for refactoring.  
This uses: An SQL query  
This varies by: Insert, Delete, etc.*

Many checks together: 
Variation: Control Update  
Variation: Update&Insert  
Variation: Update&Delete  
Variation: Conditional Update/Insert  

---
You are reviewing queries to identify any anti-patterns. Analyze the following SQL Server queries for atomicity and thread-safety issues, specifically any UPDATE/INSERT/DELETE anti-patterns that should be replaced with MERGE, and explain the risks. 

For each query:

Identify anti-patterns - If there is evidence of any UPDATE/INSERT/DELETE anti-patterns that should be replaced with a MERGE, answer Yes and return the anti-pattern. Otherwise, answer No. 

Risk Explanation - If there is evidence of any UPDATE/INSERT/DELETE anti-patterns that should be replaced with a MERGE, explain the risks of those patterns. 

Provide Corrected Query - If there is evidence of any UPDATE/INSERT/DELETE anti-patterns that should be replaced with a MERGE, provide a formatted version of the query that would not have an anti-pattern and would be optimized

Query 1: 
```
UPDATE products SET price = price * 1.10, last_updated = GETDATE() 
WHERE category_id = 5 AND discontinued = 0;
```

Query 2: 
```
IF EXISTS (SELECT 1 FROM orders WHERE order_id = 100) 
BEGIN 
UPDATE orders SET status = 'Shipped', last_updated = GETDATE() 
WHERE order_id = 100; 
END 
ELSE 
BEGIN 
INSERT INTO orders (order_id, status, created_date, last_updated) VALUES (100, 'Shipped', GETDATE(), GETDATE()); 
END
```

Query 3: 
```
UPDATE users SET status = 'Archived' last_login < DATEADD(year, -1, GETDATE()); 
DELETE FROM users 
WHERE status = 'Unverified' AND last_login IS NULL;
```

Query 4: 
```
IF (SELECT COUNT(*) FROM inventory WHERE product_id = 500 AND warehouse_id = 1) > 0 
BEGIN 
UPDATE inventory 
SET quantity = quantity + 10 
WHERE product_id = 500 AND warehouse_id = 1; END 
ELSE BEGIN 
INSERT INTO inventory (product_id, warehouse_id, quantity) VALUES (500, 1, 10); 
END
```

## Cartesian join on queries

*This does: Analyzes a query to determine if the SQL can produce a cartesian product and recommends how to refactor to avoid this.  
This uses: An SQL query  
This varies by: Various Causes of a Cartesian Product*

### Variation: Implicit Cross-Join

---
Analyze the following SQL query to determine if it is generating a Cartesian product (unintentional cross join). A Cartesian product occurs when tables are joined without proper join conditions, resulting in every row from one table being matched with every row from another.

For Each Query:

Examine all JOIN clauses – Ensure each JOIN has an explicit and correct ON or USING condition.
Check for implicit cross joins – Detect if tables are listed in the FROM clause without proper join conditions.
Verify WHERE clause filters – Ensure that conditions in the WHERE clause are not accidentally replacing proper JOIN logic.
Evaluate subqueries and derived tables – Confirm that subqueries or CTEs are correctly joined to the main query.
Assess query logic – If a Cartesian product is intentional (rare), highlight it and suggest whether it’s necessary.

Expected Output:
Flag any potential Cartesian products with an explanation.
Suggest fixes (e.g., adding missing join conditions).
Estimate the impact (e.g., "This would multiply 1000 rows × 500 rows = 500,000 rows").

Provide optimized alternatives if applicable.

Please analyze my query step by step and provide actionable feedback:
```
SELECT e.employee_name, d.department_nameFROM employees e, departments d
WHERE e.salary > 50000;
```

### Variation: Control
---
Analyze the following SQL query to determine if it is generating a Cartesian product (unintentional cross join). A Cartesian product occurs when tables are joined without proper join conditions, resulting in every row from one table being matched with every row from another.

For Each Query:

Examine all JOIN clauses – Ensure each JOIN has an explicit and correct ON or USING condition.

Check for implicit cross joins – Detect if tables are listed in the FROM clause without proper join conditions.

Verify WHERE clause filters – Ensure that conditions in the WHERE clause are not accidentally replacing proper JOIN logic.

Evaluate subqueries and derived tables – Confirm that subqueries or CTEs are correctly joined to the main query.

Assess query logic – If a Cartesian product is intentional (rare), highlight it and suggest whether it’s necessary.

Expected Output:

- Flag any potential Cartesian products with an explanation.
- Suggest fixes (e.g., adding missing join conditions).
- Estimate the impact (e.g., "This would multiply 1000 rows × 500 rows = 500,000 rows").
- Provide optimized alternatives if applicable.

Please analyze my query step by step and provide actionable feedback:
```
SELECT 
    d.department_name,
    COUNT(e.employee_id) AS employee_count,
    AVG(e.salary) AS avg_salary,
    MAX(p.project_budget) AS max_project_budget
FROM departments d
JOIN employees e ON d.department_id = e.department_id
LEFT JOIN projects p ON e.employee_id = p.lead_employee_id
WHERE d.location = 'New York'
GROUP BY d.department_name
HAVING COUNT(e.employee_id) > 5
ORDER BY avg_salary DESC;
```

## More than 3 or 4 Joins in a Query

*This does: Analyzes a query to determine if the current number of JOINs it too expensive and offers solutions to better optimize  
This uses: An SQL query  
This varies by: The number of JOINS present and whether a refactored solution is straightforward without heavy database modification*

## Variation: Temp Table: 6 join statements and complex schema

Analyze the following SQL query and provide a detailed review with a focus on JOIN operations. Specifically, check if the query contains more than 4 JOIN statements (including INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN, etc.), as this could impact performance.

For each JOIN in the query:
- Identify the type of JOIN used and the tables involved.
- Assess whether the JOIN is necessary or if the query could be optimized (e.g., by restructuring, using subqueries, or denormalizing certain tables).
- Flag any potential performance risks (e.g., missing indexes, Cartesian products, or overly complex joins).

If the query exceeds 4 JOINs:
- Provide an optimized and version of the query (e.g., breaking into smaller queries, using temporary tables, or revisiting the schema design). Please provide an explanation for the optimized version. 
- Highlight whether any redundant or duplicate JOINs exist.

Please analyze my query step by step and provide actionable feedback:
```
SELECT s.sale_id, c.customer_name, p.product_name, e.employee_name, st.store_name, r.region_name, pm.payment_method 
FROM sales s 
INNER JOIN customers c ON s.customer_id = c.customer_id 
INNER JOIN products p ON s.product_id = p.product_id 
INNER JOIN employees e ON s.employee_id = e.employee_id 
INNER JOIN stores st ON s.store_id = st.store_id 
INNER JOIN regions r ON st.region_id = r.region_id 
LEFT JOIN payment_methods pm ON s.payment_id = pm.payment_id;
```

### Variation: Redundant Inner Join
---
Analyze the following SQL query and provide a detailed review with a focus on JOIN operations. Specifically, check if the query contains more than 4 JOIN statements (including INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN, etc.), as this could impact performance.

For each JOIN in the query:
- Identify the type of JOIN used and the tables involved.
- Assess whether the JOIN is necessary or if the query could be optimized (e.g., by restructuring, using subqueries, or denormalizing certain tables).
- Flag any potential performance risks (e.g., missing indexes, Cartesian products, or overly complex joins).

If the query exceeds 4 JOINs:

- Provide an optimized and version of the query (e.g., breaking into smaller queries, using temporary tables, or revisiting the schema design). Please provide an explanation for the optimized version. 
- Highlight whether any redundant or duplicate JOINs exist.

Please analyze my query step by step and provide actionable feedback:
```
SELECT u.user_id, u.username, p.post_title, c.comment_text, u2.username AS commenter_name  
FROM users u INNER JOIN posts p ON u.user_id = p.user_id  
INNER JOIN comments c ON p.post_id = c.post_id  
INNER JOIN users u2 ON c.user_id = u2.user_id -- Joining 'users' again!  
WHERE p.post_date > '2023-06-01'; 
```

### Variation: Control
---
Analyze the following SQL query and provide a detailed review with a focus on JOIN operations. Specifically, check if the query contains more than 4 JOIN statements (including INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN, etc.), as this could impact performance.

For each JOIN in the query:

- Identify the type of JOIN used and the tables involved.
- Assess whether the JOIN is necessary or if the query could be optimized (e.g., by restructuring, using subqueries, or denormalizing certain tables).
- Flag any potential performance risks (e.g., missing indexes, Cartesian products, or overly complex joins).
If the query exceeds 4 JOINs:
- Provide an optimized version of the query (e.g., breaking into smaller queries, using temporary tables, or revisiting the schema design).
- Highlight whether any redundant or duplicate JOINs exist.

Please analyze my query step by step and provide actionable feedback:
```
SELECT o.order_id, c.customer_name, p.product_name, oi.quantity 
FROM orders o 
INNER JOIN customers c ON o.customer_id = c.customer_id 
INNER JOIN order_items oi ON o.order_id = oi.order_id 
INNER JOIN products p ON oi.product_id = p.product_id 
WHERE o.order_date > '2023-01-01';
```

## Set limit on select (no limit clause or limit set too high)

*This does: Analyzes a query to determine if the SELECT statement is too expensive and offers guidance on setting reasonable limits.
This uses: An SQL query
This varies by:  Whether LIMIT is set at all or if LIMIT is set too high to be effective*

Many checks together (first is “Control”):
Query 1: Control (good, low limit)
Query 2: Missing Limit
Query 3: Limit was Too High

---

Analyze the following SQL queries to determine if they include a proper row-limiting mechanism (e.g., LIMIT, TOP, FETCH FIRST, ROWNUM, etc.) to prevent excessively-large result sets. 

For each query:

Identify row limit - Identify whether a row-limiting clause is presI ent.

Missing Limit - If no limit is found, provide an optimized version of the query with an appropriate limiting mechanism. Provide and explanation for the corrected query. 

High Limit - If a limit exists but is greater than 1000 rows, return a 'High Limit' flag and provide a recommendation on how to review the limit for performance impact. 

Additional Notes - Note any edge cases, such as queries with WHERE conditions that inherently restrict results or queries used in subqueries/CTEs where limiting may not be necessary.

Query 1: 
```
WITH recent_orders AS (
    SELECT * 
    FROM orders 
    ORDER BY created_at DESC
) 
SELECT TOP 100 * 
FROM recent_orders;
```

Query 2: 
```
SELECT * FROM users;
```
Query 3: 
```
SELECT TOP 5000 id, name 
FROM products 
WHERE price > 100;
```