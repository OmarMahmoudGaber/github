SELECT
    order_id,
    order_date,
    customer_name,
    quantity,
    unit_price,
    (quantity * unit_price) AS total_revenue,
    region
FROM raw_sales_data 