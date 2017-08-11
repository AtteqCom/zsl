Modules and Containers
######################

Modules and Containers are the main way how to:

* provide services,
* master dependency injection,
* extend ZSL.

Each module can provide objects via dependency injection. And thus if module
is added to the application container, the dependency injection may inject
the objects provided by module.


Services
========

Instead of manually providing services via a module, there is a mechanism to
automatically provided services via injection. If they are placed inside the
configured service package, they are automatically created and injected.

