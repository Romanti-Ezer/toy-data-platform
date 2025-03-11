{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

select * from {{source("raw","orders")}}

{% if is_incremental() %}

where
  updated_at > (select max(updated_at) from {{ this }})

{% endif %}