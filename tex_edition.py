"""Which build this is: full Texel, or the free Lite demo.

The source tree is always the full build and this file says so. `build.py
--lite` rewrites it to LITE = True inside the Lite zip and leaves out the three
paid modules (tex_anim, tex_sprite, tex_showcase), so the flag and the missing
files always travel together - one cannot ship without the other.
"""
LITE = False

# where the "in full Texel" buttons send a Lite user. Only mintworks.cc is ever
# baked into a product file (CLAUDE.md §5), never a marketplace subdomain.
FULL_URL = "https://mintworks.cc/texel"
