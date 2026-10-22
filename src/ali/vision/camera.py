"""Optional OpenCV camera adapter. Import OpenCV only when requested."""


class CameraUnavailable(RuntimeError):
    pass


class OpenCVCamera:
    def __init__(self, device_index: int = 0):
        try:
            import cv2  # type: ignore[import-not-found]
        except ImportError as exc:
            raise CameraUnavailable(
                "Camera support is optional. Install it with: pip install '.[vision]'"
            ) from exc
        self._cv2 = cv2
        self._capture = cv2.VideoCapture(device_index)
        if not self._capture.isOpened():
            self._capture.release()
            raise CameraUnavailable(f"Could not open camera device {device_index}.")

    def read(self):
        ok, frame = self._capture.read()
        if not ok:
            raise CameraUnavailable("Camera frame capture failed.")
        return frame

    def close(self) -> None:
        self._capture.release()
