{{ config(materialized="table", alias="orders_monolito", schema="123456789") }}

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
from
    (
        -- Base orders
        select
            id as order_id,
            store_id as location_id,
            customer as customer_id,
            subtotal as subtotal_cents,
            tax_paid as tax_paid_cents,
            order_total as order_total_cents,

            round(cast((subtotal / 100) as numeric), 2) as subtotal,

            round(cast((tax_paid / 100) as numeric), 2) as tax_paid,

            round(cast((order_total / 100) as numeric), 2) as order_total,

            timestamp_trunc(cast(ordered_at as timestamp), day) as ordered_at

        from `emap-summer-2025`.`publico_jaffle_shop`.`raw_orders`
    ) as base_orders
left join
    (
        -- Order items summary
        select
            order_id,
            sum(supply_cost) as order_cost,
            sum(product_price) as order_items_subtotal,
            count(order_item_id) as count_order_items,
            sum(case when is_food_item then 1 else 0 end) as count_food_items,
            sum(case when is_drink_item then 1 else 0 end) as count_drink_items
        from
            (
                select
                    oi.id as order_item_id,
                    oi.order_id,
                    p.product_price,
                    p.is_food_item,
                    p.is_drink_item,
                    s.supply_cost
                from `emap-summer-2025`.`publico_jaffle_shop`.`raw_order_items` oi
                left join
                    (
                        -- Products
                        select
                            sku as product_id,

                            round(cast((price / 100) as numeric), 2) as product_price,
                            type = 'jaffle' as is_food_item,
                            type = 'beverage' as is_drink_item
                        from `emap-summer-2025`.`publico_jaffle_shop`.`raw_products`
                    ) p
                    on oi.sku = p.product_id
                left join
                    (
                        -- Supplies summary
                        select
                            sku as product_id,
                            sum(round(cast((cost / 100) as numeric), 2)) as supply_cost
                        from `emap-summer-2025`.`publico_jaffle_shop`.`raw_supplies`
                        group by sku
                    ) s
                    on oi.sku = s.product_id
            ) order_items_detail
        group by order_id
    ) order_items_summary
    on base_orders.order_id = order_items_summary.order_id
