"""Render the new 3D models next to the flat cards they replace. Not shipped.

  blender --background --factory-startup --python proof3d.py

Writes shots/proof3d.png - the whole prop set as real geometry - and
shots/proof3d_ab.png, the same sword built both ways so the difference is a
comparison rather than a claim.
"""
from __future__ import annotations
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import models3d as M                                        # noqa: E402

RES = (1400, 720)
SAMPLES = 220


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def aim(obj, target):
    """Point an object's -Z at `target`.

    A camera with rotation (0,0,0) looks down -Z. Rotating X by rx then Z by rz
    sends that to (-sin rx sin rz, sin rx cos rz, -cos rx), so matching a
    direction (dx,dy,dz) means rx = atan2(hypot(dx,dy), -dz) and
    rz = atan2(dy,dx) - pi/2. Getting either sign wrong aims it at the sky,
    which is what an empty first render looked like.
    """
    lx, ly, lz = obj.location
    dx, dy, dz = target[0] - lx, target[1] - ly, target[2] - lz
    obj.rotation_euler = (math.atan2(math.hypot(dx, dy), -dz), 0,
                          math.atan2(dy, dx) - math.pi / 2)


def ground(shade=(0.026, 0.024, 0.032, 1)):
    bpy.ops.mesh.primitive_plane_add(size=120, location=(0, 0, 0))
    o = bpy.context.active_object
    m = bpy.data.materials.new("Ground")
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = shade
    b.inputs["Roughness"].default_value = 0.96
    o.data.materials.append(m)
    return o


def key_light():
    """Three lights, none of them visible to camera - an area light that renders
    is a white slab across the frame."""
    for name, loc, energy, size, col in (
            ("Key",  (-4.5, -5.0, 7.0), 380, 5.0, (1.0, 0.94, 0.86)),
            ("Fill", (5.5, -4.0, 3.4), 110, 6.0, (0.66, 0.76, 1.0)),
            ("Rim",  (2.0, 6.5, 5.0), 300, 3.0, (1.0, 0.70, 0.40))):
        d = bpy.data.lights.new(name, "AREA")
        d.energy, d.size, d.color = energy, size, col
        d.use_shadow = True
        o = bpy.data.objects.new(name, d)
        o.location = loc
        o.visible_camera = False
        bpy.context.collection.objects.link(o)
        aim(o, (0, 0, 1.2))


def camera(loc, look, lens=52):
    d = bpy.data.cameras.new("Cam")
    d.lens = lens
    cam = bpy.data.objects.new("Cam", d)
    bpy.context.collection.objects.link(cam)
    cam.location = loc
    aim(cam, look)
    bpy.context.scene.camera = cam
    return cam


