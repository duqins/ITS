# The Arabic pages write numbers the way they are written in the UAE: 1,800.00 (Django's own Arabic
# format would write 1.800,00). Dates are DD month YYYY and action times are in Gulf Standard Time,
# as on the English pages (SRS 3.1.1).
DECIMAL_SEPARATOR = "."
THOUSAND_SEPARATOR = ","
NUMBER_GROUPING = 3
DATE_FORMAT = "d F Y"
DATETIME_FORMAT = "d F Y، H:i بتوقيت الخليج"
