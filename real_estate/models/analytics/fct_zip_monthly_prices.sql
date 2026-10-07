select
    zipcode,
    date_trunc('month', sale_date)               as sale_month,
    count(*)                                     as num_sales,
    median(price)                                as median_price,
    avg(price / nullif(sqft_living, 0))          as avg_price_per_sqft
from {{ ref('stg_house_sales') }}
group by 1, 2
