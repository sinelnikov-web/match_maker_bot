from collections.abc import Sequence
from dataclasses import fields, is_dataclass
from enum import Enum
from inspect import isclass
from typing import TypeVar, List, get_args, get_origin, get_type_hints, Callable, Generator, Union, Tuple, Any, Type
import dto

BaseModel = TypeVar('BaseModel')
DTOModel = TypeVar('DTOModel')


class LazyField(Sequence):
    is_initialized = False

    def __init__(self, init_function: Callable[[Tuple[Any]], List[Any]], args: list[Any] = []):
        self.init_function = init_function
        self.args = args

    def __getitem__(self, item):
        return self._get_collection_or_init()[item]

    def __len__(self):
        return len(self._get_collection_or_init())

    def _get_collection_or_init(self):
        if not self.is_initialized:
            self.collection = self.init_function(*self.args)
        return self.collection


def lazy_dto(fn: Callable[[Tuple[any]], Union[DTOModel, list[DTOModel]]], *args) -> Callable[
    [], Generator[Union[DTOModel, list[DTOModel]], None, None]]:
    def gen():
        yield fn(*args)

    return gen


def lazy_getattr(fields, dto):
    def inner(self, name):
        result = super(dto, self).__getattribute__(name)
        if callable(result) and name in fields:
            print(next(result()))
        return result
        # print(name)
        # if name in fields:
        #     n = next(object.__getattribute__(self, name)())
        #     return n
        # return object.__getattribute__(self, name)

    return inner


def has_dataclass(args):
    for arg in args:
        if is_dataclass(arg):
            return True
    return False

def get_dataclass(args):
    for arg in args:
        if is_dataclass(arg):
            return arg
    return False

def create_dto(base_model: BaseModel, dto_model: Type[DTOModel]) -> DTOModel:
    dto_fields = fields(dto_model)
    kwargs = {}
    annotations = get_type_hints(dto_model, localns={**vars(dto)})
    lazy_fields = []
    for field in dto_fields:
        annotation = annotations.get(field.name)
        args = get_args(annotation)
        origin = get_origin(annotation)
        if is_dataclass(annotation):
            kwargs[field.name] = create_dto(getattr(base_model, field.name), annotation)
        elif origin in [list, List]:
            type_arg = get_dataclass(args)
            fn = lambda t, f: list(map(lambda m: create_dto(m, t), getattr(base_model, f).all()))
            kwargs[field.name] = LazyField(fn, [type_arg, field.name])
            lazy_fields.append(field.name)
        elif has_dataclass(args):
            fn = lambda t, f: create_dto(getattr(base_model, f), t)
            kwargs[field.name] = LazyField(fn, [get_dataclass(args), field.name])
            lazy_fields.append(field.name)
        elif isclass(annotation) and issubclass(annotation, Enum):
            kwargs[field.name] = annotation(getattr(base_model, field.name))
        else:
            kwargs[field.name] = getattr(base_model, field.name)

    return dto_model(**kwargs)
