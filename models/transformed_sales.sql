SELECT
    order_id,
    CAST(order_date AS DATE) as clean_date,
    split_part(product_info, '|', 1) as category,
    split_part(product_info, '|', 2) as product,
    quantity,
    unit_price,
    (quantity * unit_price) as total_revenue,
    region
FROM raw_sales_data
WHERE status != 'cancelled'