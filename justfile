_default:
    just --list

hass-demo:
    podman run --rm --name hass-demo -p 8123:8123 -v ${PWD}/.hass_dev:/config -v ${PWD}/custom_components:/config/custom_components --cap-add=CAP_NET_RAW,CAP_NET_BIND_SERVICE homeassistant/home-assistant:stable

hass-demo-attach:
    podman exec -it hass-demo bash
