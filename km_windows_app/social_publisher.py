from __future__ import annotations

import requests


def post_to_facebook(page_token: str, message: str) -> None:
    response = requests.post(
        "https://graph.facebook.com/v22.0/me/feed",
        data={"message": message, "access_token": page_token},
        timeout=30,
    )
    response.raise_for_status()


def post_to_instagram(ig_business_account_id: str, access_token: str, caption: str, image_url: str) -> None:
    create_resp = requests.post(
        f"https://graph.facebook.com/v22.0/{ig_business_account_id}/media",
        data={"caption": caption, "image_url": image_url, "access_token": access_token},
        timeout=30,
    )
    create_resp.raise_for_status()
    creation_id = create_resp.json()["id"]

    publish_resp = requests.post(
        f"https://graph.facebook.com/v22.0/{ig_business_account_id}/media_publish",
        data={"creation_id": creation_id, "access_token": access_token},
        timeout=30,
    )
    publish_resp.raise_for_status()


def post_to_tiktok(access_token: str, caption: str) -> None:
    # TikTok posting flows depend on app type; this endpoint is illustrative.
    response = requests.post(
        "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"post_info": {"title": caption}},
        timeout=30,
    )
    response.raise_for_status()
