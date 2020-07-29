# MGIS Cloud optimize geotiff service.

Only Crop selected:
`GET`

```
http://${MARS_API_URL}/api/v1/cog/raster/{z}/{x}/{y}.png?mask=raster_${crop}_production_webmerc_cog.tif
```

Only risk selected:
`GET`

```
http://${MARS_API_URL}/api/v1/cog/raster/{z}/{x}/{y}.png?data=raster_aqueduct3_bws_webmerc_cog.tif
```

Risk and Crop selected:
`GET`

```
http://${MARS_API_URL}/api/v1/cog/raster/{z}/{x}/{y}.png?data=raster_aqueduct3_bws_webmerc_cog.tif&mask=raster_${crop}_production_webmerc_cog.tif
```

Interactivity:
`GET`

```
http://${MARS_API_URL}/api/v1/cog/raster/point/?data=raster_aqueduct3_bws_webmerc_cog.tif&lat=-14379964&long=-11880235&mask=raster_${crop}_production_webmerc_cog.tif
```