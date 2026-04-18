import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

usa_employees = pd.read_sql("""
                            SELECT lastName, firstName, officeCode
                            FROM employees
                            JOIN offices
                              USING(officeCode)
                            WHERE country = "USA";
                            """, conn)

# the same query, but this time using a subquery
subquery_usa_employees = pd.read_sql("""
                                     SELECT lastName, firstName, officeCode
                                      FROM employees
                                     WHERE officeCode IN(
                                      SELECT officeCode
                                      FROM offices
                                      WHERE country = "USA")
                                     """, conn)

# finding all the employees from offices with at least 5 employees
# instinct: find all the offices with at least 5 employees, then get all the employees in those offices
at_least_5 = pd.read_sql("""
                         SELECT lastName, firstName, officeCode
                         FROM employees
                         WHERE officeCode IN(
                          SELECT officeCode
                          FROM offices
                          JOIN employees
                            USING(officeCode)
                          GROUP BY 1
                          HAVING COUNT(employeeNumber) >= 5);
                         """, conn)

# print(at_least_5)

# average number of individual customers' average payments:
averages = pd.read_sql("""
                       SELECT AVG(customerAvgPayment) AS averagePayment
                       FROM (
                        SELECT AVG(amount) AS customerAvgPayment
                        FROM payments
                        JOIN customers USING(customerNumber)
                        GROUP BY customerNumber);
                       """, conn)

# print(averages)

# running subqueries that reference keys using different names between different tables
# For example, you can use the employee number in the employees table and the matching sales rep employee number in the customers table.
# It is looking at customers in the USA and the employee who represents them, not employees in the USA.
using_keys = pd.read_sql("""
                         SELECT lastName, firstName, employeeNumber
                         FROM employees
                         WHERE employeeNumber IN (
                          SELECT salesRepEmployeeNumber
                          FROM customers
                          WHERE country = "USA");
                         """, conn)

print(using_keys)

conn.close()