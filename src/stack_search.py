from pystac_client import Client
from config import URL_PC
import planetary_computer

class STACKSearcher:
    """Search and inspect collections from a STAC API."""

    def __init__(self, stac_api=URL_PC, headers=None):
        """
        Initialize a STAC client.

        Args:
            stac_api (str): STAC API URL.
            headers (dict | None): Optional HTTP headers.
        """
        self.client = Client.open(
            stac_api,
            headers=headers
        )

    @property
    def all_collections(self):
        """Return all collection IDs available in the STAC API."""
        return [
            collection.id
            for collection in self.client.get_collections()
        ]

    def search_collection(self, text: str):
        """
        Search collections by name/description.

        Args:
            text (str): Search text, e.g. "sentinel" or "landsat".

        Returns:
            list[str]: Matching collection IDs.
        """
        return [
            collection.id
            for collection in self.client.collection_search(q=text).collections()
        ]

    def get_collection(self, collection_id: str):
        """
        Return a STAC Collection object.

        Args:
            collection_id (str): Collection ID.

        Returns:
            pystac.Collection: STAC collection.
        """
        return self.client.get_collection(collection_id)

    def get_queryables(self, collection_id: str):
        """
        Return queryable property names for a collection.

        Args:
            collection_id (str): Collection ID.

        Returns:
            list[str]: Queryable property names.
        """
        collection = self.get_collection(collection_id)
        queryables = collection.get_queryables()

        return list(queryables["properties"].keys())

    def search_items(
        self,
        collection_id=None,
        geometry=None,
        start_date=None,
        end_date=None,
        sign=True,
        **kwargs
    ):
        """
        Search STAC items using collection, spatial, temporal,
        and additional STAC API filters.

        Args:
            collection_id (str | list[str] | None):
                STAC collection ID or list of collection IDs.
                Example:
                    "sentinel-2-l2a"

            geometry (dict | None):
                GeoJSON geometry used as the spatial filter.
                Example:
                    mapping(gdf.geometry.iloc[0])

            start_date (str | None):
                Start date in ISO format.
                Example:
                    "2025-01-01"

            end_date (str | None):
                End date in ISO format.
                Example:
                    "2025-03-01"

            sign (bool):
                If True, sign the returned assets using
                Planetary Computer's signing service.
                Default is True.

            **kwargs:
                Additional arguments passed directly to
                pystac-client's Client.search() method.

                Common examples include:
                    bbox
                    datetime
                    ids
                    collections
                    intersects
                    query
                    filter
                    filter_lang
                    max_items
                    limit

        Returns:
            list[pystac.Item]:
                List of STAC Items matching the search criteria.

        Raises:
            ValueError:
                If the date range is incomplete.
        """

        # Build datetime range
        if start_date and end_date:
            datetime_range = f"{start_date}/{end_date}"
        elif start_date or end_date:
            raise ValueError(
                "Both start_date and end_date must be provided."
            )
        else:
            datetime_range = None

        # Build search parameters
        search_params = {
            "collections": collection_id,
            "intersects": geometry,
            "datetime": datetime_range,
            **kwargs
        }

        # Remove parameters that were not provided
        search_params = {
            key: value
            for key, value in search_params.items()
            if value is not None
        }

        # Execute STAC search
        search_instance = self.client.search(**search_params)

        # Get matching items
        items = list(search_instance.items())

        # Sign assets if requested
        if sign:
            items = [
                planetary_computer.sign(item)
                for item in items
            ]

        return items

if __name__ == "__main__":

    client = STACKSearcher()

    print(client.all_collections)

    print(
        client.search_collection("sentinel")
    )

    collection = client.get_collection("sentinel-2-l2a")

    print(collection.description)

    print(
        client.get_queryables("sentinel-2-l2a")
    )
