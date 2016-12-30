# Importing a dynamically generated module
# http://stackoverflow.com/questions/5362771/load-module-from-string-in-python

# Note: IMP is being deprocated in favor of...
# https://docs.python.org/3/library/importlib.html#module-importlib
def importCode(code,name,add_to_sys_modules=0):
    """
    Import dynamically generated code as a module. code is the
    object containing the code (a string, a file handle or an
    actual compiled code object, same types as accepted by an
    exec statement). The name is the name to give to the module,
    and the final argument says wheter to add it to sys.modules
    or not. If it is added, a subsequent import statement using
    name will return this module. If it is not added to sys.modules
    import will try to load it in the normal fashion.

    import foo

    is equivalent to

    foofile = open("/path/to/foo.py")
    foo = importCode(foofile,"foo",1)

    Returns a newly generated module.
    """
    import sys,imp

    module = imp.new_module(name)

    #exec code in module.__dict__
    exec(code, module.__dict__)

    if add_to_sys_modules:
        sys.modules[name] = module

    return module
