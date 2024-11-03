from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeTranscriptFetcher:
    @staticmethod
    def get_transcript(video_id):
        YouTubeTranscriptApi.get_transcript(video_id,
                                            languages=['en', 'af', 'sq', 'am', 'ar', 'hy', 'az', 'bn', 'eu', 'be', 'bs',
                                                       'bg', 'my',
                                                       'ca', 'ceb', 'zh-Hans', 'zh-Hant', 'co', 'hr', 'cs', 'da', 'nl',
                                                       'eo', 'et', 'fil', 'fi', 'fr', 'gl', 'ka', 'de', 'el', 'gu',
                                                       'ht',
                                                       'ha', 'haw',
                                                       'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja',
                                                       'jv',
                                                       'kn', 'kk', 'km', 'rw', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt',
                                                       'lb', 'mk',
                                                       'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'ne', 'no', 'ny', 'or',
                                                       'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'sn',
                                                       'sd', 'si',
                                                       'sk', 'sl', 'so', 'st', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'tt',
                                                       'te', 'th', 'tr', 'tk', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'fy',
                                                       'xh', 'yi',
                                                       'yo', 'zu'])

        transcript = YouTubeTranscriptApi.get_transcript(video_id,
                                                         languages=['en', 'af', 'sq', 'am', 'ar', 'hy', 'az', 'bn',
                                                                    'eu',
                                                                    'be', 'bs', 'bg', 'my',
                                                                    'ca', 'ceb', 'zh-Hans', 'zh-Hant', 'co', 'hr', 'cs',
                                                                    'da', 'nl', 'eo', 'et', 'fil', 'fi', 'fr', 'gl',
                                                                    'ka',
                                                                    'de', 'el', 'gu', 'ht', 'ha', 'haw',
                                                                    'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga',
                                                                    'it',
                                                                    'ja', 'jv', 'kn', 'kk', 'km', 'rw', 'ko', 'ku',
                                                                    'ky',
                                                                    'lo', 'la', 'lv', 'lt', 'lb', 'mk',
                                                                    'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'ne',
                                                                    'no',
                                                                    'ny', 'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro',
                                                                    'ru',
                                                                    'sm', 'gd', 'sr', 'sn', 'sd', 'si',
                                                                    'sk', 'sl', 'so', 'st', 'es', 'su', 'sw', 'sv',
                                                                    'tg',
                                                                    'ta', 'tt', 'te', 'th', 'tr', 'tk', 'uk', 'ur',
                                                                    'ug',
                                                                    'uz', 'vi', 'cy', 'fy', 'xh', 'yi',
                                                                    'yo', 'zu'])

        result = ""
        for i in transcript:
            result += ' ' + i['text']
        return str(result)