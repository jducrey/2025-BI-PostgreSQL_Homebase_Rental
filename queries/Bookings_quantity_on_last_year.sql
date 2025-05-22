SELECT DATE_TRUNC('month', start_date) AS month, COUNT(*) AS bookings_count
FROM bookings
WHERE start_date >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY month
ORDER BY month;
