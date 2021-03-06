import pickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture
from featureextraction import extract_features
#from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")

#path to training data
# source   = "development_set/"
source   = "trainingData/"   

#path where training speakers will be saved

# dest = "speaker_models/"
# train_file = "development_set_enroll.txt"

dest = "Speakers_models/"
train_file = "trainingDataPath.txt"        
file_paths = open(train_file,'r')

count = 1
# Extracting features for each speaker (5 files per speakers)
features = np.asarray(())
print(file_paths)
for path in file_paths:

    path = path.strip()
    # print path
    print(path)
    # read the audio
    sr,audio = read(source + path)
    # extract 40 dimensional MFCC & delta MFCC features
    vector   = extract_features(audio,sr)
    
    if features.size == 0:
        features = vector
    else:
        features = np.vstack((features, vector))
    # when features of 45 files of speaker are concatenated, then do model training
	# -> if count == 45: --> edited below
    if count == 15:
        gmm = GaussianMixture(n_components = 18, max_iter = 300, covariance_type='diag', n_init = 5)
        gmm.fit(features)
        
        # dumping the trained gaussian model
        picklefile = path.split("-")[0]+".gmm"
        #print picklefile
        pickle.dump(gmm,open(dest + picklefile,'wb'))
        print('+ modeling completed for speaker:' + str(picklefile) + " with data point = " + str(features.shape))    
        features = np.asarray(())
        count = 0
    count = count + 1
