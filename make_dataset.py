import os
import shutil
import random

# Start by puting the images in 'images' folder, and the labels in 'labels' folder, then run this script to make the test, train and valid folders following a certain distribution

def create_dirs(base_path, dirs):
    for dir in dirs:
        os.makedirs(os.path.join(base_path, dir, 'images'), exist_ok=True)
        os.makedirs(os.path.join(base_path, dir, 'labels'), exist_ok=True)

def distribute_files(image_files, label_files, output_path, distribution):
    random.shuffle(image_files)
    split_train = int(len(image_files) * distribution['train'])
    split_valid = split_train + int(len(image_files) * distribution['valid'])

    train_files = image_files[:split_train]
    valid_files = image_files[split_train:split_valid]
    test_files = image_files[split_valid:]

    # Function to copy files
    def copy_files(files, type_):
        for file in files:
            basename = os.path.basename(file)
            shutil.copy(file, os.path.join(output_path, type_, 'images', basename))
            label_basename = basename.rsplit('.', 1)[0] + '.txt'  # Change to split at the first dot
            if label_basename in label_files:
                shutil.copy(os.path.join(label_dir, label_basename), os.path.join(output_path, type_, 'labels', label_basename))

    # Copy files to their respective directories
    copy_files(train_files, 'train')
    copy_files(valid_files, 'valid')
    copy_files(test_files, 'test')

# Define your paths and settings
base_path = ''  # Base directory for the dataset
image_dir = os.path.join(base_path, 'images')  # Directory with images
label_dir = os.path.join(base_path, 'labels')  # Directory with labels
output_path = os.path.join(base_path, 'output')  # Output directory

# Create directories
dirs = ['train', 'valid', 'test']
create_dirs(output_path, dirs)

# Get all image and label files
image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
label_files = {f for f in os.listdir(label_dir) if f.endswith('.txt')}

# Set distribution of datasets
distribution = {'train': 0.70, 'valid': 0.20, 'test': 0.10}

# Distribute files accordingly
distribute_files(image_files, label_files, output_path, distribution)

print("Dataset has been organized into train, valid, and test sets 🐣")
