SELECT p.title, AVG(r.rating) AS avg_rating
FROM properties p
JOIN bookings b ON p.property_id = b.property_id
JOIN reviews r ON b.booking_id = r.booking_id
GROUP BY p.title
ORDER BY avg_rating DESC;