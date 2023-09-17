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

    kitchen_types_in = MapCompose(str.strip, fix_whitespaces, normalize_str)
    kitchen_types_out = Join(', ')

    social_media_in = MapCompose(str.strip, fix_whitespaces, normalize_str)
    social_media_out = Identity()

    phone_in = MapCompose(str.strip, format_number)

    working_hours_out = Identity()
    
    reviews_out = Identity()

    menu_positions_out = Identity()


class LocationLoader(ItemLoader):
    default_output_processor = TakeFirst()

    coordinates_in = MapCompose(str.strip, float)
    coordinates_out = Identity()


class AddressLoader(ItemLoader):
    default_output_processor = TakeFirst()

    street_in = MapCompose(str.strip, fix_whitespaces, normalize_str)
    zip_in = MapCompose(str.strip, fix_whitespaces)
    city_in = MapCompose(str.strip, fix_whitespaces, normalize_str)


class WorkingHoursLoader(ItemLoader):
    default_output_processor = TakeFirst()

    open_time_in = MapCompose(str.strip)

    close_time_in = MapCompose(str.strip)


class MenuLoader(ItemLoader):
    default_output_processor = TakeFirst()

    name_in = MapCompose(str.strip, fix_whitespaces, normalize_str)
    name_out = Join()

    price_in = MapCompose(str.strip, float)

    currency_in = MapCompose(str.strip, str.upper)

    description_in = MapCompose(str.strip, fix_whitespaces, normalize_str)
    description_out = Join()

    category_in = MapCompose(w3h.remove_tags, str.strip, fix_whitespaces)
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