from __future__ import annotations
import httpx
from typing import TYPE_CHECKING, Literal, Optional
import logging
from urllib.parse import urlparse, urljoin

from .exceptions import HTTPStatusException

if TYPE_CHECKING:
    from .config import ClientConfig
    from .cache import BaseCache
    from .base import BaseClass, IdentifiableBase

LOGGER = logging.getLogger(__name__)

class Client:
    _config: ClientConfig
    _async_client: httpx.AsyncClient
    _sync_client: httpx.Client
    _cache: BaseCache
    
    def __init__(self, config: ClientConfig):
        self._config = config
        self._async_client = httpx.AsyncClient(
            #base_url=None,
            limits=httpx.Limits(max_connections=config.httpx_semaphore),
            timeout=httpx.Timeout(timeout=config.httpx_timeout),
            headers={"Authorization": f"Token {config.api_token}"} if config.api_token else {}
        )
        self._sync_client = httpx.Client(
            #base_url=None,
            limits=httpx.Limits(max_connections=config.httpx_semaphore),
            timeout=httpx.Timeout(timeout=config.httpx_timeout),
            headers={"Authorization": f"Token {config.api_token}"} if config.api_token else {}
        )
        self._cache = config.cache
    
    async def get_from_url(self, url: str, *, load: bool = True, register: bool = True) -> IdentifiableBase:
        """Get object from url

        Args:
            url (str): url of the object

        Returns:
            IdentifiableBase: the object
        """
        url = urljoin(self._config.base_url, url)
        obj = self.get_and_set_data(url, None, register=register)
        if not obj._loaded and load:
            await obj._request_async("GET")
        return obj
    
    async def get_v1(self) -> models.V1Root:
        return await self.get_from_url("/api/v1")
    
    async def get_tournaments(self) -> models.PaginatedTournaments:
        return await self.get_from_url("/api/v1/tournaments")
    
    async def get_tournament(self, tournament_slug: str) -> models.Tournament:
        return await self.get_from_url(f"/api/v1/tournaments/{tournament_slug}")
    
    async def get_institutions(self) -> models.PaginatedInstitutions:
        return await self.get_from_url("/api/v1/institutions")
    
    async def _request_async(self, method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"], url: str, body: dict|list, params: dict = None) -> dict | list:
        if method not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
            raise ValueError(f"Invalid method {method}")
        if method != "GET" and not self._config.editable:
            raise Exception("Client is not editable")
        res = await self._async_client.request(method, url, params=params, json=body)
        try:
            res.raise_for_status()
            LOGGER.info(f"{method} {url} [{res.status_code}] {body}")
        except httpx.HTTPStatusError as e:
            msg = f"{method} {url} [{res.status_code}] {body}"
            msg_json = res.json() if res.headers.get("Content-Type") == "application/json" else None
            if msg_json:
                msg += f" -> {msg_json}"
            LOGGER.error(msg)
            raise HTTPStatusException(f"Status code {res.status_code} for {method} {url}" + f": {msg_json}" if msg_json else "")
        return res.json() if res.text else None
    
    def _request_sync(self, method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"], url: str, body: dict|list, params: dict) -> dict | list:
        if method not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
            raise ValueError(f"Invalid method {method}")
        if method != "GET" and not self._config.editable:
            raise Exception("Client is not editable")
        res = self._sync_client.request(method, url, params=params, json=body)
        try:
            res.raise_for_status()
            LOGGER.info(f"{method} {url} [{res.status_code}]")
        except httpx.HTTPStatusError as e:
            msg = f"{method} {url} [{res.status_code}] {body}"
            msg_json = res.json() if res.headers.get("Content-Type") == "application/json" else None
            if msg_json:
                msg += f" -> {msg_json}"
            LOGGER.error(msg)
            raise HTTPStatusException(f"Status code {res.status_code} for {method} {url}" + f": {msg_json}" if msg_json else "")
        return res.json()
    
    def get_and_set_data(self, identifier: str, type_validate: type|None, content: dict|None = None, register: bool = True) -> IdentifiableBase:
        """Get from cache / create object with identifier and set data if provided

        Args:
            identifier (str): Identifier, usually the url of the object
            type_validate (type | None): Type to validate the object against. Defaults to None.
            content (dict | None, optional): Content to update the object. Defaults to None.

        Raises:
            ValueError: when the object is not a subclass of type_validate

        Returns:
            IdentifiableBase: the newly created / retrieved object
        """
        obj = self._cache.get(identifier)
        if obj is None:
            from .route_model import route_model
            cls = route_model(identifier)
            # Validate against type_validate if provided
            if type_validate is not None and not issubclass(cls, type_validate):
                raise ValueError(f"Inferred object with identifier {identifier} is not a subclass of {type_validate}")
            obj = cls._from_client(self)
            obj._href = identifier
            if register:
                self._cache.set(identifier, obj)
        elif type_validate is not None and not isinstance(obj, type_validate):
            raise ValueError(f"Cached object with identifier {identifier} is not an instance of {type_validate}")
        if content is not None:
            obj.update_data(content)
            obj._loaded = True
        return obj

from . import models