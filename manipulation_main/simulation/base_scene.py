import os
import numpy as np
import pybullet as p
import pybullet_data
from abc import ABC, abstractmethod

class BaseScene(ABC):
    def __init__(self, world, config, rng, test=False, validate=False):
        self._world = world
        self._rng = rng
        self._model_path = pybullet_data.getDataPath()
        self._validate = validate
        self._test = test
        self.extent = config.get('extent', 0.1)
        # self.max_objects = config.get('max_objects', 6)
        self.max_objects = config.get('max_objects', 1)
        self.min_objects = config.get('min_objects', 1)
        object_samplers = {'wooden_blocks': self._sample_wooden_blocks,
                           'random_urdfs': self._sample_random_objects,
                           'heap_urdfs': self._sample_objects_heap,
                           'egad_urdfs': self._sample_objects_egad}
        # 'random_urdfs': self._sample_objects_heap,
        print("Config scene data_set: " + config['scene']['data_set'])
        self._object_sampler = object_samplers[config['scene']['data_set']]
        print("dataset", config['scene']['data_set'])

    ### This function loads all the objects from a given folder containing meshes in OBJ format.
    # Author: Mihai ANDRIES
    # Date: 2022.03.18
    # It returns an array of paths to the objects contained in the object set (dataset)
    def _sample_objects_from_path(self, n_objects,  path):
        dataset_of_filenames = []
        dataset_path = "models/" + path
        format_suffix = ".obj"

        print("\n\nSampling objects from path {0}".format(dataset_path))

        # Walk through the directory, and pick the files
        for root, dirs, files in os.walk(dataset_path, topdown=True):  # directory
            # for directory in dirs:
            #   print('\nFound: ' + directory + '/')
            for filename in files:
                # print('\nFound: ' + filename)
                if filename.endswith(format_suffix):
                  global_filename = os.path.join(root, filename)
                  dataset_of_filenames.append(global_filename)
                  # increase the counter of loaded files

        print("Total object meshes loaded: {0}".format(len(dataset_of_filenames)))
        print("Files: ")
        print(dataset_of_filenames)

        # Provide only as many objects as requested
        dataset_of_filenames = dataset_of_filenames[0:n_objects]

        return dataset_of_filenames, 1.

    # Load the objects generated in the HEAP project
    def _sample_objects_heap(self, n_objects):
        print("n_objects: {}".format(n_objects))
        return self._sample_objects_from_path(n_objects, path="heap_2020.06.12_02h00")

    # Load the objects generated in the EGAD project
    def _sample_objects_egad(self, n_objects):
        print("n_objects: {}".format(n_objects))
        return self._sample_objects_from_path(n_objects, path="egad_eval_set")

    def _sample_wooden_blocks(self, n_objects):
        self._model_path = "models/"
        object_names = ['circular_segment', 'cube',
                        'cuboid0', 'cuboid1', 'cylinder', 'triangle']
        selection = self._rng.choice(object_names, size=n_objects)
        paths = [os.path.join(self._model_path, 'wooden_blocks',
                              name + '.urdf') for name in selection]
        return paths, 1.


    def _sample_random_objects(self, n_objects):
        if self._validate:
            self.object_range = np.arange(700, 850)
        elif self._test:
            self.object_range = np.arange(850, 1000)
        else:
            self.object_range = 700
        # object_range = 900 if not self._test else np.arange(900, 1000)
        selection = self._rng.choice(self.object_range, size=n_objects)
        paths = [os.path.join(self._model_path, 'random_urdfs',
                            '{0:03d}/{0:03d}.urdf'.format(i)) for i in selection]
        return paths, 1.

    @abstractmethod
    def reset(self):
        raise NotImplementedError
