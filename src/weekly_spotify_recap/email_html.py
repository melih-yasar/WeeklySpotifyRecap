from .config import PLAYLIST_URL
from .helpers import estimate_listening_hours


def build_top_artist_cards(enriched):
    cards = []

    for index, item in enumerate(enriched["artists"], start=1):
        image_html = (
            f'<img src="{item["image_url"]}" alt="{item["artist"]}" '
            'style="width:88px;height:88px;border-radius:16px;object-fit:cover;display:block;margin:0 auto 14px auto;">'
            if item["image_url"]
            else '<div style="width:88px;height:88px;border-radius:16px;background:#2a2a2a;display:block;margin:0 auto 14px auto;"></div>'
        )

        name_html = (
            f'<a href="{item["spotify_url"]}" style="color:#ffffff;text-decoration:none;">{item["artist"]}</a>'
            if item["spotify_url"]
            else item["artist"]
        )

        cards.append(f"""
        <td style="width:33.33%;padding:8px;vertical-align:top;">
            <div style="background:#181818;border-radius:20px;padding:18px;text-align:center;min-height:190px;">
                {image_html}
                <div style="font-size:11px;color:#9f9f9f;letter-spacing:1px;text-transform:uppercase;">Top Artist #{index}</div>
                <div style="font-size:20px;color:#ffffff;font-weight:700;line-height:1.3;margin-top:8px;">{name_html}</div>
                <div style="font-size:15px;color:#1ed760;margin-top:8px;font-weight:700;">{item["plays"]} plays</div>
            </div>
        </td>
        """)

    return "".join(cards)


def build_top_track_rows(enriched):
    rows = []

    for index, item in enumerate(enriched["tracks"], start=1):
        cover_html = (
            f'<img src="{item["cover_url"]}" alt="{item["title"]}" style="width:64px;height:64px;border-radius:12px;object-fit:cover;display:block;">'
            if item["cover_url"]
            else '<div style="width:64px;height:64px;border-radius:12px;background:#2a2a2a;display:block;"></div>'
        )

        title_html = (
            f'<a href="{item["spotify_url"]}" style="color:#ffffff;text-decoration:none;">{item["title"]}</a>'
            if item["spotify_url"]
            else item["title"]
        )

        rows.append(f"""
        <tr>
            <td style="padding:14px 0;color:#8f8f8f;font-size:14px;width:34px;">{index}</td>
            <td style="padding:14px 0;width:80px;">{cover_html}</td>
            <td style="padding:14px 0;">
                <div style="font-size:17px;color:#ffffff;font-weight:700;line-height:1.35;">{title_html}</div>
                <div style="font-size:14px;color:#b3b3b3;margin-top:5px;">{item["artist"]}</div>
            </td>
            <td style="padding:14px 0;text-align:right;color:#1ed760;font-size:15px;font-weight:700;">{item["plays"]}</td>
        </tr>
        """)

    return "".join(rows)


def build_top_album_rows(enriched):
    rows = []

    for index, item in enumerate(enriched["albums"], start=1):
        cover_html = (
            f'<img src="{item["cover_url"]}" alt="{item["album"]}" style="width:64px;height:64px;border-radius:12px;object-fit:cover;display:block;">'
            if item["cover_url"]
            else '<div style="width:64px;height:64px;border-radius:12px;background:#2a2a2a;display:block;"></div>'
        )

        album_html = (
            f'<a href="{item["spotify_url"]}" style="color:#ffffff;text-decoration:none;">{item["album"]}</a>'
            if item["spotify_url"]
            else item["album"]
        )

        rows.append(f"""
        <tr>
            <td style="padding:14px 0;color:#8f8f8f;font-size:14px;width:34px;">{index}</td>
            <td style="padding:14px 0;width:80px;">{cover_html}</td>
            <td style="padding:14px 0;">
                <div style="font-size:17px;color:#ffffff;font-weight:700;line-height:1.35;">{album_html}</div>
                <div style="font-size:14px;color:#b3b3b3;margin-top:5px;">{item["artist"]}</div>
            </td>
            <td style="padding:14px 0;text-align:right;color:#1ed760;font-size:15px;font-weight:700;">{item["plays"]}</td>
        </tr>
        """)

    return "".join(rows)


