with
    raw_orders as (select * from {{ ref("raw_orders") }}),

    order_items_detail as (select * from {{ ref("order_items_detail") }}),

    order_items_summary as (
        select
            order_id,
            sum(supply_cost) as order_cost,
            sum(product_price) as order_items_subtotal,
            count(order_item_id) as count_order_items,
            sum(case when is_food_item then 1 else 0 end) as count_food_items,
            sum(case when is_drink_item then 1 else 0 end) as count_drink_items
        from order_items_detail
        group by order_id
    )

select
    base_orders.*,
    order_items_summary.order_cost,
    order_items_summary.order_items_subtotal,
    order_items_summary.count_food_items,
    order_items_summary.count_drink_items,
    order_items_summary.count_order_items,
    order_items_summary.count_food_items > 0 as is_food_order,
    order_items_summary.count_drink_items > 0 as is_drink_order,
    row_number() over (
        partition by base_orders.customer_id order by base_orders.ordered_at asc
    ) as customer_order_number
from raw_orders as base_orders
left join order_items_summary
    on base_orders.order_id = order_items_summary.order_id
