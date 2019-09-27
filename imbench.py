from glob import glob
from itertools import cycle
import os

import numpy as np

import pytest


@pytest.fixture
def images():
    return cycle(glob(os.environ["IMAGES_PATTERN"]))


def test_PIL_array(images, benchmark):
    Image = pytest.importorskip("PIL.Image")

    @benchmark
    def _():
        np.asarray(Image.open(next(images)).convert("RGB"))


def test_opencv_array(images, benchmark):
    cv2 = pytest.importorskip("cv2")

    @benchmark
    def _():
        cv2.cvtColor(cv2.imread(next(images)), cv2.COLOR_BGR2RGB)


def test_jpeg4py_array(images, benchmark):
    jpeg4py = pytest.importorskip("jpeg4py")

    @benchmark
    def _():
        jpeg4py.JPEG(next(images)).decode()


def test_skimage_array(images, benchmark):
    skimage = pytest.importorskip("skimage")

    @benchmark
    def _():
        skimage.io.imread(next(images), plugin="matplotlib")


def test_imageio_array(images, benchmark):
    imageio = pytest.importorskip("imageio")

    @benchmark
    def _():
        imageio.imread(next(images))


def test_pyvips_array(images, benchmark):
    pyvips = pytest.importorskip("pyvips")

    @benchmark
    def _():
        image = pyvips.Image.new_from_file(next(images), access="sequential")
        np.ndarray(
            buffer=image.write_to_memory(),
            dtype=np.uint8,
            shape=[image.height, image.width, image.bands],
        )


def test_tf_image(images, benchmark):
    tf = pytest.importorskip("tensorflow")
    tf.enable_eager_execution()

    @benchmark
    def _():
        tf.image.decode_jpeg(open(next(images), 'rb').read()).numpy()
