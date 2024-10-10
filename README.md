# STOCKX
#### Video Demo: https://youtu.be/X-mkaG9ZriQ
#### Description:
StockX is a app designed for new investors navigating the Brazilian stock market (B3) who follow a strategy of maintaining an even distribution of their holdings across multiple stocks. This app provides a interface to simulate the purchase of new shares, allowing investors to visualize the impact on their portfolio before making any real investments.
##### Key features:
1. **Portfolio Overview:**
    - View a overview of your current portfolio, including the number of shares, the total value of each stock and the weight they represent in your portfolio.
2. **Simulate New Share Purchase:**
    - Easily simulate the purchase of new shares and the impact in your portfolio.
3. **Real-Time Prices:**
    - Access updated stock prices from the B3 market, powered by the finances API Brapi available on https://brapi.dev/. This integration ensures accurate data based on the latest market conditions.

The objective is to assist new B3 investors in enhancing their decision-making regarding portfolio allocation, optimizing investments, maintaining a well-balanced distribution across all holdings, and visualizing their overall investment strategy.

---

#### Project files description:
 - **static/index.js**: File that contains the javascript responsible for updating the table when the number of shares changes:
    - **handleSharesNumber** function: Handle the value of the shares input, performs validations to avoid invalid values, calculates new value, assigns the value to the element and returns the new value.
    - **updateTable** function: Calls the handleSharesNumber function and based on the returned value, calculates and updates the table with new values, it is called when the increment and decrement buttons are clicked.
 - **schema.sql**: SQL code that creates the database file and tables.
 - **app.py**: Main app file, for general configuration and routes.
 - **helpers.py**: Functions that will be used several times in the project:
    - **login_required** function: Check if there is already an active session and redirects to the login page.
    - **quote** function: Make a request to the Brapi API to obtain data for a specific symbol.
---

#### Create database and tables:
`sqlite3 database.db ".read schema.sql"`

#### Some B3 symbols for testing:
- PETR4 (Petrobras)
- VALE3 (Vale)
- ITUB4 (Itaú Unibanco)
- BBDC4 (Bradesco)
- BBAS3 (Banco do Brasil)

---

### For development purposes:
- Primary color: #D5B263
- Background color: ##212529

#### General guidelines:
- [x] Register
    - [x] Usernme
        - [x] Unique
        - [x] Error message
    - [x] Password
        - [x] Confirmation match
        - [x] Error message
    - [x] Success message
- [x] Login
    - [x] Error messages
- [x] Pofile
    - [x] Change username
        - [x] Unique
        - [x] Error message
        - [x] Success message
    - [x] Change password
        - [x] Confirmation match
        - [x] Error message
        - [x] Success message
- [x] Logout
- [x] Portfolio
    - [x] List stocks
        - [x] Quote
    - [x] Edit shares
        - [x] Remove stock
        - [x] Update table
            - [x] Shares
            - [x] Variation
            - [x] Weight
            - [x] Shares total
            - [x] Total
    - [x] Add new stock
        - [x] Check if already exists
        - [x] Quote
        - [x] Error messages
    - [x] Undo changes
    - [x] Delete portfolio
    - [x] Save
