with

    source as (select * from {{ source("publico_jaffle_shop", "raw_customers") }}),

    renamed as (

        select

            -- --------  ids
            id as customer_id,

            -- -------- text
            name as customer_name

        from source

    )

select *
from renamed
