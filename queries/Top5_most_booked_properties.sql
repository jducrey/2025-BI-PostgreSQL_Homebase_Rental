SELECT p.title, COUNT(b.booking_id) AS total_bookings
FROM properties p
JOIN bookings b ON p.property_id = b.property_id
GROUP BY p.title
ORDER BY total_bookings DESC
LIMIT 5;
