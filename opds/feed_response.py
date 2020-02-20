from flask import make_response
from .opds_writer import OPDSFeed

def feed_response(content, acquisition=True, cache_for=600):
    content_type=OPDSFeed.FEED_TYPE

    if isinstance(cache_for, int):
        # A CDN should hold on to the cached representation only half
        # as long as the end-user.
        client_cache = cache_for
        cdn_cache = cache_for / 2
        cache_control = "public, no-transform, max-age=%d, s-maxage=%d" % (
            client_cache, cdn_cache)
    else:
        cache_control = "private, no-cache"

    return make_response(content, 200, {"Content-Type": content_type,
                                        "Cache-Control": cache_control})

