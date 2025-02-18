from __future__ import annotations
from typing_extensions import get_type_hints
from dataclasses import dataclass, field, MISSING
from typing import Any, Self, ClassVar, get_args, get_origin, Callable, Literal, Iterator, override
import inspect
from reprlib import recursive_repr
import logging
import asyncio
from warnings import deprecated
from httpx import HTTPStatusError

from . import config
from .client import Client

#TODO: Add support for DELETEd objects, weakrefs, automatic update of Paginated data when DELETE/POST is called

LOGGER = logging.getLogger(__name__)

class _NULL:
    def __repr__(self):
        return "<NIL>"

NULL = _NULL()

type UrlStr[T] = T

def datafield(readonly: bool = True, required: bool = True):
    if readonly:
        assert required
    #return field(default=MISSING if not readonly and required else NULL, init=not readonly)
    return field(default=NULL, init=not readonly)

def check_base_recursive(type_: type) -> type[BaseClass]|None:
    """Returns BaseClass subclass if type_ contains elements of BaseClass
    e.g. type[BaseClass], Union[type[BaseClass]], list[type[BaseClass]]

    Args:
        type_ (type): Type to check

    Returns:
        type[BaseClass]|None: Subclass of BaseClass if found, None otherwise
    """
    # X[Y], where X = Literal, Union, list, etc.
    if get_origin(type_) is not None:
        if get_origin(type_) is Literal:
            return None
        return next((check_base_recursive(arg) for arg in get_args(type_)), None)
    if issubclass(type_, BaseClass):
        return type_
    return None

