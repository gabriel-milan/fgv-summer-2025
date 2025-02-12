-- testar se a soma do campo 'order_total' é igual entre as duas tabelas

with orders_monolito as (
    select * from `emap-summer-2025.123456789_dev.orders_monolito`
),

orders_refatorada as (
    select * from `emap-summer-2025.123456789_dev.orders`
),

orders_monolito_sum as (
    select sum(order_total) as orders_monolito_sum from orders_monolito
),

orders_refatorada_sum as (
    select sum(order_total) as orders_refatorada_sum from orders_refatorada
)

select 
    m.orders_monolito_sum,
    r.orders_refatorada_sum,
    m.orders_monolito_sum - r.orders_refatorada_sum as diff
from orders_monolito_sum as m
left join orders_refatorada_sum as r on 1 = 1
where m.orders_monolito_sum  != r.orders_refatorada_sum








