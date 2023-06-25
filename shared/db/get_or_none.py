from typing import TypeVar, Type, Union

Model = TypeVar('Model')


async def get_or_none(model: Type[Model], **kwargs) -> Union[Model, None]:
    try:
        return await model.objects.aget(**kwargs)
    except:
        return None