def flat_card(name, image_name, loc, size=1.6):
    """The OLD way, rebuilt here so the comparison is honest rather than
    remembered: a texture on a plane, angled to the camera."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc,
                                     rotation=(math.radians(90), 0,
                                               math.radians(-26)))
    o = bpy.context.active_object
    o.name = name
    img = bpy.data.images.get(image_name)
    m = bpy.data.materials.new(name + "Mat")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = img
    t.interpolation = "Closest"
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(t.outputs["Alpha"], b.inputs["Alpha"])
    b.inputs["Roughness"].default_value = 0.9
    o.data.materials.append(m)
    return o


def render(path, res=None, transparent=False):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    try:
        sc.cycles.device = "GPU"
        p = bpy.context.preferences.addons["cycles"].preferences
        p.compute_device_type = "OPTIX"
        p.get_devices()
        for d in p.devices:
            d.use = True
    except Exception as e:
        print(f"[warn] CPU fallback: {e}", flush=True)
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = res or RES
    sc.render.film_transparent = bool(transparent)
    sc.view_settings.look = "AgX - Base Contrast"
    sc.world = bpy.data.worlds.new("W")
    sc.world.use_nodes = True
    sc.world.node_tree.nodes["Background"].inputs["Color"].default_value = (
        0.022, 0.020, 0.026, 1)
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print(f"  wrote {path}", flush=True)


# --------------------------------------------------------------------------
def torchbearer():
    """Character plus torch, assembled so the torch sits IN the hand.

    That is the whole point of solid geometry: two flat cards cannot hold each
    other. Returns the objects so callers can frame them.
    """
    ch = M.character("Torchbearer")
    hx, hy, hz = ch["texel_hand"]

    torch = M.prop("torch")
    torch.parent = ch                    # so turning the figure turns the torch
    # held upright in a raised hand, so no tilt - the handle passes through the
    # fist and the head clears it
    torch.location = (hx, hy, hz - 0.34)

    fl = M.flame("Flame", scale=0.85)
    fl.parent = ch
    fl.location = (hx, hy, hz + 0.70)

    li = bpy.data.lights.new("Fire", "POINT")
    li.energy, li.color, li.shadow_soft_size = 170, (1.0, 0.62, 0.28), 0.28
    lo = bpy.data.objects.new("Fire", li)
    lo.parent = ch
    lo.location = (hx, hy, hz + 0.78)
    bpy.context.collection.objects.link(lo)
    return ch, torch, fl


def styles():
    """The two candidate looks, same lighting, same texture pipeline.

    Left: voxel - stacked cubes. It works, and it is what most pixel-art 3D
    games use, but it reads as a Minecraft skin.
    Right: low-poly - every part tapered, so the silhouette is a flared robe
    under a pointed hood. Same pixels, different geometry.
    """
    reset()
    ground()
    key_light()

    for maker, x, turn in ((M.character, -1.15, 24), (M.character_hooded, 1.15, -20)):
        ch = maker()
        hx, hy, hz = ch["texel_hand"]
        t = M.prop("torch")
        t.parent = ch
        t.location = (hx, hy, hz - 0.34)
        fl = M.flame("Flame", scale=0.85)
        fl.parent = ch
        fl.location = (hx, hy, hz + 0.70)
        li = bpy.data.lights.new("Fire", "POINT")
        li.energy, li.color, li.shadow_soft_size = 150, (1.0, 0.62, 0.28), 0.28
        lo = bpy.data.objects.new("Fire", li)
        lo.parent = ch
        lo.location = (hx, hy, hz + 0.78)
        bpy.context.collection.objects.link(lo)
        ch.location = (x, 0, 0)
        ch.rotation_euler = (0, 0, math.radians(turn))

    camera((0, -8.6, 2.7), (0, 0, 1.5), lens=50)
    render(os.path.join(HERE, "shots", "proof3d_styles"), res=(1400, 800))


def hero():
    """The character alone, filling the frame - the thing being judged."""
    reset()
    ground()
    key_light()
    ch, _, _ = torchbearer()
    ch.rotation_euler = (0, 0, math.radians(26))
    camera((-1.7, -5.9, 2.35), (0.08, 0, 1.42), lens=55)
    render(os.path.join(HERE, "shots", "proof3d_hero"), res=(900, 900))


def sheet():
    """Every prop, as real geometry, in one frame."""
    reset()
    ground()
    key_light()

    ch, _, _ = torchbearer()
    ch.location = (-2.9, 0.35, 0)          # the torch is parented, so it follows
    ch.rotation_euler = (0, 0, math.radians(22))

    row = [("sword", -1.35), ("axe", -0.4), ("potion", 0.55),
           ("chest", 1.6), ("crate", 2.7), ("coin", 3.7)]
    for kind, x in row:
        o = M.prop(kind)
        o.location = (x, 0, 0)
        # the coin gets a hard turn so its edge shows: face-on, a thin disc
        # looks exactly like the card this whole exercise is replacing
        o.rotation_euler = (0, 0, math.radians(52 if kind == "coin"
                                               else -26 + (abs(x) * 37) % 46))

    camera((0.35, -9.6, 3.0), (0.35, 0, 1.15), lens=46)
    render(os.path.join(HERE, "shots", "proof3d"))


def ab():
    """The same sword, both ways.

    The card uses gallery/sword.png - the ACTUAL sprite the old pipeline put on
    a plane - so this is a comparison against what shipped, not against a
    strawman I built to lose.
    """
    reset()
    ground()
    key_light()

    old_png = os.path.join(HERE, "gallery", "sword.png")
    img = bpy.data.images.load(old_png, check_existing=True)
    card = flat_card("SwordCard", img.name, (-0.75, 0, 1.02), size=2.05)
    card.rotation_euler = (math.radians(90), 0, math.radians(-52))

    new = M.prop("sword", "SwordSolid")
    new.location = (0.75, 0, 0)
    new.rotation_euler = (0, 0, math.radians(-52))

    camera((0, -6.1, 1.75), (0, 0, 1.0), lens=50)
    render(os.path.join(HERE, "shots", "proof3d_ab"), res=(1200, 700))


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "shots"), exist_ok=True)
    styles()
    hero()
    sheet()
    ab()
    print("PROOF DONE", flush=True)
