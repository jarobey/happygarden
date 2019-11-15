from pyhap import camera

# Specify the audio and video configuration that your device can support
# The HAP client will choose from these when negotiating a session.
cameraOptions = {
    "video": {
        "codec": {
            "profiles": [
                camera.VIDEO_CODEC_PARAM_PROFILE_ID_TYPES["BASELINE"],
                camera.VIDEO_CODEC_PARAM_PROFILE_ID_TYPES["MAIN"],
                camera.VIDEO_CODEC_PARAM_PROFILE_ID_TYPES["HIGH"]
            ],
            "levels": [
                camera.VIDEO_CODEC_PARAM_LEVEL_TYPES['TYPE3_1'],
                camera.VIDEO_CODEC_PARAM_LEVEL_TYPES['TYPE3_2'],
                camera.VIDEO_CODEC_PARAM_LEVEL_TYPES['TYPE4_0'],
            ],
        },
        "resolutions": [
            # Width, Height, framerate
            # [320, 240, 15], # Required for Apple Watch
            [1920, 1080, 30],
            [3280, 2464, 15],
            [1640, 922, 40],
            [1280, 720, 90],
            [640, 480, 120],
        ],
    },
    "audio": {
        "codecs": [
            {
                'type': 'OPUS',
                'samplerate': 24,
            },
            {
                'type': 'AAC-eld',
                'samplerate': 16
            }
        ],
    },
    "address": "10.0.10.21",
}

class PiCamV2(camera):

    def __init__(self, options, *args, **kwargs):
        super().__init__(sock, client_addr, server)