# CS50W

### A repo for CS50's Web Programming with Python and JavaScript course.

## Projects

| #  | Project                | Description                                       | Video
| :- | :--------------------- | :------------------------------------------------ | :-------------------------------------
| 0  | [Search](search)       | Google Search Functionality                       | [Link](https://youtu.be/-ttbk3hA9FI)
| 1  | [Wiki](wiki)           | Wikipedia-like online Encyclopedia                | [Link](https://youtu.be/mHUZUWfhrE8)
| 2  | [Commerce](commerce)   | eBay like e-commerce auction site                 | [Link](https://youtu.be/xJp-cvoas7g)
| 3  | [Mail](mail)           | Frontend for an email client                      | [Link](https://youtu.be/K_ngUP_ueQY)

## Note - Running the Project

1. To run any project, `cd` into the directory of the project. Before running it, we will apply the migrations. In the terminal type - 
```
python manage.py makemigrations
```
``` 
python manage.py migrate
```
2. To access the project from Django admin interface, we need to create a superuser. Do this by typing the following - (After this, proceed to add your username, email and password. Then you can visit 127.0.0.1:8000/admin and login.) 

``` 
python manage.py createsuperuser
```
3. Finally, we can run the project on our server. Type-
```
python manage.py runserver 
```
4. In the browser, visit 127.0.0.1:8000 to view the project.
