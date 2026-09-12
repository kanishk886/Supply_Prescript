# MetricMind Super Store Data Dictionary

## Source Database
Snowflake Database: `METRICMIND_DB`
Schema: `PUBLIC`
Table: `FCT_SALES`

## Schema Details
| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| CATEGORY | VARCHAR | Product category (e.g. Office Supplies) |
| CITY | VARCHAR | Customer city |
| COUNTRY | VARCHAR | Customer country |
| Customer.ID | VARCHAR | Unique identifier for customer |
| Customer.Name | VARCHAR | Customer name |
| DISCOUNT | NUMBER | Discount applied to order |
| MARKET | VARCHAR | Market segment |
| 记录数 | NUMBER | Record count |
| Order.Date | TIMESTAMP_NTZ | Date order was placed |
| Order.ID | VARCHAR | Unique identifier for the order |
| Order.Priority | VARCHAR | Priority level of the order |
| Product.ID | VARCHAR | Unique identifier for the product |
| Product.Name | VARCHAR | Name of the product |
| PROFIT | NUMBER | Profit generated from the order |
| QUANTITY | NUMBER | Number of units ordered |
| REGION | VARCHAR | Region of the customer |
| Row.ID | NUMBER | Sequential row identifier |
| SALES | NUMBER | Total sales value |
| SEGMENT | VARCHAR | Customer segment (e.g. Consumer) |
| Ship.Date | TIMESTAMP_NTZ | Date the order was shipped |
| Ship.Mode | VARCHAR | Shipping mode (e.g. Standard Class, Second Class) |
| Shipping.Cost | NUMBER | Cost of shipping |
| STATE | VARCHAR | Customer state |
| SUB_CATEGORY | VARCHAR | Product sub-category |
| YEAR | NUMBER | Year of the order |
| MARKET2 | VARCHAR | Secondary market identifier |
| WEEKNUM | NUMBER | Week number of the year |
| PROFIT_MARGIN_PERCENTAGE | FLOAT | Profit margin as a percentage |

## Target Variable Formulation
**Target**: `Order-to-Ship Duration` (Target Variable: `shipping_delay_days`)
**Calculation**: `Ship.Date - Order.Date` (measured in days).
This variable represents operational duration. A configurable threshold (e.g., > 3 days) will be used to flag a shipment as "at-risk" (high risk delay).
