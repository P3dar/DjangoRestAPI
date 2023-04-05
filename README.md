# Online food E-commerce RestApi
## Made with Django DRF

This project was made for a back-end course assessment.

It's a mockup online restaurant RestAPI that allow customers to register and create an authentication token for performing different actions.

The Api has an authorization system that recognize if a user is a customer, a manager or a delivery-crew member.

The api utilize Djoser for Authentication. It automatically create generic endpoints for register, login, change password ecc...  they are avaible in the Djoser documentation in its website.

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
    
Managers can see all the delivery crew members data and add a new one from the customers.
    
    /api/groups/delivery-crew/users/<int:pk>
    
Managers can delete a delivery-crew member
    
    /api/cart/menu-items
    
a customer can add every menu item at the cart with a post request, wrtiting the id of the menuitem and the quantity. when the get method is used a customer can see only the items he added with the price of the single unit and the total price if the quantity is major than one. a manager can also see all the carts item of every customer.
    
    /api/category
    
A manager can view and add a new category
    
    /api/orders
    
A customer can create an order object and orderitems objects if his cart is not empty sending a blank post request to the endpoint. the logic of the view automatically retrive the items from the cart and convert them in orderitems. all the order items are bouded to a order object. the order object has some informations for exemple the date when the order was palced, the user who created it, the delivery crew that will process the order (set to none by default) and the total price of all the Orderitems in it. After this action the customer cart is automatically deleted. when a customer use a get method he can only see the orders, with the related orderitems, he placed. A Delivery-crew member can see only the orders with his ID. A manager can see all the orders.
    
    /api/orders/<int:pk>
    
A customer can see a specific order (if it exist and if it's his order). a manager can patch a order, this is used for pairing a delivery-crew worker to the order. he also can delete a order. A delivery cew memebr can also patch a order BUT only if the order is paired with him, he also have a limit to patch only the "status" field so he can update the order if it's delivered.
    
