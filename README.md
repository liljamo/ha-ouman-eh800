# HA Ouman EH-800

## Important, Home Assistant has got a built-in integration now!
Now on 28.5.2026, I've just read on the beta release notes of 2026.6.0 that
another integration has been merged into Home Assistant.
See:
* https://rc.home-assistant.io/integrations/ouman_eh_800
* https://github.com/home-assistant/core/pull/169733

Consider moving to that, because I will be removing this repository from GitHub
during the coming summer, after migrating myself to the built-in one.

I'd like to thank the few people who I know use this, who have contacted me for
support even. This has been my first project to have actual users.

This was originally made because I needed it for my own use, but then got left
with only L1 support due to lack of time and use of the L2 side.

This was surprisingly low maintanence and just worked after the initial version,
but I'm happy to have less maintanence burden now, especially because I don't
know how much longer I'll be living in my current house with an Ouman EH-800.

## Old readme:
An Ouman EH-800 integration for Home Assistant.

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

### Advanced examples
#### Reading valve position as a number
In Home Assistant, valve entities only record whether the valve is open or not,
due to exact position reporting being optional and dependent on the integration
implementation.

This integration does implement exact position reporting, and as such the
position can be read by templates.

Example, this will make a helper that can be viewed like a graph in history:
```yaml
template:
  - sensor:
    - name: "Valve Position"
      unit_of_measurement: "%"
      state: >
          {{ state_attr('valve.l1_valve_position', 'current_position') }}
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
