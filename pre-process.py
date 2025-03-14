# -*- coding: utf-8 -*-

import tarfile
import scipy.io
import numpy as np
import os
import cv2 as cv
import shutil
import random
from console_progressbar import ProgressBar


def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def save_train_data(fnames, labels, bboxes):
	src_folder = 'cars_train'
	num_samples = len(fnames)

	train_split = 0.8
	num_train = int(round(num_samples * train_split))
	train_indexes = random.sample(range(num_samples), num_train)

	pb = ProgressBar(total=100, prefix='Save train data', suffix='', decimals=3, length=50, fill='=')

	for i in range(num_samples):
		fname = fnames[i]
		label = labels[i]
		(x1, y1, x2, y2) = bboxes[i]

		src_path = os.path.join(src_folder, fname)
		src_image = cv.imread(src_path)
		height, width = src_image.shape[:2]
		# margins of 16 pixels
		margin = 16
		x1 = max(0, x1 - margin)
		y1 = max(0, y1 - margin)
		x2 = min(x2 + margin, width)
		y2 = min(y2 + margin, height)
		# print("{} -> {}".format(fname, label))
		pb.print_progress_bar((i + 1) * 100 / num_samples)

		if i in train_indexes:
			dst_folder = 'data/train'
		else:
			dst_folder = 'data/valid'

		dst_path = os.path.join(dst_folder, label)
		if not os.path.exists(dst_path):
			os.makedirs(dst_path)
		dst_path = os.path.join(dst_path, fname)
		#print("this : " + str(dst_path))
		fname2 = str(dst_path).split(".")
		fname11 = fname2[0] + "00.jpg"
		fname22 = fname2[0] + "01.jpg"
		
		#fname2 = str(fname) + "00"
		#dst_path2 = os.path.join(dst_path, fname2)
		#print("this2 : " + str(fname2))
		crop_image = src_image[y1:y2, x1:x2]
		dst_img = cv.resize(src=crop_image, dsize=(img_height, img_width))
		hsv_img1 = cv.cvtColor(dst_img,cv.COLOR_BGR2RGB)
		hsv_img2 = cv.cvtColor(dst_img,cv.COLOR_RGB2HSV)
		cv.imwrite(dst_path, dst_img)
		cv.imwrite(fname11, hsv_img1)
		cv.imwrite(fname22, hsv_img2)


def save_test_data(fnames, bboxes):
    src_folder = 'cars_test'
    dst_folder = 'data/test'
    num_samples = len(fnames)

    pb = ProgressBar(total=100, prefix='Save test data', suffix='', decimals=3, length=50, fill='=')

    for i in range(num_samples):
        fname = fnames[i]
        (x1, y1, x2, y2) = bboxes[i]
        src_path = os.path.join(src_folder, fname)
        src_image = cv.imread(src_path)
        height, width = src_image.shape[:2]
        # margins of 16 pixels
        margin = 16
        x1 = max(0, x1 - margin)
        y1 = max(0, y1 - margin)
        x2 = min(x2 + margin, width)
        y2 = min(y2 + margin, height)
        # print(fname)
        pb.print_progress_bar((i + 1) * 100 / num_samples)

        dst_path = os.path.join(dst_folder, fname)
        crop_image = src_image[y1:y2, x1:x2]
        dst_img = cv.resize(src=crop_image, dsize=(img_height, img_width))
        cv.imwrite(dst_path, dst_img)


def process_train_data():
	print("Processing train data...")
	cars_annos = scipy.io.loadmat('devkit/cars_train_annos')
	annotations = cars_annos['annotations']
	annotations = np.transpose(annotations)

	fnames = []
	class_ids = []
	bboxes = []
	labels = []

	for annotation in annotations:
		bbox_x1 = annotation[0][0][0][0]
		bbox_y1 = annotation[0][1][0][0]
		bbox_x2 = annotation[0][2][0][0]
		bbox_y2 = annotation[0][3][0][0]
		class_id = annotation[0][4][0][0]
		labels.append('%04d' % (class_id,))
		fname = annotation[0][5][0]
		bboxes.append((bbox_x1, bbox_y1, bbox_x2, bbox_y2))
		class_ids.append(class_id)
		fnames.append(fname)

	print(fnames[0])
	print(class_ids[0])
	print(labels[0])
	labels_count = np.unique(class_ids).shape[0]
	print(np.unique(class_ids))
	print('The number of different cars is %d' % labels_count)

	save_train_data(fnames, labels, bboxes)


