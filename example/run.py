import sys

sys.path.append("..")


from citrus import datastructures as ds
from citrus.configure import load_config


def main():
    """
    1. Initialize `par` with default values.
    2. Create FITS object.
    3. Initialize the images with default values.
    4. Call input routines from `citrus/model.py` to set both `par` and `image` values.
    """

    default_angle = -999.0

    par, imgs = load_config()


if __name__ == "__main__":
    main()