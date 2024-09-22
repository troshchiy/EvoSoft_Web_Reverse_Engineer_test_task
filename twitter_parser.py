import requests
import json


class TwitterParser:
    def __init__(self, username, proxy=None):
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'content-type': 'application/json',
            'origin': 'https://x.com',
            'priority': 'u=1, i',
            'referer': 'https://x.com/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-client-transaction-id': 'MW+p4NTQ+taxNr+xx2ndOdsBMucd81X919n3EjCPKZuAkzzVm2AsDGxjzb3wA83VPCebrDOlvRnskqddJJQF1STf08BFMg',
            # 'x-guest-token': None,
            'x-twitter-active-user': 'yes',
            'x-twitter-client-language': 'en',
        }
        self.username = username
        self.session = requests.Session()

        if proxy:
            self.session.proxies.update(proxy)

        response = self.session.post(
            'https://api.twitter.com/1.1/guest/activate.json',
            headers=self.headers
        )

        self.headers['x-guest-token'] = response.json().get('guest_token')

    def _get_user_id(self):
        variables = {"screen_name": self.username, "withSafetyModeUserFields": True}
        params = {
            'variables': json.dumps(variables),
            'features': '{"hidden_profile_subscriptions_enabled":true,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"subscriptions_feature_can_gift_premium":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
            'fieldToggles': '{"withAuxiliaryUserLabels":false}',
        }

        response = self.session.get(
            'https://api.x.com/graphql/Yka-W8dz7RaEuQNkroPkYw/UserByScreenName',
            params=params,
            headers=self.headers,
        )

        user_id = response.json().get('data', {}).get('user', {}).get('result', {}).get('rest_id')

        return user_id

    def get_user_tweets(self):
        variables = {
            "userId": self._get_user_id(),
            "count": 100,
            "includePromotedContent": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withVoice": True,
            "withV2Timeline": True
        }
        params = {
            'variables': json.dumps(variables),
            'features': '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
            'fieldToggles': '{"withAuxiliaryUserLabels":false}',
        }

        response = self.session.get(
            'https://api.x.com/graphql/E3opETHurmVJflFsUBVuUQ/UserTweets',
            params=params,
            headers=self.headers
        )

        response_json = response.json()

        timeline = response_json.get('data', {}).get('user', {}).get('result', {}).get('timeline_v2', {}).get('timeline', {}).get('instructions', [])
        entries = [x.get('entries') for x in timeline if x.get('type') == 'TimelineAddEntries']
        entries = entries[0] if entries else []

        tweets = []
        for entrie in entries:
            entrie_content = entrie.get('content', {})
            entrie_type = entrie_content.get('entryType')

            if entrie_type == 'TimelineTimelineItem':
                legacy = entrie_content.get('itemContent', {}).get('tweet_results', {}).get('result', {}).get('legacy', {})
                tweet = {
                    'id': legacy.get('id_str'),
                    'created_at': legacy.get('created_at'),
                    'content': legacy.get('full_text'),
                    'bookmark_count': legacy.get('bookmark_count'),
                    'quote_count': legacy.get('quote_count'),
                    'reply_count': legacy.get('reply_count'),
                    'retweet_count': legacy.get('retweet_count')
                }
                tweets.append(tweet)

        return tweets


if __name__ == '__main__':
    proxy = {
        'http': '9gfV4Q:gcKYdc@45.92.22.226:8000',
        'https': '9gfV4Q:gcKYdc@45.92.22.226:8000'
    }

    twitter_parser = TwitterParser('elonmusk', proxy=proxy)
    tweets = twitter_parser.get_user_tweets()

    for tweet in tweets[:10]:
        print(tweet['content'])