def build_html_email(summary, enriched, playlist_url=None):
    top_artist = summary["top_artists"][0][0] if summary["top_artists"] else "No data"
    top_track = summary["top_tracks"][0][0][1] if summary["top_tracks"] else "No data"
    top_track_artist = summary["top_tracks"][0][0][0] if summary["top_tracks"] else "No data"
    busiest_day, busiest_day_plays = summary["busiest_day"]
    favorite_hour = (
        f"{summary['favorite_hour']:02d}:00"
        if summary["favorite_hour"] is not None
        else "Unknown"
    )
    listening_hours = estimate_listening_hours(summary["total_scrobbles"])

    hero = enriched["hero"] or {}
    hero_cover = hero.get("cover_url")
    hero_link = hero.get("spotify_url")
    playlist_link = playlist_url or PLAYLIST_URL

    hero_image_html = (
        f'''
        <a href="{hero_link}" style="text-decoration:none;">
            <img src="{hero_cover}" alt="Album cover"
                 style="display:block;width:180px;height:180px;object-fit:cover;border-radius:22px;border:0;">
        </a>
        '''
        if hero_cover and hero_link
        else f'''
        <img src="{hero_cover}" alt="Album cover"
             style="display:block;width:180px;height:180px;object-fit:cover;border-radius:22px;border:0;">
        '''
        if hero_cover
        else '''
        <div style="width:180px;height:180px;border-radius:22px;background:#222222;"></div>
        '''
    )

    playlist_block = (
        f'''
        <div style="margin-top:24px;">
            <a href="{playlist_link}" style="
                display:inline-block;
                background:#1ed760;
                color:#0a0a0a;
                text-decoration:none;
                font-weight:800;
                padding:14px 22px;
                border-radius:999px;
                font-size:15px;">
                Open your weekly playlist
            </a>
        </div>
        '''
        if playlist_link
        else ""
    )

    return f"""
    <html>
    <body style="margin:0;padding:0;background:#0b0b0b;font-family:Arial,Helvetica,sans-serif;">
        <div style="background:#0b0b0b;padding:26px 12px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                    <td align="center">
                        <table role="presentation" width="760" cellspacing="0" cellpadding="0" border="0" style="width:760px;max-width:760px;background:#111111;border-radius:30px;overflow:hidden;">

                            <tr>
                                <td style="padding:34px;">
                                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:linear-gradient(180deg,#1db954 0%,#138241 35%,#111111 100%);border-radius:26px;">
                                        <tr>
                                            <td style="padding:34px;">
                                                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                                    <tr>
                                                        <td width="56%" valign="top" style="padding-right:18px;">
                                                            <div style="font-size:12px;color:#d9ffe4;letter-spacing:2px;text-transform:uppercase;font-weight:700;">
                                                                Weekly listening recap
                                                            </div>

                                                            <div style="font-size:58px;line-height:0.95;font-weight:900;color:#ffffff;margin-top:18px;">
                                                                Your<br>week<br>in music
                                                            </div>

                                                            <div style="font-size:18px;line-height:1.7;color:#ebfff2;margin-top:22px;max-width:360px;">
                                                                Heavy rotation, repeat favorites, and the albums and tracks that defined your last 7 days.
                                                            </div>

                                                            <div style="margin-top:24px;background:rgba(0,0,0,0.18);border-radius:18px;padding:18px 20px;display:inline-block;">
                                                                <div style="font-size:12px;color:#dfffea;text-transform:uppercase;letter-spacing:1px;">Most replayed track</div>
                                                                <div style="font-size:24px;color:#ffffff;font-weight:800;line-height:1.25;margin-top:8px;">{top_track}</div>
                                                                <div style="font-size:14px;color:#dfffea;margin-top:6px;">by {top_track_artist}</div>
                                                            </div>

                                                            {playlist_block}
                                                        </td>

                                                        <td width="44%" valign="middle" align="center">
                                                            <div style="background:rgba(0,0,0,0.12);border-radius:28px;padding:24px;text-align:center;">
                                                                <div style="width:180px;margin:0 auto;">
                                                                    {hero_image_html}
                                                                </div>
                                                                <div style="font-size:12px;color:#dfffea;letter-spacing:1px;text-transform:uppercase;margin-top:14px;">
                                                                    Latest listen
                                                                </div>
                                                                <div style="font-size:17px;color:#ffffff;font-weight:700;line-height:1.35;margin-top:6px;">
                                                                    {hero.get("title", "")}
                                                                </div>
                                                                <div style="font-size:13px;color:#dfffea;line-height:1.4;margin-top:4px;">
                                                                    {hero.get("artist", "")}
                                                                </div>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <tr>
                                <td style="padding:0 34px 8px 34px;">
                                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                        <tr>
                                            <td width="33.33%" style="padding:8px;">
                                                <div style="background:#181818;border-radius:20px;padding:20px;">
                                                    <div style="font-size:12px;color:#9d9d9d;text-transform:uppercase;letter-spacing:1px;">Total plays</div>
                                                    <div style="font-size:28px;color:#ffffff;font-weight:900;margin-top:8px;">{summary["total_scrobbles"]}</div>
                                                </div>
                                            </td>
                                            <td width="33.33%" style="padding:8px;">
                                                <div style="background:#181818;border-radius:20px;padding:20px;">
                                                    <div style="font-size:12px;color:#9d9d9d;text-transform:uppercase;letter-spacing:1px;">Listening time</div>
                                                    <div style="font-size:28px;color:#ffffff;font-weight:900;margin-top:8px;">{listening_hours}h</div>
                                                </div>
                                            </td>
                                            <td width="33.33%" style="padding:8px;">
                                                <div style="background:#181818;border-radius:20px;padding:20px;">
                                                    <div style="font-size:12px;color:#9d9d9d;text-transform:uppercase;letter-spacing:1px;">Peak time</div>
                                                    <div style="font-size:28px;color:#ffffff;font-weight:900;margin-top:8px;">{favorite_hour}</div>
                                                </div>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <tr>
                                <td style="padding:12px 34px 0 34px;">
                                    <div style="background:#181818;border-radius:24px;padding:26px;">
                                        <div style="font-size:12px;color:#9d9d9d;text-transform:uppercase;letter-spacing:1.2px;">Highlights</div>
                                        <div style="font-size:18px;line-height:1.8;color:#f1f1f1;margin-top:14px;">
                                            You played <span style="color:#1ed760;font-weight:800;">{summary["total_scrobbles"]}</span> tracks this week.
                                            Your soundtrack was led by <span style="color:#ffffff;font-weight:800;">{top_artist}</span>.
                                            Your biggest listening day was <span style="color:#ffffff;font-weight:800;">{busiest_day}</span> with
                                            <span style="color:#1ed760;font-weight:800;">{busiest_day_plays} plays</span>.
                                        </div>
                                    </div>
                                </td>
                            </tr>

                            <tr>
                                <td style="padding:28px 34px 0 34px;">
                                    <div style="font-size:13px;color:#9d9d9d;text-transform:uppercase;letter-spacing:1.4px;">
                                        Top artists
                                    </div>
                                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-top:10px;">
                                        <tr>
                                            {build_top_artist_cards(enriched)}
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <tr>
                                <td style="padding:28px 34px 0 34px;">
                                    <div style="font-size:13px;color:#9d9d9d;text-transform:uppercase;letter-spacing:1.4px;">
                                        Top tracks
                                    </div>
                                    <div style="background:#181818;border-radius:24px;padding:22px;margin-top:12px;">
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                            {build_top_track_rows(enriched)}
                                        </table>
                                    </div>
                                </td>
                            </tr>

                            <tr>
                                <td style="padding:28px 34px 34px 34px;">
                                    <div style="font-size:13px;color:#9d9d9d;text-transform:uppercase;letter-spacing:1.4px;">
                                        Top albums
                                    </div>
                                    <div style="background:#181818;border-radius:24px;padding:22px;margin-top:12px;">
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                            {build_top_album_rows(enriched)}
                                        </table>
                                    </div>
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """
