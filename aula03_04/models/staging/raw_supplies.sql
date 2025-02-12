select sku as product_id, sum(round(cast((cost / 100) as numeric), 2)) as supply_cost
from {{ source('publico_jaffle_shop', 'raw_supplies') }}
group by sku
