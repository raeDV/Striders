# Striders

The propose of this website is to allow customers to purchase footwear online. Customers will be using this website.<br />
Our website is featured a login, register, manage account and add to cart as well as a men, women and kids section. we also featured new arrivals and sales on the main page.<br />
Also we have a home page as the base template contains different blocks like header and footer, all other pages will inherent from this page to ensuring consistency in design and user experience across all pages.<br />
## Experience example:<br />
The client should be able to shop (mandatory) and browse (mandatory) products in each category, sort (optional) and filter (optional) the category, add items to a cart (mandatory). The user will be prompt to login (mandatory) or create (mandatory) an account before add item to cart. <br />
For database part, we utilised SQLite database to store our data, which contains 3 tables: users, products, and cart.<br />
For users we collected some basic user information: username, Email, Password, phone and password.<br />
The products table contains all products we have: Product_Id, img_url, brand, category, size range, size type, colors, Description, Price, Size, etc...
Orders table will hold all the orders placed by our customer, fields will be: Order_id, User_id, Product_id, Amount, Time etc...
Task separations:
- Yateng: Accounts (DB, Frontend, Backend)
- Chester: Products (DB, Frontend, Backend)
- Noah: Orders (DB, Frontend checkout and cart, Backend)
- Remy: Features (Frontend sort, filter, new arrivals, sales, Backend for those feature)
