WITH source AS (
    SELECT
        show_id,
        type,
        LOWER(TRIM(title)) as title,
        director,
        country,
        TRY_CAST(date_added AS DATE) AS date_added,
        release_year,
        rating,
        duration,
        listed_in,
        "description",
        "cast"
    FROM {{ source('raw', 'netflix_titles') }}
)

SELECT * FROM source