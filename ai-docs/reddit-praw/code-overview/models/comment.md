# Comment

_class_praw.models.Comment(_reddit:praw.Reddit_, _id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")|[None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")\=None_, _url:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")|[None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")\=None_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"),[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]|[None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")\=None_)

A class that represents a Reddit comment.

## Typical Attributes

**Note:** This table describes attributes that typically belong to objects of this class. PRAW dynamically provides the attributes that Reddit returns via the API. Since those attributes are subject to change on Reddit's end, PRAW makes no effort to document any new/removed/changed attributes, other than to instruct you on how to discover what is available. As a result, this table of attributes may not be complete. See Determine Available Attributes of an Object for detailed information.

If you would like to add an attribute to this table, feel free to open a [pull request](https://github.com/praw-dev/praw/pulls).

| Attribute | Description |
| --- | --- |
| `author` | Provides an instance of `Redditor`. |
| `body` | The body of the comment, as Markdown. |
| `body_html` | The body of the comment, as HTML. |
| `created_utc` | Time the comment was created, represented in [Unix Time](https://en.wikipedia.org/wiki/Unix_time). |
| `distinguished` | Whether or not the comment is distinguished. |
| `edited` | Whether or not the comment has been edited. |
| `id` | The ID of the comment. |
| `is_submitter` | Whether or not the comment author is also the author of the submission. |
| `link_id` | The submission ID that the comment belongs to. |
| `parent_id` | The ID of the parent comment (prefixed with `t1_`). If it is a top-level comment, this returns the submission ID instead (prefixed with `t3_`). |
| `permalink` | A permalink for the comment. `Comment` objects from the inbox have a `context` attribute instead. |
| `replies` | Provides an instance of `CommentForest`. |
| `saved` | Whether or not the comment is saved. |
| `score` | The number of upvotes for the comment. |
| `stickied` | Whether or not the comment is stickied. |
| `submission` | Provides an instance of `Submission`. The submission that the comment belongs to. |
| `subreddit` | Provides an instance of `Subreddit`. The subreddit that the comment belongs to. |
| `subreddit_id` | The subreddit ID that the comment belongs to. |

## Methods

### \_\_init\_\_(_reddit:praw.Reddit_, _id:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")|[None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")\=None_, _url:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")|[None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")\=None_, _\_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"),[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]|[None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")\=None_)

Initialize a `Comment` instance.

### award(_\*_, _gild\_type:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\='gid\_2'_, _is\_anonymous:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")\=True_, _message:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")\=None_) → [dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.11)")

Award the author of the item.

**Parameters:**
- **gild\_type** – Type of award to give. See table below for currently know global award types.
- **is\_anonymous** – If `True`, the authenticated user's username will not be revealed to the recipient.
- **message** – Message to include with the award.

**Returns:** A dict containing info similar to what is shown below:

```python
{
    "subreddit_balance": 85260,
    "treatment_tags": [],
    "coins": 8760,
    "gildings": {"gid_1": 0, "gid_2": 1, "gid_3": 0},
    "awarder_karma_received": 4,
    "all_awardings": [
        {
            "giver_coin_reward": 0,
            "subreddit_id": None,
            "is_new": False,
            "days_of_drip_extension": 0,
            "coin_price": 75,
            "id": "award_9663243a-e77f-44cf-abc6-850ead2cd18d",
            "penny_donate": 0,
            "coin_reward": 0,
            "icon_url": "https://www.redditstatic.com/gold/awards/icon/SnooClappingPremium_512.png",
            "days_of_premium": 0,
            "icon_height": 512,
            "tiers_by_required_awardings": None,
            "icon_width": 512,
            "static_icon_width": 512,
            "start_date": None,
            "is_enabled": True,
            "awardings_required_to_grant_benefits": None,
            "description": "For an especially amazing showing.",
            "end_date": None,
            "subreddit_coin_reward": 0,
            "count": 1,
            "static_icon_height": 512,
            "name": "Bravo Grande!",
            "icon_format": "APNG",
            "award_sub_type": "PREMIUM",
            "penny_price": 0,
            "award_type": "global",
            "static_icon_url": "https://i.redd.it/award_images/t5_q0gj4/59e02tmkl4451_BravoGrande-Static.png",
        }
    ],
}
```

**Warning:** Requires the authenticated user to own Reddit Coins. Calling this method will consume Reddit Coins.

**Example usage:**
```python
# Award the gold award anonymously
comment = reddit.comment("dkk4qjd")
comment.award()

submission = reddit.submission("8dmv8z")
submission.award()

# Award the platinum award with message and reveal username
comment = reddit.comment("dkk4qjd")
comment.award(gild_type="gild_3", message="Nice!", is_anonymous=False)

submission = reddit.submission("8dmv8z")
submission.award(gild_type="gild_3", message="Nice!", is_anonymous=False)
```

#### Known Global Awards (as of 11/08/2021)

| Name | Icon | Gild Type | Description | Cost |
| --- | --- | --- | --- | --- |
| Silver |  | gid_1 | Shows the Silver Award… and that's it. | 100 |
| Gold |  | gid_2 | Gives 100 Reddit Coins and a week of r/lounge access and ad-free browsing. | 500 |
| Platinum |  | gid_3 | Gives 700 Reddit Coins and a month of r/lounge access and ad-free browsing. | 1800 |
| LOVE! |  | award_5eac457f-ebac-449b-93a7-eb17b557f03c | When you follow your heart, love is the answer | 20 |
| Starstruck |  | award_abb865cf-620b-4219-8777-3658cf9091fb | Can't stop seeing stars | 20 |
| All-Seeing Upvote |  | award_b4ff447e-05a5-42dc-9002-63568807cfe6 | A glowing commendation for all to see | 30 |
| Narwhal Salute |  | award_a2506925-fc82-4d6c-ae3b-b7217e09d7f0 | A golden splash of respect | 30 |
| Wholesome Seal of Approval |  | award_c4b2e438-16bb-4568-88e7-7893b7662944 | A glittering stamp for a feel-good thing | 30 |
| Ally |  | award_69c94eb4-d6a3-48e7-9cf2-0f39fed8b87c | Listen, get educated, and get involved. | 50 |
| Take My Energy |  | award_02d9ab2c-162e-4c01-8438-317a016ed3d9 | I'm in this with you. | 50 |
| Wearing is Caring |  | award_80d4d339-95d0-43ac-b051-bc3fe0a9bab8 | Keep the community and yourself healthy and happy. | 50 |
| Facepalm |  | award_b1b44fa1-8179-4d84-a9ed-f25bb81f1c5f | _Lowers face into palm_ | 70 |
| Snek |  | award_99d95969-6100-45b2-b00c-0ec45ae19596 | A smol, delicate danger noodle. | 70 |
| Tree Hug |  | award_b92370bb-b7de-4fb3-9608-c5b4a22f714a | Show nature some love. | 70 |
| Bravo Grande! |  | award_9663243a-e77f-44cf-abc6-850ead2cd18d | For an especially amazing showing. | 75 |
| Party Train |  | award_75f9bc56-eba3-4988-a1af-aec974404a0b | All aboard! Every five Party Train Awards gives the author 100 Reddit Coins and a week of r/lounge access and ad-free browsing. Rack up the awards and watch the train level-up! | 75 |
| Take My Power |  | award_92cb6518-a71a-4217-9f8f-7ecbd7ab12ba | Add my power to yours. | 75 |
| Defeated |  | award_58ef8551-8c27-4f03-afa5-748432194e3d | The process of taking a painful L | 80 |
| Hugz |  | award_8352bdff-3e03-4189-8a08-82501dd8f835 | Everything is better with a good hug | 80 |
| 'MURICA |  | award_869d4135-8738-41e5-8630-de593b4f049f | Did somebody say 'Murica? | 100 |
| Burning Cash |  | award_abcdefe4-c92f-4c66-880f-425962d17098 | I don't need it, I don't even necessarily want it, but I've got some cash to burn so I'm gonna get it. | 100 |
| Dread |  | award_81cf5c92-8500-498c-9c94-3e4034cece0a | Staring into the abyss and it's staring right back | 100 |
| Evil Cackle |  | award_483d8e29-bbe5-404e-a09a-c2d7b16c4fff | Laugh like a supervillain | 100 |
| Glow Up |  | award_01178870-6a4f-4172-8f36-9ed5092ee4f9 | You look amazing, glowing, incredible! | 100 |
| Heartwarming |  | award_19860e30-3331-4bac-b3d1-bd28de0c7974 | I needed this today | 100 |
| I am disappoint |  | award_03c4f93d-efc7-463b-98a7-c01814462ab0 | I'm not mad, I'm just disappointed. | 100 |
| I'll Drink to That |  | award_3267ca1c-127a-49e9-9a3d-4ba96224af18 | Let's sip to good health and good company | 100 |
| Keep Calm |  | award_1da6ff27-7c0d-4524-9954-86e5cda5fcac | Stop, chill, relax | 100 |
| Kiss |  | award_1e516e18-cbee-4668-b338-32d5530f91fe | You deserve a smooch | 100 |
| Lawyer Up |  | award_ae89e420-c4a5-47b8-a007-5dacf1c0f0d4 | OBJECTION! | 100 |
| Masterpiece |  | award_b4072731-c0fb-4440-adc7-1063d6a5e6a0 | C'est magnifique | 100 |
| Shocked |  | award_fbe9527a-adb3-430e-af1a-5fd3489e641b | I'm genuinely flabbergasted. | 100 |
| Tearing Up |  | award_43f3bf99-92d6-47ab-8205-130d26e7929f | This hits me right in the feels | 100 |
| Yummy |  | award_ae7f17fb-6538-4c75-9ff4-5f48b4cdaa94 | That looks so good | 100 |
| Faith In Humanity Restored |  | award_611ff347-196b-4a14-ad4b-0076f2d8f9d2 | This goes a long way to restore my faith in the people of Earth | 125 |
| Wholesome |  | award_5f123e3d-4f48-42f4-9c11-e98b566d5897 | When you come across a feel-good thing. | 125 |
| Beating Heart |  | award_0d762fb3-17e4-4477-ab6b-9770b71b493c | My valentine makes my heart beat out of my chest. | 150 |
| Bless Up |  | award_77ba55a2-c33c-4351-ac49-807455a80148 | Prayers up for the blessed. | 150 |
| Buff Doge |  | award_c42dc561-0b41-40b6-a23d-ef7e110e739e | So buff, wow | 150 |
| Cake |  | award_5fb42699-4911-42a2-884c-6fc8bdc36059 | Did someone say… cake? | 150 |
| Helpful |  | award_f44611f1-b89e-46dc-97fe-892280b13b82 | Thank you stranger. Shows the award. | 150 |
| I Shy |  | award_beccaae0-d745-44f9-bc5c-3c9f8117699b | No matter how hard I try, I'm too shy to confess my love! | 150 |
| Press F |  | award_88fdcafc-57a0-48db-99cc-76276bfaf28b | To pay respects. | 150 |
| Take My Money |  | award_a7f9cbd7-c0f1-4569-a913-ebf8d18de00b | I'm buying what you're selling | 150 |
| 2020 Veteran |  | award_f0875744-15da-41ee-8591-b88e5a88c430 | A reward for making it through the most topsey- turvey year anyone can remember. Gives 100 coins to the recipient. | 200 |
| Baby Snoo |  | award_4d880932-4b45-4723-a964-5d749ace4df2 | Baby Snoo is back and cuter than ever | 200 |
| Giggle |  | award_e813313c-1002-49bf-ac37-e966710f605f | Innocent laughter | 200 |
| Got the W |  | award_8dc476c7-1478-4d41-b940-f139e58f7756 |  | 200 |
| I'd Like to Thank… |  | award_1703f934-cf44-40cc-a96d-3729d0b48262 | My kindergarten teacher, my cat, my mom, and you. | 200 |
| I'm Deceased |  | award_b28d9565-4137-433d-bb65-5d4aa82ade4c | Call an ambulance, I'm laughing too hard. | 200 |
| Looking |  | award_4922c1be-3646-4d62-96ea-19a56798df51 | I can't help but look. | 200 |
| Lurking |  | award_59ae34c0-14c8-4b16-a527-e157fac0a6c7 | Just seeing what's going on | 200 |
| Plus One |  | award_f7562045-905d-413e-9ed2-0a16d4bfe349 | You officially endorse and add your voice to the crowd. | 200 |
| Sidevote |  | award_cd297f1a-8368-4f5a-acb8-6ec96fc6e8d6 | Not an upvote, not a downvote, just an in-the- middle sidevote. | 200 |
| Stone Face |  | award_2c3bb816-f6fc-46e8-aaf7-2b196afffada | You got me stone faced | 200 |
| Stonks Falling |  | award_9ee30a8f-463e-4ef7-9da9-a09f270ec026 | Losing value fast. | 200 |
| Stonks Rising |  | award_d125d124-5c03-490d-af3d-d07c462003da | To the MOON. | 200 |
| 1UP |  | award_11be92ba-509e-46d3-991b-593239006521 | Extra life | 250 |
| Are You Serious? |  | award_ca888c60-cd8c-4875-97f1-b536dc35a9a5 | Are you being serious right now? | 250 |
| Are You Winning? |  | award_5641bae4-e690-4832-a498-4bd78da8b2b1 | Well, are you? | 250 |
| Awesome Answer |  | award_2adc49e8-d6c9-4923-9293-2bfab1648569 | For a winning take and the kind soul who nails a question. Gives %{coin_symbol}100 Coins to both the author and the community. | 250 |
| Big Brain Time |  | award_e71deb9c-a466-4743-9a73-48771c000077 | 2000 IQ | 250 |
| Calculating |  | award_242c4f2c-6f1c-4387-9b5b-d0249d6ecd36 | Something isn't adding up | 250 |
| Confetti |  | award_1671746c-49e2-4cdd-be4e-ec8892434278 | Party time, shower them with sparkly paper | 250 |
| Doom |  | award_e03a0c52-56b5-45df-bd6f-5f2da10cfdc5 | A sense of impending doom | 250 |
| Duck Dance |  | award_c3e02835-9444-4a7f-9e7f-206e8bf0ed99 | He do be dancing though | 250 |
| Endless Coolness |  | award_aac76dbe-2272-4fad-ac06-c077d2d9049e | Cool to the infinity | 250 |
| It's Cute! |  | award_cc540de7-dfdb-4a68-9acf-6f9ce6b17d21 | You made me UwU. | 250 |
| Laser Eyes |  | award_e1ed6fb9-f23e-4cb4-aad9-70c83e4b1924 |  | 250 |
| Mind Blown |  | award_9583d210-a7d0-4f3c-b0c7-369ad579d3d4 | When a thing immediately combusts your brain. Gives %{coin_symbol}100 Coins to both the author and the community. | 250 |
| Original |  | award_d306c865-0d49-4a36-a1ab-a4122a0e3480 | When something new and creative wows you. Gives %{coin_symbol}100 Coins to both the author and the community. | 250 |
| Pranked! |  | award_e2250c69-8bd9-4e2f-8fb7-e6630e6c5c8a | Cake direct to face | 250 |
| Respect |  | award_c8503d66-6450-40c5-963f-35ced99bd361 | Tip of my hat to you | 250 |
| That Smile |  | award_e11fc833-31fe-4c43-bde8-aead928b4b70 | Cute but creepy | 250 |
| Timeless Beauty |  | award_31260000-2f4a-4b40-ad20-f5aa46a577bf | Beauty that's forever. Gives %{coin_symbol}100 Coins each to the author and the community. | 250 |
| Today I Learned |  | award_a67d649d-5aa5-407e-a98b-32fd9e3a9696 | The more you know… Gives %{coin_symbol}100 Coins to both the author and the community. | 250 |
| Vibing |  | award_3f4e6f36-dacc-4919-b170-9d0201cd258f | I'm catching the vibration | 250 |
| Wink Wink |  | award_a8196b8f-1a76-4902-b324-b9473854dade | _nudge, nudge_ | 250 |
| Woah Dude |  | award_d88c5520-18d0-4ef0-9a36-41f8617584b0 | Sometimes you're left just going WOAH… | 250 |
| Yas Queen |  | award_d48aad4b-286f-4a3a-bb41-ec05b3cd87cc | YAAAAAAAAAAASSS. | 250 |
| You Dropped This |  | award_92d8645c-de2c-44ae-8cd7-7b0c6ab25297 | King | 250 |
| hehehehe |  | award_435a5692-f508-4b31-8083-ddc576f26ad3 | That's a little funny | 250 |
| Blow a Kiss |  | award_9ef35273-7942-4199-a76a-3d37f3b52a2e | _smooch_ | 300 |
| Coin Gift |  | award_3dd248bc-3438-4c5b-98d4-24421fd6d670 | Give the gift of %{coin_symbol}250 Reddit Coins. | 300 |
| Crab Rave |  | award_f7a4fd5e-7cd1-4c11-a1c9-c18d05902e81 | [Happy crab noises] | 300 |
| GOAT |  | award_cc299d65-77de-4828-89de-708b088349a0 | Historical anomaly - greatest in eternity. | 300 |
| Heartbreak |  | award_dc85c1f3-b5aa-4970-9a5d-40304252f79e | Suffering from a broken heart | 300 |
| Rocket Like |  | award_28e8196b-d4e9-45bc-b612-cd4c7d3ed4b3 | When an upvote just isn't enough, smash the Rocket Like. | 300 |
| Table Flip |  | award_3e000ecb-c1a4-49dc-af14-c8ac2029ca97 | ARGH! | 300 |
| This |  | award_68ba1ee3-9baf-4252-be52-b808c1e8bdc4 | THIS right here! Join together to give multiple This awards and see the award evolve in its display and shower benefits for the recipient. For every 3 This awards given to a post or comment, the author will get 250 coins. | 300 |
| Updoot |  | award_725b427d-320b-4d02-8fb0-8bb7aa7b78aa | Sometimes you just got to doot. | 300 |
| Wait What? |  | award_a3b7d374-68b4-4c77-8a57-e11fd6f26c06 | Hold up, what was that? | 300 |
| Spit-take |  | award_3409a4c0-ba69-43a0-be9f-27bc27c159cc | Shower them with laughs | 325 |
| Super Heart Eyes |  | award_6220ecfe-4552-4949-aa13-fb1fb7db537c | When the love is out of control. | 325 |
| Table Slap |  | award_9f928aff-c9f5-4e7e-aa91-8619dce60f1c | When laughter meets percussion | 325 |
| To The Stars |  | award_2bc47247-b107-44a8-a78c-613da21869ff | Boldly go where we haven't been in a long, long time. | 325 |
| Into the Magic Portal |  | award_2ff1fdd0-ff73-47e6-a43c-bde6d4de8fbd | Hope to make it to the other side. | 350 |
| Out of the Magic Portal |  | award_7fe72f36-1141-4a39-ba76-0d481889b390 | That was fun, but I'm glad to be back | 350 |
| Bravo! |  | award_84276b1e-cc8f-484f-a19c-be6c09adc1a5 | An amazing showing. | 400 |
| Doot 🎵 Doot |  | award_5b39e8fd-7a58-4cbe-8ca0-bdedd5ed1f5a | Sometimes you just got to dance with the doots. | 400 |
| Bless Up (Pro) |  | award_43c43a35-15c5-4f73-91ef-fe538426435a | Prayers up for the blessed. Gives %{coin_symbol}100 Coins to both the author and the community. | 500 |
| Brighten My Day |  | award_9591a26e-b2e4-4ef2-bed4-28ff69246691 | The clouds part and the sun shines through. Use the Brighten My Day Award to highlight comments that are a ray of sunshine. | 500 |
| Eureka! |  | award_65f78ca2-45d8-4cb6-bf79-a67beadf2e47 | Now that is a bright idea. Use the Eureka Award to highlight comments that are brilliant. | 500 |
| Heart Eyes |  | award_a9009ea5-1a36-42ae-aab2-5967563ee054 | For love at first sight. Gives %{coin_symbol}100 Coins to both the author and the community. | 500 |
| Helpful (Pro) |  | award_2ae56630-cfe0-424e-b810-4945b9145358 | Thank you stranger. Gives %{coin_symbol}100 Coins to both the author and the community. | 500 |
| Made Me Smile |  | award_a7a04d6a-8dd8-41bb-b906-04fa8f144014 | When you're smiling before you know it. Gives %{coin_symbol}100 Coins to both the author and the community. | 500 |
| Starry |  | award_0e957fb0-c8f1-4ba1-a8ef-e1e524b60d7d | Use the Starry Award to highlight comments that deserve to stand out from the crowd. | 500 |
| Wholesome (Pro) |  | award_1f0462ee-18f5-4f33-89cf-f1f79336a452 | When you come across a feel-good thing. Gives %{coin_symbol}100 Coins to both the author and the community. | 500 |
| Pot o' Coins |  | award_35c78e6e-507b-4f1d-b3d8-ed43840909a8 | The treasure at the end of the rainbow. Gives the author 800 Coins to do with as they please. | 1000 |
| Argentium |  | award_4ca5a4e6-8873-4ac5-99b9-71b1d5161a91 | Latin for distinguished, this award shimmers like silver and is stronger than steel. It's for those who deserve outsized recognition. Gives 2,500 Reddit Coins and three months of r/lounge access and ad-free browsing. | 20000 |
| Ternion All-Powerful |  | award_2385c499-a1fb-44ec-b9b7-d260f3dc55de | Legendary level, this award is a no holds barred celebration of something that hits you in the heart, mind, and soul. Some might call it unachievanium. Gives 5,000 Reddit Coins and six months of r/lounge access and ad-free browsing. | 50000 |

### block()

Block the user who sent the item.

**Note:** This method pertains only to objects which were retrieved via the inbox.

**Example usage:**
```python
comment = reddit.comment("dkk4qjd")
comment.block()

# or, identically:
comment.author.block()
```

### clear\_vote()

Clear the authenticated user's vote on the object.

**Note:** Votes must be cast by humans. That is, API clients proxying a human's action one-for-one are OK, but bots deciding how to vote on content or amplifying a human's vote are not. See the reddit rules for more details on what constitutes vote manipulation.

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.clear_vote()

comment = reddit.comment("dxolpyc")
comment.clear_vote()
```

### collapse()

Mark the item as collapsed.

**Note:** This method pertains only to objects which were retrieved via the inbox.

**Example usage:**
```python
inbox = reddit.inbox()

# select first inbox item and collapse it
message = next(inbox)
message.collapse()
```

**See also:** `uncollapse()`

### delete()

Delete the object.

**Example usage:**
```python
comment = reddit.comment("dkk4qjd")
comment.delete()

submission = reddit.submission("8dmv8z")
submission.delete()
```

### disable\_inbox\_replies()

Disable inbox replies for the item.

**Example usage:**
```python
comment = reddit.comment("dkk4qjd")
comment.disable_inbox_replies()

submission = reddit.submission("8dmv8z")
submission.disable_inbox_replies()
```

**See also:** `enable_inbox_replies()`

### downvote()

Downvote the object.

**Note:** Votes must be cast by humans. That is, API clients proxying a human's action one-for-one are OK, but bots deciding how to vote on content or amplifying a human's vote are not. See the reddit rules for more details on what constitutes vote manipulation.

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.downvote()

comment = reddit.comment("dxolpyc")
comment.downvote()
```

**See also:** `upvote()`

### edit(_body:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_) → praw.models.Comment|praw.models.Submission

Replace the body of the object with `body`.

**Parameters:**
- **body** – The Markdown formatted content for the updated object.

**Returns:** The current instance after updating its attributes.

**Example usage:**
```python
comment = reddit.comment("dkk4qjd")

# construct the text of an edited comment
# by appending to the old body:
edited_body = comment.body + "Edit: thanks for the gold!"
comment.edit(edited_body)
```

### enable\_inbox\_replies()

Enable inbox replies for the item.

**Example usage:**
```python
comment = reddit.comment("dkk4qjd")
comment.enable_inbox_replies()

submission = reddit.submission("8dmv8z")
submission.enable_inbox_replies()
```

**See also:** `disable_inbox_replies()`

### fullname _:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_ (Property)

Return the object's fullname.

A fullname is an object's kind mapping like `t3` followed by an underscore and the object's base36 ID, e.g., `t1_c5s96e0`.

### gild() → [dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.11)")

Alias for `award()` to maintain backwards compatibility.

### id\_from\_url(_url:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_) → [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)") (Static Method)

Get the ID of a comment from the full URL.

### is\_root _:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.11)")_ (Property)

Return `True` when the comment is a top-level comment.

### mark\_read()

Mark a single inbox item as read.

**Note:** This method pertains only to objects which were retrieved via the inbox.

**Example usage:**
```python
inbox = reddit.inbox.unread()

for message in inbox:
    # process unread messages
    ...
```

**See also:** `mark_unread()`

To mark the whole inbox as read with a single network request, use `Inbox.mark_all_read()`

### mark\_unread()

Mark the item as unread.

**Note:** This method pertains only to objects which were retrieved via the inbox.

**Example usage:**
```python
inbox = reddit.inbox(limit=10)

for message in inbox:
    # process messages
    ...
```

**See also:** `mark_read()`

### mod() → praw.models.reddit.comment.CommentModeration

Provide an instance of `CommentModeration`.

**Example usage:**
```python
comment = reddit.comment("dkk4qjd")
comment.mod.approve()
```

### parent() → Comment|praw.models.Submission

Return the parent of the comment.

The returned parent will be an instance of either `Comment`, or `Submission`.

If this comment was obtained through a `Submission`, then its entire ancestry should be immediately available, requiring no extra network requests. However, if this comment was obtained through other means, e.g., `reddit.comment("COMMENT_ID")`, or `reddit.inbox.comment_replies`, then the returned parent may be a lazy instance of either `Comment`, or `Submission`.

**Lazy comment example:**
```python
comment = reddit.comment("cklhv0f")
parent = comment.parent()
# 'replies' is empty until the comment is refreshed
print(parent.replies)  # Output: []
parent.refresh()
print(parent.replies)  # Output is at least: [Comment(id="cklhv0f")]
```

**Warning:** Successive calls to `parent()` may result in a network request per call when the comment is not obtained through a `Submission`. See below for an example of how to minimize requests.

If you have a deeply nested comment and wish to most efficiently discover its top-most `Comment` ancestor you can chain successive calls to `parent()` with calls to `refresh()` at every 9 levels. For example:

```python
comment = reddit.comment("dkk4qjd")
ancestor = comment
refresh_counter = 0
while not ancestor.is_root:
    ancestor = ancestor.parent()
    if refresh_counter % 9 == 0:
        ancestor.refresh()
    refresh_counter += 1
print(f"Top-most Ancestor: {ancestor}")
```

The above code should result in 5 network requests to Reddit. Without the calls to `refresh()` it would make at least 31 network requests.

### parse(_data:[Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.11)")\[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)"),[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)")\]_, _reddit:praw.Reddit_) → [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.11)") (Class Method)

Return an instance of `cls` from `data`.

**Parameters:**
- **data** – The structured data.
- **reddit** – An instance of `Reddit`.

### refresh()

Refresh the comment's attributes.

If using `Reddit.comment()` this method must be called in order to obtain the comment's replies.

**Example usage:**
```python
comment = reddit.comment("dkk4qjd")
comment.refresh()
```

### replies _:CommentForest_ (Property)

Provide an instance of `CommentForest`.

This property may return an empty list if the comment has not been refreshed with `refresh()`

Sort order and reply limit can be set with the `reply_sort` and `reply_limit` attributes before replies are fetched, including any call to `refresh()`:

```python
comment.reply_sort = "new"
comment.refresh()
replies = comment.replies
```

**Note:** The appropriate values for `reply_sort` include `"confidence"`, `"controversial"`, `"new"`, `"old"`, `"q&a"`, and `"top"`.

### reply(_body:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_) → praw.models.Comment|praw.models.Message|[None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")

Reply to the object.

**Parameters:**
- **body** – The Markdown formatted content for a comment.

**Returns:** A `Comment` or `Message` object for the newly created comment or message or `None` if Reddit doesn't provide one.

**Raises:** `prawcore.exceptions.Forbidden` when attempting to reply to some items, such as locked submissions/comments or non-replyable messages.

A `None` value can be returned if the target is a comment or submission in a quarantined subreddit and the authenticated user has not opt-ed into viewing the content. When this happens the comment will be successfully created on Reddit and can be retried by drawing the comment from the user's comment history.

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.reply("reply")

comment = reddit.comment("dxolpyc")
comment.reply("reply")
```

### report(_reason:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")_)

Report this object to the moderators of its subreddit.

**Parameters:**
- **reason** – The reason for reporting.

**Raises:** `RedditAPIException` if `reason` is longer than 100 characters.

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.report("report reason")

comment = reddit.comment("dxolpyc")
comment.report("report reason")
```

### save(_\*_, _category:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")|[None](https://docs.python.org/3/library/constants.html#None "(in Python v3.11)")\=None_)

Save the object.

**Parameters:**
- **category** – The category to save to. If the authenticated user does not have Reddit Premium this value is ignored by Reddit (default: `None`).

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.save(category="view later")

comment = reddit.comment("dxolpyc")
comment.save()
```

**See also:** `unsave()`

### submission _:praw.models.Submission_ (Property)

Return the `Submission` object this comment belongs to.

### unblock\_subreddit()

Unblock a subreddit.

**Note:** This method pertains only to objects which were retrieved via the inbox.

**Example:**
```python
from praw.models import SubredditMessage

subs = set()
for item in reddit.inbox.messages(limit=None):
    if isinstance(item, SubredditMessage):
        if (
            item.subject == "[message from blocked subreddit]"
            and str(item.subreddit) not in subs
        ):
            item.unblock_subreddit()
            subs.add(str(item.subreddit))
```

### uncollapse()

Mark the item as uncollapsed.

**Note:** This method pertains only to objects which were retrieved via the inbox.

**Example usage:**
```python
inbox = reddit.inbox()

# select first inbox item and uncollapse it
message = next(inbox)
message.uncollapse()
```

**See also:** `collapse()`

### unsave()

Unsave the object.

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.unsave()

comment = reddit.comment("dxolpyc")
comment.unsave()
```

**See also:** `save()`

### upvote()

Upvote the object.

**Note:** Votes must be cast by humans. That is, API clients proxying a human's action one-for-one are OK, but bots deciding how to vote on content or amplifying a human's vote are not. See the reddit rules for more details on what constitutes vote manipulation.

**Example usage:**
```python
submission = reddit.submission("5or86n")
submission.upvote()

comment = reddit.comment("dxolpyc")
comment.upvote()
```

**See also:** `downvote()`