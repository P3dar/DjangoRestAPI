This file contains some informations about the RestAPI project.

1: the api is only for learnig purpose
2: for a correct use a localhost must be used, it's already preconfigured
3: the superuser/manager credentials are: username = maggio, password = marcomaggio
4: delivery crew credentials:
    username: rocco password: roccoiudici
    username: sielo password: porcucan
5: authenticated customers:
    username: beatrice password: cagna1994
    username: valeria password: fagiolina95
6: a list of all endpoints:
    /api/menu-items/
    /api/menu-items/<int:pk>
    /api/groups/manager/users
    /api/groups/manager/users/<int:pk>
    /api/groups/delivery-crew/users
    /api/groups/delivery-crew/users/<int:pk>
    /api/cart/menu-items
    /api/category
    /api/orders
    /api/orders/<int:pk>
7: filtering, searching, ordering and pagination options 
    are avaible only if manualy declared in the endpoints
8: throttoling rate is 20 calls/minute
9: for a better test experience is reccomanded the use of Insomnia, Postman
    or another similar tool