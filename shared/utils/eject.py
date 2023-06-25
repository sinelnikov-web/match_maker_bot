def eject_kwargs(base_model, extra_model):
    arg_names = base_model.__init__.__code__.co_varnames
    if arg_names[0] == 'self':
        arg_names = arg_names[1:]

    new_dict = dict()

    for arg in arg_names:
        new_dict[arg] = extra_model.__dict__.get(arg)

    return new_dict