def process_test_data():
    print("Processing test data...")
    cars_annos = scipy.io.loadmat('devkit/cars_test_annos')
    annotations = cars_annos['annotations']
    annotations = np.transpose(annotations)

    fnames = []
    bboxes = []

    for annotation in annotations:
        bbox_x1 = annotation[0][0][0][0]
        bbox_y1 = annotation[0][1][0][0]
        bbox_x2 = annotation[0][2][0][0]
        bbox_y2 = annotation[0][3][0][0]
        fname = annotation[0][4][0]
        bboxes.append((bbox_x1, bbox_y1, bbox_x2, bbox_y2))
        fnames.append(fname)

    save_test_data(fnames, bboxes)


if __name__ == '__main__':
	# parameters
	#img_width, img_height = 224, 224
	img_width, img_height = 299, 299

	
	print('Extracting cars_train.tgz...')
	if not os.path.exists('cars_train'):
		with tarfile.open('cars_train.tgz', "r:gz") as tar:
def is_within_directory(directory, target):
	
	abs_directory = os.path.abspath(directory)
	abs_target = os.path.abspath(target)

	prefix = os.path.commonprefix([abs_directory, abs_target])
	
	return prefix == abs_directory

def safe_extract(tar, path=".", members=None, *, numeric_owner=False):

	for member in tar.getmembers():
		member_path = os.path.join(path, member.name)
		if not is_within_directory(path, member_path):
			raise Exception("Attempted Path Traversal in Tar File")

	tar.extractall(path, members, numeric_owner=numeric_owner) 
	

safe_extract(tar)
	print('Extracting cars_test.tgz...')
	if not os.path.exists('cars_test'):
		with tarfile.open('cars_test.tgz', "r:gz") as tar:
def is_within_directory(directory, target):
	
	abs_directory = os.path.abspath(directory)
	abs_target = os.path.abspath(target)

	prefix = os.path.commonprefix([abs_directory, abs_target])
	
	return prefix == abs_directory

def safe_extract(tar, path=".", members=None, *, numeric_owner=False):

	for member in tar.getmembers():
		member_path = os.path.join(path, member.name)
		if not is_within_directory(path, member_path):
			raise Exception("Attempted Path Traversal in Tar File")

	tar.extractall(path, members, numeric_owner=numeric_owner) 
	

safe_extract(tar)
	print('Extracting car_devkit.tgz...')
	if not os.path.exists('devkit'):
		with tarfile.open('car_devkit.tgz', "r:gz") as tar:
def is_within_directory(directory, target):
	
	abs_directory = os.path.abspath(directory)
	abs_target = os.path.abspath(target)

	prefix = os.path.commonprefix([abs_directory, abs_target])
	
	return prefix == abs_directory

def safe_extract(tar, path=".", members=None, *, numeric_owner=False):

	for member in tar.getmembers():
		member_path = os.path.join(path, member.name)
		if not is_within_directory(path, member_path):
			raise Exception("Attempted Path Traversal in Tar File")

	tar.extractall(path, members, numeric_owner=numeric_owner) 
	

safe_extract(tar)
	
	cars_meta = scipy.io.loadmat('devkit/cars_meta')
	class_names = cars_meta['class_names']  # shape=(1, 196)
	class_names = np.transpose(class_names)
	print('class_names.shape: ' + str(class_names.shape))
	print('Sample class_name: [{}]'.format(class_names[195][0][0]))

	ensure_folder('data/train')
	ensure_folder('data/valid')
	ensure_folder('data/test')

	process_train_data()
	#process_test_data()


	# clean up
	shutil.rmtree('cars_train')
	shutil.rmtree('cars_test')
	shutil.rmtree('devkit')
