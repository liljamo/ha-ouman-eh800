# HA Ouman EH-800

An Ouman EH-800 integration for Home Assistant.

Mostly kinda working™.

I'll add instructions after some more testing.

A demo video is available at [liljamo.dev/ha-ouman-eh800](https://liljamo.dev/ha-ouman-eh800/).

### What's supported

A very generic list would be:
- L1 operation mode control
- L1 temperature control, drop settings
- L1 manual drive
- Home/Away switch

Some extra data is available for reading via the attributes of the `l1_climate`
entity. E.g. some L1 heating curve values, but these may get controls at some point.

I don't have a second loop, so no L2 values are currently available.

I'll add all read-only values soon, but read-write values will require some more
thinking.


### Need help?

Contact me via one of the methods listed on [liljamo.com/contact](https://liljamo.com/contact/).

You can mention me on Matrix for a quick question or chat in:
- [#Home-Assistant:matrix.org](https://matrix.to/#/#Home-Assistant:matrix.org) (English)
- [#kotiautomaatio:hacklab.fi](https://matrix.to/#/#kotiautomaatio:hacklab.fi) (Finnish)

## GitHub mirror

Mirrored to GitHub so HACS can import it.

### Mirror policy

If you so desire, you may open issues and PRs on GitHub.

This may change at any moment, but right now I haven't got a different issue
tracker open (src.quest is under long renovations).

### Pushing the mirror

```sh
git remote add --mirror=push github-mirror git@github.com:liljamo/ha-ouman-eh800.git
git push github-mirror
```

## Development

### Notes
- `strings.json` should match `translations/en.json`.

### Resources
- https://community.home-assistant.io/t/how-to-control-your-ouman-eh-800-heating-controller-using-home-assistant/445244
- https://github.com/Belaial/Ouman-EH800---Home-Assistant
- https://lampopumput.info/foorumi/threads/homeassistant-ja-s%C3%A4hk%C3%B6p%C3%B6rssiohjaus.34446/page-6
- https://lampopumput.info/foorumi/threads/oumanilta-uusi-s%C3%A4%C3%A4din-eh-800.6332/#post-103372
- https://ouman.fi/wp-content/uploads/2021/11/XM1198B_EH-800-kayttoohje_v.3.1.3_FIN_PRINT.pdf#page=15
