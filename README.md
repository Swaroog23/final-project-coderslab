# final-project-coderslab
__*Final project for CodersLab Python Bootcamp*__

Project is a site to order from sushi restaurant. All of site is written in Polish language.
In order to access site, you'll need to run in your terminal, **with activated venv, all dependencies installed and database ready**, command *"python3 manage.py runserver"*
By default, it will run on _localhost:8000/_

## Dependencies:
* All needed libraries are in file "reqierments.txt". To download them, you'll need Pythons virtual enviorment, and then run command "pip3 install -r requierments.txt" while venv is activated.

## Setting up:
* There are few things you'll need to do for this site to work. First of, you'll need to set up a PostgreSQL database with name "buri", or change in settings.py database setting to suit your needs. For me, it runs on Postgre with buri for db name. You'll need to supply django with login and password to get to db, and if you want to use diffrent db, you'll need to supply django with correct library to work.
* After setting up db, and having your Virtual Env set up and ready to use, you'll need to run these commands:
  * _"python3 manage.py makemigrations"_ <- this command prepares set of data to transfer to db, like setting up tables and relations.
  * _"python3 manage.py migrate"_ <- this command applies all changes to the database. Is is neccessary for this up to run, so don't forget about it.
* After this set of comnmand you sould be able to type _"python3 manage.py runserver"_ to start server with site on it.

## Models used: 
*  **User** -> Djangos user model, taken from djangos libraries.
*  **Cart** -> Model for *Users* cart. It has relations with *User* model (*OneToOne*) and with *Product* model (*ManyToMany*). Last field is Price field, made with djangos *DecimalField*.
*  **Product** -> Model for restaurants products. It has relations with *Cart* model, *Ingredients* model (*ManyToMany*), *Category* model (*ManyToMany*). Other fields present are: Name (*CharField*), Price (*DecimalField*) and Details (*TextField*).
*  **Category** -> Model for *Products* categories. Other than *ManyToMany* relation with *Product*, it has Name field (*CharField*) and Details field (*TextField*).
*  **Address** -> Model for *Users* delivery address. It has relation with *User* model (*OneToMany*), and fields: Street (*CharField*), Street_number (*IntegerField*) and Home_number (*IntegerField*).
*  **Ingredients** -> Model for ingredients in restaurants products. It has *ManyToMany* relation with *Product* model. Fields in it are: Name (*CharField*), Is_gluten (*BooleanField*, used to indicate if gluten is present), Is_not_vegan (*BooleanField*, by default **True**, idicates if ingredient is made from animal products) and Is_allergic (*BooleanField*, used to idicate if it can produce allergic reaction for somebody).

## Views in project:
*  **Main page** (url: "/") -> First page of the site. It consists of anchor for user creation page, login page, menu page, cart page and anchor back to main menu. If user is logged in, it will show insted of login and create user page, a logout page and account details page. If user has _"is_staff"_ field set to true, it will also have a page for adding new products.
*  **Menu page** (url: "/categories/") -> This page shows all categories in menu with short summary of what specific category is. Also contains similar anchors like main page, but without menu and add product pages. Name of each category in menu page is an anchor to page with all products inside specific category
*  **Category detail page** (url: "/category/<category id>/") -> Shows all products in given category. Each product is shown with price, description and ingredients, which show if the ingredients are vegan, gluten free or can couse allergic response. Below each of the product is form with amount and submit button, used for storing amount of specific product that the user wants to order. Orders are stored in cookies. Has same anchors as previous view with addition of smaller menu anchors, which allow user to go to diffrent category without going back to category view.
*  **Cart page** (url: "/cart/<user id>/") -> Page for summary of order. It shows all ordered products with their amount and price for them. It contains anchors to change user data page, menu and main page, and payment page. For not loged users, it is possible to add products to cart and place an order.
*  **Payment page** (url: "/cart/<user id>/payment/") -> Its a similar page to cart page, but with added form with delivery address. Page saves address if it is validated. If successfull, address will be saved, if its not already in db and connected to user, and user will be shifted to main page with information that order was placed. If user is not loged, it is possible to place an order, and everything will be saved, but with user_id = None in db.
*  **Change user data page** (url "/user/<user id>/") -> Page containing all of user data, username, first and last name and email. Also, shows all saved addresses by user. It also contains a form for changing this data. It contains anchors to main page, change password form, and add new delivery address page.
*  **Change password form** (url: "/user/<user id>/change_password/") -> Page with djangos form for changing password. It does just that. Contains anchors for main page, logout page, and change user data page.
*  **Add new address page** (url: "/user/<user id>/add_new_address/") -> Similar page to previous, but with form to add new address.
*  **Login page** (url: "/login/?next=<url>/") -> Simple form for logging in user. Contains main and cart page anchors. GET argument "next" is used for returning user after successfull login to page where they were before logging in.
*  **Logut page** (url: "/logout/") -> Simple page that logs out user and returns them to main page.
*  **Create new user page** (url: "/create_user/") -> Simple django form for user creation. Only anchor present is to main page.
*  **Add new product page** (url: "/add_product/") -> If user has *is_staff* set to __true__, this form is avaiable. It allows to add new product to specific category, or multiple of them, with chosen ingredients. Has anchors to main page, logout page, and user data page.
  
  
  
