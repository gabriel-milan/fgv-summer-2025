{{ config(materialized = "ephemeral", alias = "int_order_items_detail") }}

with
    raw_order_items as (select * from {{ ref("raw_order_items") }}),

    raw_products as (select * from {{ ref("raw_products") }}),

    raw_supplies as (select * from {{ ref("raw_supplies") }})

select
    oi.order_item_id,
    oi.order_id,
    p.product_price,
    p.is_food_item,
    p.is_drink_item,
    s.supply_cost
from raw_order_items oi
left join raw_products p on oi.sku = p.product_id
left join raw_supplies s on oi.sku = s.product_id
