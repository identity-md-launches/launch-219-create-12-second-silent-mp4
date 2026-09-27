# Frog engineer video

Playable output: [artifacts/video.mp4](artifacts/video.mp4)

| Time | Scene seen in the encoded video |
| --- | --- |
| 0:00–0:04 | A frog engineer in an orange helmet moves block 3 onto blocks 1 and 2 on a workbench. |
| 0:04–0:08 | A second frog in glasses scans the stack with a magnifier and completes a checklist. |
| 0:08–0:12 | Both frogs wheel a cardboard box labeled **SOURCE** to the receiving bay. |

Inspected frames from each scene and the frames on either side of the 4-second and 8-second cuts. The three scenes use original flat-vector artwork and hard cuts, with no flashing effects, logos, or financial claims.

**Media:** MP4; 12.000 seconds; 1280 × 720; 24 fps (288 frames); H.264 video in yuv420p; AAC stereo audio at 48 kHz. The AAC track was encoded from a silent source. The MP4 has its `moov` atom before the video data for browser playback. File size: 409,950 bytes.

**Limitations:** The piece is simple 2D animation with straight scene cuts and no sound design. AAC decoding can produce a one-bit-level quantization residue (measured peak −91 dB); there is no audible speech, music, or effect.

To regenerate the output, run `python3 render_video.py` with FFmpeg installed. The script writes intermediate SVG frames under `test/scratch/` and the final MP4 under `artifacts/`.
