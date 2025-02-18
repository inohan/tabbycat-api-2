from urllib.parse import urlparse, urlunparse
from dataclasses import dataclass, field
from .cache import BaseCache, ApiCache

CONFIG_NULL_EXCEPTION: bool = True # Whether to raise an exception when a NULL value is accessed
CONFIG_LAZY_LOAD: bool = True # Whether to load unloaded objects when their attributes are accessed
CONFIG_FAILED_REQUESTS_EXCEPTION: bool = True # Whether to skip failed requests or raise an exception

def set_tabbycat_config(*, null_exception: bool|None = None, lazy_load: bool|None = None, failed_requests_exception: bool|None = None):
    global CONFIG_NULL_EXCEPTION, CONFIG_LAZY_LOAD, CONFIG_FAILED_REQUESTS_EXCEPTION
    if null_exception is not None:
        CONFIG_NULL_EXCEPTION = null_exception
    if lazy_load is not None:
        CONFIG_LAZY_LOAD = lazy_load
    if failed_requests_exception is not None:
        CONFIG_FAILED_REQUESTS_EXCEPTION = failed_requests_exception

@dataclass(frozen=True)
class ClientConfig:
    base_url: str
    api_token: str|None = None
    editable: bool = False
    httpx_timeout: float = 5.0
    httpx_semaphore: int = 10
    cache: BaseCache = field(default_factory=ApiCache)
    
    
    def __post_init__(self):
        parsed_url = urlparse(self.base_url)
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, "", "", "", ""))
        object.__setattr__(self, "base_url", new_url)