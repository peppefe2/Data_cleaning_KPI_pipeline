DROP VIEW IF EXISTS v_kpi_by_status;
CREATE VIEW v_kpi_by_status AS
SELECT
    status,
    COUNT(*) AS orders_count,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(AVG(amount), 2) AS avg_amount
FROM clean_orders
GROUP BY status
ORDER BY total_amount DESC;

DROP VIEW IF EXISTS v_kpi_by_customer;
CREATE VIEW v_kpi_by_customer AS
SELECT
    customer_name,
    COUNT(*) AS total_orders,
    COUNT(CASE WHEN status = 'paid' THEN 1 END) AS paid_orders,
    ROUND(SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END), 2) AS net_revenue
FROM clean_orders
GROUP BY customer_name
ORDER BY net_revenue DESC;
