# Reviewarr
Reviewarr is a personal project to self-host a media rating service integrating with [Seerr](https://github.com/seerr-team/seerr) and [Jellyfin](https://github.com/jellyfin/jellyfin).

# `Work In Progress`

## Connect Jellyfin webhook

Install the native Jellyfin webhook plugin. Add a generic webhook with the following settings:
- **Name**: Reviewarr
- **URL**: `http://<REVIEWARR_HOST>:8000/webhook/jellyfin`
- **template**:
```json
{
  "NotificationType": "PlaybackStop",
  "Timestamp": "{{Date}}",
  "Server": {
    "Name": "{{{ServerName}}}",
    "Url": "{{ServerUrl}}"
  },
  "Session": {
    "User": "{{{NotificationUsername}}}",
    "UserId": "{{UserId}}",
    "Client": "{{{ClientName}}}",
    "Device": "{{{DeviceName}}}",
    "PlayedToCompletion": {{PlayedToCompletion}},
    "PlaybackPosition": "{{PlaybackPosition}}"
  }

  {{#if_equals ItemType 'Movie'}},
  "Media": {
    "ItemType": "Movie",
    "Title": "{{{Name}}}",
    "OriginalTitle": "{{{OriginalTitle}}}",
    "Year": "{{Year}}",
    "Runtime": "{{RunTime}}",
    "Overview": "{{{Overview}}}",
    "Tagline": "{{{Tagline}}}",
    "Genres": "{{{Genres}}}",
    "VideoCodec": "{{VideoCodec}}",
    "AudioCodec": "{{AudioCodec}}",
    "ExternalIds": {
      "IMDB": "{{Provider_imdb}}",
      "TMDB": "{{Provider_tmdb}}"
    }
  }
  {{/if_equals}}

  {{#if_equals ItemType 'Episode'}},
  "Media": {
    "ItemType": "Episode",
    "SeriesTitle": "{{{SeriesName}}}",
    "EpisodeTitle": "{{{Name}}}",
    "Season": "{{SeasonNumber00}}",
    "Episode": "{{EpisodeNumber00}}",
    "Year": "{{Year}}",
    "Runtime": "{{RunTime}}",
    "Overview": "{{{Overview}}}",
    "VideoCodec": "{{VideoCodec}}",
    "AudioCodec": "{{AudioCodec}}",
    "ExternalIds": {
      "TVDB": "{{Provider_tvdb}}",
      "IMDB": "{{Provider_imdb}}",
      "TMDB": "{{Provider_tmdb}}"
    }
  }
  {{/if_equals}}
}
```
