-- Products
select
    sku as product_id,

    round(cast((price / 100) as numeric), 2) as product_price,
    type = 'jaffle' as is_food_item,
    type = 'beverage' as is_drink_item
from {{ source('publico_jaffle_shop', 'raw_products') }}