@dataclass(init=False, repr=False)
class BaseClass:
    _client: Client|None = field(default=None, init=False)
    _client_made: bool = field(default=False, init=False)
    
    IGNORED_ATTRIBUTES: ClassVar[set[str]] = {"_client", "IGNORED_ATTRIBUTES", "JSON_ATTRIBUTES"}
    JSON_ATTRIBUTES: ClassVar[dict[Literal["GET", "POST", "PUT", "PATCH", "DELETE"] | str, set[str]]] = {}
    
    def _is_data_attribute(self, name: str) -> bool:
        return name in object.__getattribute__(self, "_get_data_fields")()
    
    def _get_data_fields(self) -> set[str]:
        return {k for k in object.__getattribute__(self, "__class__").__dataclass_fields__.keys() if k not in object.__getattribute__(self, "IGNORED_ATTRIBUTES")}
    
    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if object.__getattribute__(self, "_is_data_attribute")(name) and attr is NULL and config.CONFIG_NULL_EXCEPTION:
            raise AttributeError(f"'{self.__class__.__name__}' object has missing data attribute '{name}'")
        return attr
    
    def __setattr__(self, name, value):
        if self._is_data_attribute(name):
            #TODO: Add type checking for manual insertion
            pass
        super().__setattr__(name, value)
    
    @recursive_repr()
    def __repr__(self):
        attrs = [
            f'{k}={v}'
            for k in self._get_data_fields()
            if k not in self.IGNORED_ATTRIBUTES and (v := getattr(self, k)) is not NULL
        ]
        return f"<{self.__class__.__name__} {', '.join(attrs)}>"
    
    def _parse_data[T](self, data: Any, type_: type[T]) -> T:
        if data is None or data is NULL:
            return data
        # UrlStr[IdentifiableBase], UrlStr[list[IdentifiableBase]], UrlStr[Union[IdentifiableBase]], UrlStr[list[Union[IdentifiableBase]]]
        if get_origin(type_) is UrlStr:
            type_arg = get_args(type_)[0]
            if get_origin(type_arg) is list:
                # data: list[str]
                return [self._client.get_and_set_data(data, get_args(type_arg)[0]) for data in data]
            # type_arg: IdentifiableBase | Union[IdentifiableBase]
            return self._client.get_and_set_data(data, type_arg)
        base = check_base_recursive(type_)
        # Not associated with BaseClass (i.e. a string, Literal, number, etc.)
        if base is None:
            return data
        # BaseClasses that need caching
        if issubclass(base, IdentifiableBase):
            # FIXME: Atomicity is not ensured when some objects fail during caching
            if get_origin(type_) is list:
                return [self._client.get_and_set_data(d.get("url"), base, content=d) for d in data]
            return self._client.get_and_set_data(data.get("url"), base, content=data)
        if issubclass(base, BaseClass):
            def _parse_base(data: dict[str, Any]) -> BaseClass:
                obj = base._from_client(self._client)
                obj.update_data(data)
                return obj
            if get_origin(type_) is list:
                return [_parse_base(d) for d in data]
            return _parse_base(data)
        raise TypeError(f"Invalid type {type_} found in object")
    
    @deprecated("Use _parse_data for atomic updating")
    def _parse_and_insert_data(self, name: str, value: Any) -> Any:
        """Method for parsing raw json data

        Args:
            name (str): property name
            value (Any): value, usually dict, list, or literal number/string

        Returns:
            Any: _description_
        """
        value_ = NULL
        type_ = get_type_hints(self.__class__)[name]
        if value is None or value is NULL:
            value_ = value
        elif get_origin(type_) is UrlStr:
            # IdentfiableBase, list[IdentifiableBase], Union[IdentifiableBase], list[Union[IdentifiableBase]] 
            inside = get_args(type_)[0]
            if get_origin(inside) is list:
                inside = get_args(inside)[0]
                value_ = [self._client.get_and_set_data(value, inside) for value in value]
            else:
                value_ = self._client.get_and_set_data(value, inside)
        else:
            def _check_base_recursive(type_: type) -> type[BaseClass]|None:
                # Returns BaseClass if type_ contains elements of BaseClass (i.e. type[BaseClass], Union[type[BaseClass]], list[type[BaseClass]])
                if get_origin(type_) is not None:
                    if get_origin(type_) is Literal:
                        return None
                    return next((_check_base_recursive(arg) for arg in get_args(type_)), None)
                if issubclass(type_, BaseClass):
                    return type_
                return None
            base = _check_base_recursive(type_)
            if base is None:
                value_ = value
            elif issubclass(base, IdentifiableBase):
                if get_origin(type_) is list:
                    value_ = [self._client.get_and_set_data(value.get("url"), base, content=value) for value in value]
                else:
                    value_ = self._client.get_and_set_data(value.get("url"), base)
            elif issubclass(base, BaseClass):
                def _parse_value(value: dict[str, Any]) -> BaseClass:
                    obj = base._from_client(self._client)
                    obj.update_data(value)
                    return obj
                if get_origin(type_) is list:
                    value_ = [_parse_value(value) for value in value]
                else:
                    value_ = _parse_value(value)
            else:
                raise TypeError(f"Invalid type {type_} found in object")
        super().__setattr__(name, value_)
    
    @classmethod
    def _from_client(cls, client: Client) -> Self:
        # Fill required parameters with NULL
        sig = inspect.signature(cls)
        bind = sig.replace(parameters=[p.replace(default=NULL) for p in sig.parameters.values()]).bind()
        bind.apply_defaults()
        obj = cls(*bind.args, **bind.kwargs)
        obj._client = client
        obj._client_made = True
        return obj
    
    def update_data(self, data: dict[str, Any]):
        parsed_data: dict[str, Any] = {
            k: self._parse_data(v, get_type_hints(self.__class__)[k])
            for k, v in data.items()
        }
        for key, value in parsed_data.items():
            assert self._is_data_attribute(key), f"Invalid key {key} found in object"
            super().__setattr__(key, value)
        # for key in self._get_data_fields():
        #     value = data.get(key, NULL)
        #     self._parse_and_insert_data(key, value)
        #     if key in data:
        #         del data[key]
        # if data:
        #     raise ValueError(f"Invalid keys {list(data.keys())} found in object")
    
    def to_json(self, mode: str = "default") -> dict[str, Any] | None:
        type_hints = get_type_hints(self.__class__)
        included_attributes = None
        if mode in self.JSON_ATTRIBUTES:
            included_attributes = self.JSON_ATTRIBUTES[mode]
        elif mode == "all":
            included_attributes = self._get_data_fields()
        else:
            # Everything except readonly attributes
            included_attributes = {k for k, v in self.__class__.__dataclass_fields__.items() if v.init and k in type_hints and k not in self.IGNORED_ATTRIBUTES}
        if included_attributes is None:
            return None
        def _convert(annotation: type, value: Any) -> Any:
            if value is None:
                return None
            if get_origin(annotation) is UrlStr:
                if get_origin(get_args(annotation)[0]) is list:
                    return [v._href for v in value]
                return value._href
            if isinstance(value, BaseClass):
                return value.to_json(self.__class__.__name__)
            if isinstance(value, list):
                return [_convert(get_args(annotation)[0], v) for v in value]
            return value
        json_data = {
            k: _convert(type_hints[k], v)
            for k in included_attributes
            if (v := object.__getattribute__(self, k)) is not NULL
        }
        return json_data

