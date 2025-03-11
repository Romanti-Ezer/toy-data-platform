with df as (

    SELECT
    n.show_id,
    n.type,
    n.title,
    n.director,
    n.country,
    n.date_added,
    n.release_year,
    n.duration,
    n.listed_in,
    n.description,
    m.rating,
    m.no_of_persons_voted,
    m.directed_by,
    m.written_by,
    m.genres,
    m.release_date
FROM {{ref("netflix_titles")}} n
INNER JOIN {{ref("meta_critic")}} m
    ON n.title = m.title 
    and m.rating is not null

)

select * from df