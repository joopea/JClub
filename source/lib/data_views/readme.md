# Data Views #

*Data Views for creating a controllable layer between view and (Django) ORM*

Instead of using the ORM directly it's mandatory to use Data Views as data api layer.

The data api provides us with a few important benefits like being able to monitor and cache certain functions, as well as changing the implementation without changing the interface.

To keep the data view class as abstract as possible and prevent possible circular import we are using django's get_model() method to get a model instance. It's required to assign the app_name and model name when inheriting.

As a wrapper for getting a single object the query_single is used. By separating these two both querying multiple and single record can be implemented on a Data View.

Caching can be added in a very simple way:
- Using the provided decorators
- And directly passing arguments to configure cashing

Situated here is an example implementation of a Data View:


```
#!python

class ExampleDataView(ModelDataView):    
    app_name = "example"
    model = "Example"
    
    @classmethod
    def by_id(cls, object_id):
        # Getting a single record by Id
        return cls.get_or_none(id=object_id)

    @classmethod
    def published(cls):
        #Getting a list of published records
        return cls.list(published=True)
        
```

*Usage*

A few quidelines for using the data api as intended:

- Create data_views.py in your app.
- Implement your ORM calls in a ModelDataView subclass
- Only query on the model bound to the ModelDataView
- The ModelDataView API can be used to bind to Django ModelForms or CBV's either with queryset or get_model


*Installation*

```
#!bash

pip install [path_to_package]

```