type JsonResponse = dict[str, Any] | list[Any]
type ResponseHandlerCallable = Callable[[JsonResponse, str], JsonResponse]

@dataclass(init=False, repr=False)
class ResponseHandler:
    handler_get: ResponseHandlerCallable|None = None
    handler_post: ResponseHandlerCallable|None = None
    handler_put: ResponseHandlerCallable|None = None
    handler_patch: ResponseHandlerCallable|None = None
    handler_delete: ResponseHandlerCallable|None = None
    
    def __init__(
        self,
        all: ResponseHandlerCallable = None,
        *,
        get: ResponseHandlerCallable = None,
        post: ResponseHandlerCallable = None,
        put: ResponseHandlerCallable = None,
        patch: ResponseHandlerCallable = None,
        delete: ResponseHandlerCallable = None
    ):
        if all is not None:
            if not (get is None and post is None and put is None and patch is None and delete is None):
                raise ValueError("Cannot provide both 'all' and specific methods")
            self.handler_get = all
            self.handler_post = all
            self.handler_put = all
            self.handler_patch = all
            self.handler_delete = all
        else:
            self.handler_get = get
            self.handler_post = post
            self.handler_put = put
            self.handler_patch = patch
            self.handler_delete = delete
    
    def get_handler(self, method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]) -> ResponseHandlerCallable|None:
        if method == "GET":
            return self.handler_get
        if method == "POST":
            return self.handler_post
        if method == "PUT":
            return self.handler_put
        if method == "PATCH":
            return self.handler_patch
        if method == "DELETE":
            return self.handler_delete
        raise ValueError(f"Invalid method {method}")

