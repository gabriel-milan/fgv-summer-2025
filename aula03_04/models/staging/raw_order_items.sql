select
    id as order_item_id,
    order_id,
    sku
from {{ source('publico_jaffle_shop', 'raw_order_items') }}
