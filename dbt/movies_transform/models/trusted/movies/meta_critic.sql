WITH source AS (
    SELECT
        {{normalize("title")}} as title,
        TRY_CAST(release_date AS DATE) AS release_date, 
        max(description) as description,
        max(rating) as rating,
        max(TRY_CAST(no_of_persons_voted AS BIGINT)) AS no_of_persons_voted, 
        max(directed_by) as directed_by,
        max(written_by) as written_by,
        max(duration) as duration,
        max(genres) as genres
    FROM {{ source('raw', 'meta_critic') }}  
    group by 1, 2
)

SELECT * FROM source