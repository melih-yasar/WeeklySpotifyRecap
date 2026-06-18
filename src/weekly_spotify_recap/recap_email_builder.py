"""Build the Spotify-style HTML email."""

from .config import PLAYLIST_URL
from .music_helpers import estimate_listening_hours


def build_top_artist_cards(enriched):
    """Build the table cells for the top artist cards."""
    cards = []

    for index, item in enumerate(enriched["artists"], start=1):
        image_html = artist_image(item)
        name_html = linked_text(item["artist"], item["spotify_url"])

        cards.append(f"""
        <td class="artist-card-cell" style="width:33.33%;padding:8px;vertical-align:top;">
            <div style="background:#181818;border:1px solid #282828;border-radius:18px;padding:18px;text-align:center;min-height:190px;">
                {image_html}
                <div style="font-size:11px;color:#1ed760;text-transform:uppercase;font-weight:800;">#{index} Artist</div>
                <div style="font-size:20px;color:#ffffff;font-weight:800;line-height:1.3;margin-top:8px;">{name_html}</div>
                <div style="font-size:15px;color:#1ed760;margin-top:8px;font-weight:700;">{item["plays"]}</div>
            </div>
        </td>
        """)

    return "".join(cards)


def build_top_track_rows(enriched):
    """Build table rows for top tracks."""
    rows = []

    for index, item in enumerate(enriched["tracks"], start=1):
        cover_html = cover_image(item["cover_url"], item["title"])
        title_html = linked_text(item["title"], item["spotify_url"])

        rows.append(track_or_album_row(index, cover_html, title_html, item["artist"], item["plays"]))

    return "".join(rows)


def build_top_album_rows(enriched):
    """Build table rows for top albums."""
    rows = []

    for index, item in enumerate(enriched["albums"], start=1):
        cover_html = cover_image(item["cover_url"], item["album"])
        album_html = linked_text(item["album"], item["spotify_url"])

        rows.append(track_or_album_row(index, cover_html, album_html, item["artist"], item["plays"]))

    return "".join(rows)


def build_html_email(summary, enriched, playlist_url=None):
    """Build the complete HTML email from summary and Spotify data."""
    data = email_data(summary, enriched, playlist_url)

    return email_page(f"""
        {brand_header()}
        {hero_section(data)}
        {stats_section(data)}
        {highlights_section(data)}
        {artists_section(enriched)}
        {tracks_section(enriched)}
        {albums_section(enriched)}
    """)


def email_data(summary, enriched, playlist_url):
    """Prepare values that are reused in multiple email sections."""
    busiest_day, busiest_day_plays = summary["busiest_day"]
    favorite_hour = summary["favorite_hour"]

    return {
        "summary": summary,
        "hero": enriched["hero"] or {},
        "top_artist": summary["top_artists"][0][0] if summary["top_artists"] else "No data",
        "top_track": summary["top_tracks"][0][0][1] if summary["top_tracks"] else "No data",
        "top_track_artist": summary["top_tracks"][0][0][0] if summary["top_tracks"] else "No data",
        "busiest_day": busiest_day,
        "busiest_day_plays": busiest_day_plays,
        "favorite_hour": f"{favorite_hour:02d}:00" if favorite_hour is not None else "Unknown",
        "listening_hours": estimate_listening_hours(summary["total_scrobbles"]),
        "playlist_link": playlist_url or PLAYLIST_URL,
    }


