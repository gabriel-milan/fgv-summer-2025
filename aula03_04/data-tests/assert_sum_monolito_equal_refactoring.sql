-- check if the sum of the monolito is equal to the refactoring

with monolito as (
    select * from {{ ref('monolito') }}
),

refactoring as (
    select * from {{ ref('refactoring') }}
)