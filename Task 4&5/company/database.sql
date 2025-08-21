SELECT 
    e.id AS employeeId,
    e.name AS employeeName,
    d.name AS departmentName,
    la.month,
    la.year,
    e.baseSalary,
    la.leaves,
    (e.baseSalary - (la.leaves * (e.baseSalary / 25))) AS payableSalary
FROM Employee e
JOIN Department d 
    ON e.departmentId = d.id
JOIN LeaveApplication la 
    ON e.id = la.employeeId;
