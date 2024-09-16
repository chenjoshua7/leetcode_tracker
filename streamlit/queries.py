streak_query = f"""WITH ranked_data AS (
                        SELECT 
                            *,
                            LAG(CAST(date AS DATE), 1) OVER (ORDER BY date ASC) AS prev_date
                        FROM 
                            daily_problems
                    ),
                    streaks AS (
                        SELECT 
                            *,
                            CASE 
                                WHEN DATEDIFF(CAST(date AS DATE), prev_date) = 1 THEN 0
                                ELSE 1
                            END AS is_new_streak
                        FROM ranked_data
                    ),
                    streak_groups AS (
                        SELECT *,
                            SUM(is_new_streak) OVER (ORDER BY date DESC ROWS UNBOUNDED PRECEDING) AS streak_id
                        FROM streaks
                    )
                    SELECT 
                        streak_id,
                        MAX(date) AS end_date,
                        COUNT(*) AS streak_length
                    FROM 
                        streak_groups
                    GROUP BY 
                        streak_id
                    ORDER BY 
                        end_date DESC;
                    """
                  
streak_gpt_query = f"""WITH ranked_data AS (
                        SELECT 
                            *,
                            LAG(CAST(date AS DATE), 1) OVER (ORDER BY date ASC) AS prev_date
                        FROM 
                            daily_problems
                        WHERE gpt = 0  -- Filter to include only rows where gpt = 0
                    ),
                    streaks AS (
                        SELECT 
                            *,
                            CASE 
                                WHEN DATEDIFF(CAST(date AS DATE), prev_date) = 1 THEN 0
                                ELSE 1
                            END AS is_new_streak
                        FROM ranked_data
                    ),
                    streak_groups AS (
                        SELECT *,
                            SUM(is_new_streak) OVER (ORDER BY date DESC ROWS UNBOUNDED PRECEDING) AS streak_id
                        FROM streaks
                    )
                    SELECT 
                        streak_id,
                        MAX(date) AS end_date,
                        COUNT(*) AS streak_length
                    FROM 
                        streak_groups
                    GROUP BY 
                        streak_id
                    ORDER BY 
                        end_date DESC;
                    """