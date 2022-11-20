import Utility as Util
import cv2


def main():
    orig_early_summer_path = 'Resources/OriginalEarlySummer'
    orig_late_summer_path = 'Resources/OriginalLateSummer'
    new_early_summer_path = 'Resources/EarlySummer'
    new_late_summer_path = 'Resources/LateSummer'
    orig_early_summer_files = Util.get_files(orig_early_summer_path)
    orig_late_summer_files = Util.get_files(orig_late_summer_path)

    print(f'Early Summer Count: {len(orig_early_summer_files)}')
    print(f'Late Summer Count: {len(orig_late_summer_files)}')
    early_summer_paths = Util.image_preprocessing(orig_early_summer_files, new_early_summer_path)
    print('Completed Early Summer Preprocessing')
    late_summer_paths = Util.image_preprocessing(orig_late_summer_files, new_late_summer_path)
    print('Complete Late Summer Preprocessing')
    Util.generate_histogram(early_summer_paths)


if __name__ == '__main__':
    main()
