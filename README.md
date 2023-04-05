# Online food E-commerce RestApi
## Made with Django DRF

This project was made for a back-end course assessment.

It's a mockup online restaurant RestAPI that allow customers to register and create an authentication token for performing different actions.

The Api has an authorization system that recognize if a user is a customer, a manager or a delivery-crew member.
here's all the endpoints avaible and explained:

    /api/menu-items/
    
    an authenticated customer can see all the menu-items, perform searching, filtering and ordering. A manager can add new menu-items with a post request that comtains th title of the item, the price, the category and the featured check (True o False if is the menuitem of the day). Pagination is implemented.
    
    /api/menu-items/<int:pk>
    
    an authenticated cutomer can retrive a single menu-item data, a manager can also modify and delete it.
    
    /api/groups/manager/users
    
    A manager can see all the managers data and add a new one from the customers.
    
    /api/groups/manager/users/<int:pk>
    
    a manager can delete another manager from the list
    
    /api/groups/delivery-crew/users
    
    A manager can see all the delivery crew members data and add a new one from the customers.
    
    /api/groups/delivery-crew/users/<int:pk>
    
    a manager can delete a delivery-crew member
    
    /api/cart/menu-items
    
    a customer can add every menu item at the cart with a post request, wrtiting the id of the menuitem and the quantity. when the get method is used a customer can see only the items he added with the price of the single unit and the total price if the quantity is major than one. a manager can also see all the carts item of every customer.
    
    /api/category
    
    
    
    /api/orders
    /api/orders/<int:pk>
