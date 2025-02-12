
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

from {{ source('publico_jaffle_shop', 'raw_orders') }}
