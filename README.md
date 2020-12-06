# final-project-coderslab
Final project for CodersLab Python Bootcamp

Project is a site to order from sushi restaurant.

Models used: 
  -User -> Djangos user model, taken from djangos libraries.
  -Cart -> Model for Users cart. It has relations with User model (one to one relation) and with Product model (many to many). Last field is price field, made with djangos DecimalField.
  -Product -> Model for restaurants products. It has relations with Cart model, Ingredients model (many to many), Category model (many to many). Other fields present are: Name (CharField), Price (DecimalField) and Details (TextField).
  -Category -> Model for Products categories. Other than ManyToMany relation with Product, it has Name field (CharField) and Details field (TextField)
  -Address -> Model for Users delivery address. It has relation with User model (OneToMany), and fields: Street (CharField), Street_number (IntegerField) and Home_number (IntegerField)
  -Ingredients -> Model for ingredients in restaurants products. It has ManyToMany relation with Product model. Fields in it are: Name (CharField), Is_gluten (BoolField, used to indicate if gluten is present), Is_not_vegan (BoolField, by default True, idicates if ingredient is made from animal products) and Is_allergic (BoolField, used to idicate if it can produce allergic reaction for somebody)
  
