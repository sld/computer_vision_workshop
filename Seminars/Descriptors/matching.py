from skimage import data
from sys import (argv, exit)
from skimage import transform as tf
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches,
                             BRIEF, CENSURE)
from skimage.color import rgb2gray
from skimage.transform import ProjectiveTransform
from skimage.measure import ransac

import matplotlib.pyplot as plt


def extract_by_orb(img1, img2, n_keypoints=200):
    def extract_keypoints_and_descriptors(descriptor_extractor, img):
        descriptor_extractor.detect_and_extract(img)
        keypoints = descriptor_extractor.keypoints
        descriptors = descriptor_extractor.descriptors

        return (keypoints, descriptors)

    descriptor_extractor = ORB(n_keypoints=n_keypoints)
    keyp1, desc1 = extract_keypoints_and_descriptors(descriptor_extractor, img1)
    keyp2, desc2 = extract_keypoints_and_descriptors(descriptor_extractor, img2)

    return [keyp1, keyp2, desc1, desc2]


def extract_by_brief(img1, img2, min_distance=1):
    extractor = BRIEF()
    detector = CENSURE(mode='STAR')
    detector.detect(img1)
    keyp1 = detector.keypoints

    detector.detect(img2)
    keyp2 = detector.keypoints

    extractor.extract(img1, keyp1)
    desc1 = extractor.descriptors

    extractor.extract(img1, keyp2)
    desc2 = extractor.descriptors

    return [keyp1, keyp2, desc1, desc2]


def load_images(img1_path, img2_path):
    img1 = data.imread(img1_path, as_grey=True)
    img2 = data.imread(img2_path, as_grey=True)
    return (img1, img2)


def run(img1_path, img2_path, type='ORB'):
    img1, img2 = load_images(img1_path, img2_path)

    if type == 'ORB':
        keyp1, keyp2, desc1, desc2 = extract_by_orb(img1, img2, 100)
    elif type == 'BRIEF':
        keyp1, keyp2, desc1, desc2 = extract_by_brief(img1, img2, 10)

    matches = match_descriptors(desc1, desc2, cross_check=True)

    plot(img1, img2, keyp1, keyp2, matches)


def plot(img1, img2, keyp1, keyp2, matches):
    plot_matches(plt, img1, img2, keyp1, keyp2, matches)
    plt.show()


if __name__ == '__main__':
    if len(argv) < 4:
        exit('Pass img1, img2 and type(ORB or BRIEF)')
    img1_path = argv[1]
    img2_path = argv[2]
    type = argv[3]
    run(img1_path, img2_path, type)
