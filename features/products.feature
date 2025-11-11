Feature: The product service handles products
    As an e-commerce user
    I need to interact with products
    So that I can manage inventory

Background:
    Given the following products
        | name | description | price | available | category |
        | Hat | A nice hat | 10.00 | true | CLOTHING |
        | Shirt | A nice shirt | 20.00 | true | CLOTHING |
        | Pants | A nice pair of pants | 30.00 | false | CLOTHING |
        | Apple | A red apple | 0.50 | true | FOOD |
        | Orange | A ripe orange | 0.80 | true | FOOD |
        | TV | A 4K TV | 1000.00 | true | ELECTRONICS |

    # (Task 6a) READ
    Scenario: Read a Product
        When I visit the "Home Page"
        And I set the "Product ID" to "1"
        And I press the "Retrieve" button
        Then I should see "Hat" in the "name"
        And I should see "10.00" in the "price"

    # (Task 6b) UPDATE
    Scenario: Update a Product
        When I visit the "Home Page"
        And I press the "Clear" button
        And I set the "Product ID" to "1"
        And I press the "Retrieve" button
        And I should see "Hat" in the "name"
        And I change the "Name" to "Fedora"
        And I press the "Update" button
        Then I should see the message "Success"
        When I press the "Clear" button
        And I set the "Product ID" to "1"
        And I press the "Retrieve" button
        Then I should see "Fedora" in the "name"
    
    # (Task 6c) DELETE
    Scenario: Delete a Product
        When I visit the "Home Page"
        And I set the "Product ID" to "1"
        And I press the "Retrieve" button
        Then I should see "Hat" in the "name"
        When I press the "Delete" button
        Then I should see the message "Success"
        When I press the "Clear" button
        And I set the "Product ID" to "1"
        And I press the "Retrieve" button
        Then I should see "Hat" not in the "name"
        
    # (Task 6d) LIST ALL
    Scenario: List all products
        When I visit the "Home Page"
        And I press the "Search" button
        Then I should see "Hat" in the results
        And I should see "Shirt" in the results
        And I should see 6 rows in the results

    # (Task 6e) Search by Category
    Scenario: Search products by category
        When I visit the "Home Page"
        And I select "CLOTHING" in the "Category"
        And I press the "Search" button
        Then I should see "Hat" in the results
        And I should see "Shirt" in the results
        And I should not see "Apple" in the results

    # (Task 6f) Search by Availability
    Scenario: Search products by availability
        When I visit the "Home Page"
        And I select "True" in the "Available"
        And I press the "Search" button
        Then I should see "Hat" in the results
        And I should not see "Pants" in the results

    # (Task 6g) Search by Name
    Scenario: Search products by name
        When I visit the "Home Page"
        And I set the "Name" to "Hat"
        And I press the "Search" button
        Then I should see "Hat" in the results
        And I should not see "Shirt" in the results
