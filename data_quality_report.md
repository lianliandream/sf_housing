| Column           | Issue                         | Resolution                        |
| ---------------- | ----------------------------- | --------------------------------- |
| `monthly_rent`   | Stored as ranges              | Created midpoint column           |
| `square_footage` | Inconsistent labels (`Sq.ft`) | Standardized to `Sq.Ft`           |
| `bedroom_count`  | Multiple naming conventions   | Mapped to numeric values          |
| `bathroom_count` | Mixed text and numeric values | Standardized and converted        |
| `point`          | Coordinates stored as text    | Split into longitude and latitude |
