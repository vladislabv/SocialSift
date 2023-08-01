import w3lib.html as w3h
from scrapy.loader import ItemLoader
from itemloaders.processors import (
    TakeFirst,
    MapCompose,
    Join,
    Identity,
)

from webscraper.utils import (
    fix_whitespaces,
    normalize_str,
    format_number,
    filter_empty,
    to_datetime
)


class RestoLoader(ItemLoader):
    default_output_processor = TakeFirst()

    name_in = MapCompose(w3h.remove_tags, str.strip, fix_whitespaces, normalize_str)
    name_out = Join()

    about_in = MapCompose(w3h.remove_tags, str.strip, fix_whitespaces, normalize_str)
    about_out = Join()

    kitchen_type_in = MapCompose(str.strip, fix_whitespaces, normalize_str)
    kitchen_type_out = Join(', ')

    opening_hours_in = MapCompose(str.strip, fix_whitespaces, normalize_str)
    opening_hours_out = Identity()

    social_media_in = MapCompose(str.strip, fix_whitespaces, normalize_str)
    social_media_out = Identity()

    address_in = MapCompose(str.strip, fix_whitespaces, normalize_str)

    zip_in = MapCompose(str.strip, fix_whitespaces)

    city_in = MapCompose(str.strip, fix_whitespaces, normalize_str)

    phone_in = MapCompose(str.strip, format_number)

    location_in = MapCompose(str.strip, float)
    location_out = Identity()


class MenuLoader(ItemLoader):
    default_output_processor = TakeFirst()

    name_in = MapCompose(str.strip, fix_whitespaces, normalize_str, filter_empty)
    name_out = Join()

    price_in = MapCompose(str.strip, float)

    currency_in = MapCompose(str.strip, str.upper)

    description_in = MapCompose(str.strip, fix_whitespaces, normalize_str, filter_empty)
    description_out = Join()

    category_in = MapCompose(w3h.remove_tags, str.strip, fix_whitespaces, filter_empty)
    category_out = Join(', ')


class ReviewLoader(ItemLoader):
    default_output_processor = TakeFirst()

    date_in = MapCompose(str.strip, to_datetime)

    rating_in = MapCompose(float)

    title_in = MapCompose(str.strip, fix_whitespaces, normalize_str)
    title_out = Join()

    text_in = MapCompose(w3h.remove_tags, str.strip, fix_whitespaces, normalize_str)
    text_out = Join()

    language_in = MapCompose(str.strip, str.upper)

    platform_in = MapCompose(str.strip, filter_empty)

    author_name_in = MapCompose(str.strip, fix_whitespaces, normalize_str)

    author_username_in = MapCompose(str.strip, fix_whitespaces, normalize_str)


class WebsiteLoader(ItemLoader):
    default_output_processor = TakeFirst()

    url_in = MapCompose(str.strip, fix_whitespaces, normalize_str)

    title_in = MapCompose(str.strip, fix_whitespaces, normalize_str)

    text_in = MapCompose(str.strip, fix_whitespaces, normalize_str)
    text_out = Join('|>|')

    snapshot_at_in = MapCompose(str.strip, to_datetime)


class WebFileLoader(ItemLoader):
    default_output_processor = Identity()