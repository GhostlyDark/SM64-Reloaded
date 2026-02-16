# SM64 Reloaded

SM64 Reloaded is an UHD texture pack for GLideN64, rt64, Dolphin, sm64ex (including forks), Ghostship and Jabo.

> [!IMPORTANT]
> Release files can be found over at [evilgames.eu](https://evilgames.eu/texture-packs/sm64-reloaded.htm) and [GitHub Releases](https://github.com/GhostlyDark/SM64-Reloaded/releases/latest).

![](/sm64-reloaded.jpg)



## Porting scripts

> [!Tip]
> This repository contains scripts for automated porting of textures to supported platforms. They require bash v4 and a native Linux environment. On Windows, it is recommended to use WSL2 from within the `wsl.localhost` file system. The scripts will also work using MSYS2, but file operations are going to run much slower. Currently available are `dolphin.sh`, `ghostship.sh`, `jabo.sh` and `sm64ex.sh`.

Make script executable and run it:

```
chmod u+x dolphin.sh
```

```
./dolphin.sh
```

Ported files will be available inside `_build`.



## Texture rescaling

The `sm64.tdb` file contains information about the original texture sizes, which can be used by [Bighead's Custom Texture Tool](https://forums.dolphin-emu.org/Thread-custom-texture-tool-ps-v52-5) to rescale them to a new upscale ratio. This way, an HD replacement for a 32x32 texture can be rescaled to 8x the original resolution (256x256), down from however big the given HD texture might be.



## GLideN64

> [!NOTE]
> Latest [WIP build](https://github.com/gonetz/GLideN64/releases/github-actions) required. Use `PJ64Legacy-Qt-x86` if Project64 is your emulator of choice.

Pre-compiled `.hts` files are `cache` files and have to be located inside:

- Project64: `Project64/Plugin/GFX/cache`
- RMG: `RMG/Cache/cache`
- mupen64plus:
-- Windows: `%appdata%/mupen64plus/cache`
-- Linux: `~/.cache/mupen64plus/cache`
-- macOS: `~/Library/Application Support/Mupen64plus/cache`
- mupen64plus-nx (RetroArch): `RetroArch/system/Mupen64plus/cache`


**Only for advanced users:** HTS cache can be generated from the source PNG textures:

- Project64: `Project64/Plugin/GFX/hires_texture/SUPER MARIO 64`
- RMG: `RMG/Data/hires_texture/SUPER MARIO 64`
- mupen64plus:
-- Windows: `%appdata%/mupen64plus/hires_texture/SUPER MARIO 64`
-- Linux: `~/.local/share/mupen64plus/hires_texture/SUPER MARIO 64`
-- macOS: `~/Library/Application Support/Mupen64plus/hires_texture/SUPER MARIO 64`
- mupen64plus-nx (RetroArch): `RetroArch/system/Mupen64plus/hires_texture/SUPER MARIO 64`


Required graphics settings (named differently depending on emulator):

- Set texture pack usage: `Use texture pack` | `txHiresEnable` | `Use High-Res textures` to **On**
- Set use of full alpha: `Use full transparencies` | `txHiresFullAlphaChannel` | `Use High-Res Full Alpha Channel` to **On**
- Set use of HTS over HTC: `Use file storage instead of memory cache` | `txHiresTextureFileStorage` | `Use enhanced Hi-Res Storage` to **On**


Optional (but recommended) settings:

- Set cache compression: `Compress texture cache` | `txCacheCompression` | `Use High-Res Texture Cache Compression` to **Off**
- Fix black lines: `Fix black lines between 2D elements: For adjacent 2D elements` | `CorrectTexrectCoords: 1 (Auto)` | `Continuous texrect coords: Auto`
- Set mip-mapping: `Enable N64-style mip-mapping` | `EnableLOD` | `LOD Emulation` to **On**



## Dolphin

> [!NOTE]
> Download a recent [release build](https://dolphin-emu.org/download). DDS textures for playing are highly recommended.

- Click `File --> Open User Folder` and copy the texture folder into `Load/Textures`
- Open `Graphics --> Advanced` and activate `Load Custom Textures`



## sm64ex

Supported are sm64ex and most forks based on it, including but not limited to sm64rt (DDS recommended), sm64coopdx and render96ex. The textures can be read from a `.zip` file that sits inside the `build/us_pc/res` directory next to `base.zip`. It is also possible to be unpacked, following the same folder structure as the one inside `base.zip`.



## Ghostship

> [!NOTE]
> O2R files go into the `mods` directory. The order in which mods are loaded can be modified by changing file names. Release files have the `alt/` path prepended, which requires unhiding the menu pressing `Escape` and enabling `Use Alternate Assets` while in-game. Alternatively, press `Tab` to toggle the textures.

If you wish to generate ready to use textures from source, you are required to download and run [retro](https://github.com/HarbourMasters/retro/releases/latest).



### Optional: Update manifest.json

This repo contains a `manifest.json`, which may be required to be updated when a new Ghostship build is released.

1. Install Ghostship by generating as many `.o2r` files as possible using supported ROMs. Check the Ghostship readme for supported versions.
2. Using retro, click `Create OTR / O2R --> Replace Textures --> No`, then select all available `.o2r` files at the same time. This will extract the textures from all archives and generates a `manifest.json`.
3. The compiled `manifest.json` needs to be copied into the directory that contains HD textures, mirroring the file structure of the extracted files.



### Optional: Convert textures

1. Inside retro, choose `Create OTR / O2R --> Replace Textures --> Yes` and select the folder containing HD textures.
2. Keep files uncompressed to reduce stuttering. It is recommended to prepend `alt/` before staging textures, which allows assets to be toggled on-the-fly. Click `Stage Textures` to continue.
3. Click `Finalize OTR / O2R` and `Generate OTR / O2R` as the final step.



## Jabo

HD textures go into `Project64/textures-load`. `Jabo's Direct3D8 1.7.0.57-ver6` is required.

> [!CAUTION]
> Please note that this is a closed source 32-bit only legacy plugin that loads and keeps high resolution textures in RAM once they are triggered. Due to 32-bit limitations, the emulator is guaranteed to crash somewhere between 2 and 3 GB of RAM usage. Due to this, using the pack at its full ("4K") resolution renders the game unplayable. If you do whish to use this outdated plugin, use the downscaled ("HD") pack release.

Jabo's video plugin supports loading DDS textures (uncompressed, DXT1, DXT3, DXT5) including mip-mapping support. Uncompressed (ARGB8) DDS textures aren't displayed correctly however and DXT (BC1, BC2, BC3) textures exhibit terrible quality and more often than not display visual issues as well. Use downscaled PNG textures instead.



## Credits

Texture packs:

- [Fanfreluche's Fan Font](https://github.com/Fanfreluche/SUPERMARIO64-hires-texture-pack)
- [Hypatia's Hi-Res Wind Waker (Termina Invasion)](https://onthegreatsea.tumblr.com/DOWNLOADS)
- [Mollymutt's Super Mario 64](https://emulationking.com/mollymutts-super-mario-64-retexture)
- [MU-TH-UR's Super Mario 64](https://emulationking.com/mu-th-urs-super-mario-64-texture-pack)
- [Nerrel's MM N64HD (Termina Invasion)](http://www.emutalk.net/threads/56677-Majora-s-Mask-N64HD-Project)
- [p3st's Texture Pack](https://github.com/p3st-textures/p3st-Texture_pack)
- [Poke Headroom's Render96 HD Texture Pack](https://github.com/pokeheadroom/RENDER96-HD-TEXTURE-PACK)
- [SM64 Redrawn](https://github.com/TechieAndroid/sm64redrawn)
- [Super Mario 64 - Plumbers Unite Edition (by Roovahlees & Teaufou)](http://www.emutalk.net/threads/57431-Super-Mario-64-Plumbers-Unite-Edition)

General assets:

- Icon: [Bomb (Termina Invasion)](https://www.svgrepo.com/svg/422654/bomb)
- Icon: [Clock (Italian translation)](https://www.mariowiki.com/File:Plus_Clock_Artwork_-_Super_Mario_3D_World.png)
- Icon: [Link Head (Termina Invasion)](https://cults3d.com/de/modell-3d/haus/link-the-legend-of-zelda-2d)
- Icon: [Majora's Mask Clock (Termina Invasion)](http://thecwaftyblog.blogspot.com/2014/08/tutorial-tuesday-majoras-mask-clock.html)
- Icon: [Ocarina (Termina Invasion)](https://www.svgrepo.com/svg/240626/ocarina)
- Icon: [Triforce (Termina Invasion)](https://www.svgrepo.com/svg/323529/triforce)
- Painting: [Jolly Roger Bay](https://www.deviantart.com/rs200groupb/art/Jolly-Roger-Bay-238446343)

Contributors:

- **Admentus:** Technical assistance
- **James:** Rupee object (Termina Invasion)
- **Matteoki:** Wii Home Menu textures
- **michaeltung:** Grindel texture
- **Rulesless:** Italian textures
- **turpinator:** Link icon (Termina Invasion)
- **WARIO:** iQue textures
- **Zack:** Toad icon (sm64coopdx)
