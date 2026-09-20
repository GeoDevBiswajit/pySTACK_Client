# pySTACK_Client
An easy-to-use Python toolkit for exploring, inspecting, and accessing geospatial data from STAC APIs with PySTAC Client.
pystac-client is mainly the discovery/search layer. It helps you answer
“What satellite data exists, where is it, when was it acquired, and what metadata/assets are available?”
                 STAC SEARCH
                     │
                     ▼
              Sentinel-2 Item
                     │
            ┌────────┴────────┐
            │                 │
            ▼                 ▼
      ANALYSIS MODE      DOWNLOAD MODE
            │                 │
            ▼                 ▼
        ODC-STAC           Rasterio
            │                 │
            ▼                 ▼
   Common analysis grid   Original grid
            │                 │
            ▼                 ▼
       xarray/Dask        GeoTIFF/COG
            │                 │
            ▼                 ▼
    NDVI/statistics/ML    User downloads