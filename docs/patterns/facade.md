
## What Problem Did We Have?
When the dashboard opens, it needs a lot of different information:
- Location details and zones
- Which devices belong to each zone
- The latest sensor readings
- The current automation strategy and its recommendation

If the frontend had to make four or five separate API calls to get all this, or if our API router had to talk to five different repositories at once, the code would get messy and slow down.

## How Did Facade Fix It?
We created one single class called `LocationOverviewFacade`. 

Instead of making the frontend or API router fetch everything piece by piece, they just make one call to `GET /api/locations/{location_id}/overview`. The Facade works behind the scenes to collect all the needed data, combine it into one clean `LocationOverviewDto` response, and send it back.

## Key Design Details
- **One Entry Point:** The API router only talks to `LocationOverviewFacade`. It does not talk to individual repositories.
- **Dynamic Recommendation:** The recommendation (`irrigate` or `wait`) is calculated fresh on every request using the saved strategy key. We do not store static recommendations in a new database table.
- **Fast Queries:** We fetch assigned devices and the newest reading for each device in batch queries instead of running a separate database search for every single device inside a loop.
- **No New Tables:** This pattern uses data we already saved in earlier phases, so no new database migration was needed.