def email_page(content):
    """Wrap all email sections in the main HTML page layout."""
    return f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @media only screen and (max-width: 600px) {{
                .email-shell {{
                    width: 100% !important;
                    max-width: 100% !important;
                    border-radius: 0 !important;
                }}
                .section-padding {{
                    padding-left: 18px !important;
                    padding-right: 18px !important;
                }}
                .brand-cell {{
                    padding: 20px 18px 8px 18px !important;
                }}
                .hero-inner {{
                    padding: 24px !important;
                }}
                .hero-column {{
                    display: block !important;
                    width: 100% !important;
                    padding-right: 0 !important;
                }}
                .hero-title {{
                    font-size: 44px !important;
                }}
                .hero-card-cell {{
                    padding-top: 24px !important;
                }}
                .artist-card-cell {{
                    display: block !important;
                    width: 100% !important;
                    box-sizing: border-box !important;
                }}
                .media-index {{
                    width: 24px !important;
                    font-size: 12px !important;
                }}
                .media-cover-cell {{
                    width: 58px !important;
                    padding-right: 10px !important;
                }}
                .media-cover,
                .media-cover-placeholder {{
                    width: 50px !important;
                    height: 50px !important;
                    border-radius: 10px !important;
                }}
                .media-title {{
                    font-size: 15px !important;
                    overflow-wrap: anywhere !important;
                    word-break: break-word !important;
                }}
                .media-artist {{
                    font-size: 13px !important;
                    overflow-wrap: anywhere !important;
                    word-break: break-word !important;
                }}
                .media-count {{
                    width: 44px !important;
                    min-width: 44px !important;
                    font-size: 13px !important;
                }}
            }}
        </style>
    </head>
    <body style="margin:0;padding:0;background:#0b0b0b;font-family:Arial,Helvetica,sans-serif;">
        <div style="background:#0b0b0b;padding:26px 12px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                    <td align="center">
                        <table class="email-shell" role="presentation" width="760" cellspacing="0" cellpadding="0" border="0" style="width:100%;max-width:760px;background:#111111;border-radius:30px;overflow:hidden;">
                            {content}
                        </table>
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """


def brand_header():
    """Build the top brand bar."""
    return """
    <tr>
        <td class="brand-cell" style="padding:26px 34px 4px 34px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                    <td style="vertical-align:middle;">
                        <div style="font-size:15px;color:#ffffff;font-weight:900;line-height:1;">
                            <span style="display:inline-block;width:14px;height:14px;background:#1ed760;border-radius:50%;vertical-align:-2px;margin-right:8px;"></span>
                            Spotify Recap
                        </div>
                    </td>
                    <td align="right" style="vertical-align:middle;font-size:11px;color:#a7a7a7;text-transform:uppercase;font-weight:700;">
                        Last 7 days
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    """


def hero_section(data):
    """Build the green hero section at the top of the email."""
    return f"""
    <tr>
        <td class="section-padding" style="padding:18px 34px 26px 34px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#1ed760;border-radius:28px;">
                <tr>
                    <td class="hero-inner" style="padding:34px;background:linear-gradient(160deg,#1ed760 0%,#0f6f35 45%,#121212 100%);border-radius:28px;">
                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                            <tr>
                                {hero_copy(data)}
                                {hero_card(data["hero"])}
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    """


def hero_copy(data):
    """Build the left side of the hero section."""
    return f"""
    <td class="hero-column" width="56%" valign="top" style="padding-right:18px;">
        <div style="font-size:12px;color:#d9ffe4;text-transform:uppercase;font-weight:900;">
            Weekly listening recap
        </div>
        <div class="hero-title" style="font-size:56px;line-height:0.95;font-weight:900;color:#ffffff;margin-top:16px;">
            Your week<br>sounded<br>like this
        </div>
        <div style="font-size:17px;line-height:1.65;color:#ebfff2;margin-top:22px;max-width:360px;">
            A fresh recap of your top songs, artists, albums, and listening habits from the last 7 days.
        </div>
        <div style="margin-top:24px;background:#121212;border-radius:18px;padding:18px 20px;display:inline-block;">
            <div style="font-size:12px;color:#dfffea;text-transform:uppercase;letter-spacing:1px;">Most replayed track</div>
            <div style="font-size:24px;color:#ffffff;font-weight:800;line-height:1.25;margin-top:8px;">{data["top_track"]}</div>
            <div style="font-size:14px;color:#dfffea;margin-top:6px;">by {data["top_track_artist"]}</div>
        </div>
        {playlist_button(data["playlist_link"])}
    </td>
    """


def hero_card(hero):
    """Build the latest-listen card in the hero section."""
    return f"""
    <td class="hero-column hero-card-cell" width="44%" valign="middle" align="center">
        <div style="background:#121212;border:1px solid rgba(255,255,255,0.12);border-radius:24px;padding:22px;text-align:center;">
            <div style="width:180px;margin:0 auto;">
                {hero_image(hero)}
            </div>
            <div style="font-size:11px;color:#1ed760;text-transform:uppercase;font-weight:900;margin-top:14px;">
                Latest listen
            </div>
            <div style="font-size:18px;color:#ffffff;font-weight:800;line-height:1.35;margin-top:6px;">
                {hero.get("title", "")}
            </div>
            <div style="font-size:13px;color:#dfffea;line-height:1.4;margin-top:4px;">
                {hero.get("artist", "")}
            </div>
        </div>
    </td>
    """


def stats_section(data):
    """Build the three stat cards below the hero section."""
    return f"""
    <tr>
        <td class="section-padding" style="padding:0 34px 8px 34px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                    {stat_card("Total listens", data["summary"]["total_scrobbles"])}
                    {stat_card("Listening time", f'{data["listening_hours"]}h')}
                    {stat_card("Peak time", data["favorite_hour"])}
                </tr>
            </table>
        </td>
    </tr>
    """


def stat_card(label, value):
    """Build one small stat card."""
    return f"""
    <td width="33.33%" style="padding:8px;">
        <div style="background:#181818;border-top:4px solid #1ed760;border-radius:18px;padding:18px 20px;">
            <div style="font-size:12px;color:#9d9d9d;text-transform:uppercase;letter-spacing:1px;">{label}</div>
            <div style="font-size:28px;color:#ffffff;font-weight:900;margin-top:8px;">{value}</div>
        </div>
    </td>
    """


def highlights_section(data):
    """Build the weekly highlights text block."""
    summary = data["summary"]
    return f"""
    <tr>
        <td class="section-padding" style="padding:12px 34px 0 34px;">
            <div style="background:#181818;border:1px solid #282828;border-radius:24px;padding:26px;">
                <div style="font-size:12px;color:#1ed760;text-transform:uppercase;font-weight:900;">Made for your week</div>
                <div style="font-size:18px;line-height:1.8;color:#f1f1f1;margin-top:14px;">
                    You listened to <span style="color:#1ed760;font-weight:800;">{summary["total_scrobbles"]}</span> tracks this week.
                    Your soundtrack was led by <span style="color:#ffffff;font-weight:800;">{data["top_artist"]}</span>.
                    Your biggest listening day was <span style="color:#ffffff;font-weight:800;">{data["busiest_day"]}</span> with
                    <span style="color:#1ed760;font-weight:800;">{data["busiest_day_plays"]} tracks</span>.
                </div>
            </div>
        </td>
    </tr>
    """


def artists_section(enriched):
    """Build the top artists section."""
    return section_with_table("Your top artists", f"<tr>{build_top_artist_cards(enriched)}</tr>")


def tracks_section(enriched):
    """Build the top tracks section."""
    return dark_table_section("Your top tracks", build_top_track_rows(enriched))


def albums_section(enriched):
    """Build the top albums section."""
    return dark_table_section("Your top albums", build_top_album_rows(enriched), last=True)


def section_with_table(title, rows):
    """Build a normal section containing a table."""
    return f"""
    <tr>
        <td class="section-padding" style="padding:28px 34px 0 34px;">
            <div style="font-size:13px;color:#ffffff;text-transform:uppercase;font-weight:900;">
                {title}
            </div>
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-top:10px;">
                {rows}
            </table>
        </td>
    </tr>
    """


def dark_table_section(title, rows, last=False):
    """Build a dark card section containing table rows."""
    padding = "28px 34px 34px 34px" if last else "28px 34px 0 34px"
    return f"""
    <tr>
        <td class="section-padding" style="padding:{padding};">
            <div style="font-size:13px;color:#ffffff;text-transform:uppercase;font-weight:900;">
                {title}
            </div>
            <div style="background:#181818;border:1px solid #282828;border-radius:24px;padding:22px;margin-top:12px;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                    {rows}
                </table>
            </div>
        </td>
    </tr>
    """


def hero_image(hero):
    """Build the latest-listen image or a placeholder."""
    cover = hero.get("cover_url")
    link = hero.get("spotify_url")

    if cover and link:
        return f'''
        <a href="{link}" style="text-decoration:none;">
            <img src="{cover}" alt="Album cover"
                 style="display:block;width:180px;height:180px;object-fit:cover;border-radius:22px;border:0;">
        </a>
        '''

    if cover:
        return f'''
        <img src="{cover}" alt="Album cover"
             style="display:block;width:180px;height:180px;object-fit:cover;border-radius:22px;border:0;">
        '''

    return '<div style="width:180px;height:180px;border-radius:22px;background:#222222;"></div>'


def playlist_button(link):
    """Build the playlist button when a link is available."""
    if not link:
        return ""

    return f'''
    <div style="margin-top:24px;">
        <a href="{link}" style="
            display:inline-block;
            background:#1ed760;
            color:#0a0a0a;
            text-decoration:none;
            font-weight:800;
            padding:14px 22px;
            border-radius:999px;
            font-size:15px;">
            Open playlist on Spotify
        </a>
    </div>
    '''


def artist_image(item):
    """Build an artist image or a placeholder."""
    if item["image_url"]:
        return (
            f'<img src="{item["image_url"]}" alt="{item["artist"]}" '
            'style="width:88px;height:88px;border-radius:16px;object-fit:cover;display:block;margin:0 auto 14px auto;">'
        )

    return '<div style="width:88px;height:88px;border-radius:16px;background:#2a2a2a;display:block;margin:0 auto 14px auto;"></div>'


def cover_image(url, alt):
    """Build an album cover image or a placeholder."""
    if url:
        return f'<img class="media-cover" src="{url}" alt="{alt}" style="width:64px;height:64px;border-radius:12px;object-fit:cover;display:block;">'

    return '<div class="media-cover-placeholder" style="width:64px;height:64px;border-radius:12px;background:#2a2a2a;display:block;"></div>'


def linked_text(text, url):
    """Return linked text when a Spotify URL is available."""
    if url:
        return f'<a href="{url}" style="color:#ffffff;text-decoration:none;">{text}</a>'

    return text


def track_or_album_row(index, image_html, title_html, artist, count):
    """Build one reusable track or album table row."""
    return f"""
    <tr>
        <td class="media-index" style="padding:14px 0;color:#8f8f8f;font-size:14px;width:34px;">{index}</td>
        <td class="media-cover-cell" style="padding:14px 12px 14px 0;width:80px;">{image_html}</td>
        <td style="padding:14px 0;">
            <div class="media-title" style="font-size:17px;color:#ffffff;font-weight:700;line-height:1.35;overflow-wrap:anywhere;word-break:break-word;">{title_html}</div>
            <div class="media-artist" style="font-size:14px;color:#b3b3b3;margin-top:5px;overflow-wrap:anywhere;word-break:break-word;">{artist}</div>
        </td>
        <td class="media-count" style="padding:14px 0 14px 10px;text-align:right;color:#1ed760;font-size:15px;font-weight:700;width:52px;min-width:52px;white-space:nowrap;">{count}</td>
    </tr>
    """

