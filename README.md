# ttms_wingitfoodcart

Hugo site for **Wing it Food Cart** (`wingitfoodcart.ttmenus.com`). Based on [ttms_wingit](../ttms_wingit).

## Theme submodule

```bash
git submodule update --init --recursive
```

## Build

```bash
hugo --gc --minify
```

Netlify uses `build_menu.sh` (see `netlify.toml`).
