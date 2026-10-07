with zip_medians as (
    select zipcode, median(price / nullif(sqft_living, 0)) as zip_median_ppsf
    from {{ ref('stg_house_sales') }}
    group by 1
)
select
    s.property_sale_id,
    s.zipcode,
    s.sale_date,
    s.price,
    s.sqft_living,
    s.price / nullif(s.sqft_living, 0)                           as price_per_sqft,
    z.zip_median_ppsf,
    (s.price / nullif(s.sqft_living, 0)) / z.zip_median_ppsf - 1 as pct_vs_zip_median
from {{ ref('stg_house_sales') }} s
join zip_medians z using (zipcode)
