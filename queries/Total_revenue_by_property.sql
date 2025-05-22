SELECT p.title, SUM(b.total_price) AS total_revenue
FROM properties p
JOIN bookings b ON p.property_id = b.property_id
GROUP BY p.title
ORDER BY total_revenue DESC;