@dataclass(init=False, repr=False)
class IdentifiableBase(BaseClass):
    _href: str|None = field(default=None, init=False)
    _loaded: bool = field(default=False, init=False)
    
    IGNORED_ATTRIBUTES: ClassVar[set[str]] = {"_client", "_href", "_loaded", "IGNORED_ATTRIBUTES", "JSON_ATTRIBUTES", "AVAILABLE_METHODS", "RESPONSE_HANDLER"}
    AVAILABLE_METHODS: ClassVar[set[Literal["GET", "POST", "PUT", "PATCH", "DELETE"]]] = {"GET"}
    RESPONSE_HANDLER: ClassVar[ResponseHandler | None] = None
    JSON_ATTRIBUTES: ClassVar[dict[Literal["GET", "POST", "PUT", "PATCH", "DELETE"] | str, set[str]]] = {
        "GET": None,
        "DELETE": None
    }
    
    @override
    def __getattribute__(self, name):
        if object.__getattribute__(self, "_is_data_attribute")(name) and not object.__getattribute__(self, "_loaded") and object.__getattribute__(self, "_client_made") and config.CONFIG_LAZY_LOAD:
            object.__getattribute__(self, "_load")()
        attr = object.__getattribute__(self, name)
        if object.__getattribute__(self, "_is_data_attribute")(name) and attr is NULL and config.CONFIG_NULL_EXCEPTION:
            raise AttributeError(f"'{self.__class__.__name__}' object has missing data attribute '{name}'")
        return attr
    
    @override
    def __repr__(self):
        if self._loaded:
            return super().__repr__()
        return f"<Lazy {self.__class__.__name__} href={self._href}>"
    
    @override
    def update_data(self, data):
        super().update_data(data)
        self._loaded = True
    
    async def load(self, force: bool = False, depth: int = 0, order: Literal["wait-single-layer", "wait-all-layers", "no-wait"] = "wait-all-layers") -> Self:
        if depth < 0:
            raise ValueError("Depth must be a non-negative integer")
        if force or not self._loaded:
            await self.request_get()
        if depth > 0:
            if order == "wait-single-layer":
                raise NotImplementedError("wait-single-layer not implemented")
            elif order == "wait-all-layers":
                loaded_urls: set[IdentifiableBase] = set()
                next_load: list[IdentifiableBase] = self._get_loadable_children()
                
                async def _load_child(obj: IdentifiableBase) -> IdentifiableBase|None:
                    if obj._href not in loaded_urls:
                        loaded_urls.add(obj._href)
                        return await obj.load(force, 0)
                
                for i in range(depth):
                    res = await asyncio.gather(*[_load_child(obj) for obj in next_load])
                    next_load.clear()
                    for obj in res:
                        if obj is not None:
                            next_load.extend(obj._get_loadable_children())
            elif order == "no-wait":
                LOGGER.warning("no-wait is not recommended for large depths")
                await asyncio.gather(*[obj.load(force, depth - 1, order) for obj in self._get_loadable_children()])
        return self
    
    async def request_get(self):
        await self._request_async("GET", self.to_json("GET"))
    
    async def request_post(self):
        await self._request_async("POST", self.to_json("POST"))
    
    async def request_put(self):
        await self._request_async("PUT", self.to_json("PUT"))
    
    async def request_patch(self, patch_data: Self):
        if not isinstance(patch_data, self.__class__):
            raise TypeError(f"Invalid patch data {patch_data.__class__.__name__} for object {self.__class__.__name__}")
        await self._request_async("PATCH", patch_data.to_json("PATCH"))
    
    async def request_delete(self):
        await self._request_async("DELETE", None, update_data=False)
    
    async def _request_async(self, method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"], body: dict|list|None=None, params: dict = None, update_data: bool = True):
        self._check_request_permission(method)
        try:
            response = await self._client._request_async(method, self._href, body, params)
        except HTTPStatusError as e:
            if config.CONFIG_FAILED_REQUESTS_EXCEPTION:
                raise e
            else:
                return
        if not update_data:
            return
        response_handler = self.RESPONSE_HANDLER.get_handler(method) if self.RESPONSE_HANDLER is not None else None
        if response_handler:
            response = response_handler(response, self._href)
        self.update_data(response)
    
    def _request_sync(self, method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"], params: dict = None):
        self._check_request_permission(method)
        try:
            response = self._client._request_sync(method, self._href, self.to_json(method), params)
        except HTTPStatusError as e:
            if config.CONFIG_FAILED_REQUESTS_EXCEPTION:
                raise e
            else:
                return
        reponse_handler = self.RESPONSE_HANDLER.get_handler(method) if self.RESPONSE_HANDLER is not None else None
        if reponse_handler:
            response = reponse_handler(response, self._href)
        self.update_data(response)
    
    def _check_request_permission(self, method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]) -> None:
        if self._client is None:
            raise ValueError(f"Object {self.__class__.__name__} is not associated with a client")
        if self._href is None:
            raise ValueError(f"Object {self.__class__.__name__} does not have a valid href")
        if method not in self.AVAILABLE_METHODS:
            raise ValueError(f"Method {method} not available for object {self.__class__.__name__}")
    
    def _load(self):
        LOGGER.debug(f"Loading lazy {self.__class__.__name__} object")
        self._request_sync("GET")
    
    def _get_loadable_children(self) -> list[IdentifiableBase]:
        children = {}
        def run(obj: Any) -> None:
            if isinstance(obj, IdentifiableBase):
                children[obj._href] = obj
            elif isinstance(obj, BaseClass):
                for key in obj._get_data_fields():
                    run(getattr(obj, key))
            elif isinstance(obj, list):
                for e in obj:
                    run(e)
        for key in self._get_data_fields():
            run(getattr(self, key))
        return list(children.values())

@dataclass(init=False, repr=False)
class PaginatedBase[T](IdentifiableBase):
    _data: list[T] = field(default_factory=list, init=False)
    
    JSON_ATTRIBUTES: ClassVar[dict[str, set[str]]] = {
        "GET": None
    }
    
    def __iter__(self) -> Iterator[T]:
        data = self._data
        return iter(data)
    
    def __getitem__(self, key: int) -> T:
        return self._data[key]
    
    def __len__(self) -> int:
        return len(self._data)
    
    @override
    def update_data(self, data: list) -> None:
        data_ = {
            "_data": data
        }
        super().update_data(data_)
    
    def find(self, *funcs: Callable[[T], bool], **kwargs) -> T|None:
        data = self._data
        def _query(e: T) -> bool:
            for func in funcs:
                if not func(e):
                    return False
            for key, value in kwargs.items():
                if getattr(e, key) != value:
                    return False
            return True
        return next((e for e in data if _query(e)), None)
    
    def filter(self, *funcs: Callable[[T], bool], **kwargs) -> list[T]:
        data = self._data
        def _query(e: T) -> bool:
            for func in funcs:
                if not func(e):
                    return False
            for key, value in kwargs.items():
                if getattr(e, key) != value:
                    return False
            return True
        return [e for e in data if _query(e)]