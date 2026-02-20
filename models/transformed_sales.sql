SELECT
    order_id,
    order_date,
    category,
    quantity,
    unit_price,
    (quantity * unit_price) AS total_revenue,
    UPPER(region) AS region_code
FROM raw_sales_data
WHERE status != 'cancelled'