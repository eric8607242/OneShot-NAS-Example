# OSNASLib

## Introduction
OSNASLib is a library for one-shot neural architecture search (NAS). Recently, searching the neural architecture for various deep learning tasks (e.g., semantic segmentation, object detection, and NLP) becomes a common pipeline to improve the performance. Therefore, OSNASLib provides extremely flexible interfaces to allow researchers can incorporate different one-shot NAS algorithms into various specific tasks efficient.

In OSNASLib, we cover various components of one-shot NAS (e.g., search space, search strategy, and training strategy). You can incorporate any components to specify for different dataset, differnt criterion and different specific tasks easily. 
Please refer to [What is OSNASLib](./doc/osnaslib.md) for more detail about this library.

* [What is neural architecture search (NAS)](./doc/nas.md)
* [What is one-shot NAS](./doc/one_shot_nas.md)

**We are glad at all contributions to improve this repo. Please feel free to pull request.**

## Getting Started
```
python3 main.py -c [CONFIG FILE] --title [EXPERIMENT TITLE]

optional arguments:
    --title                 The title of the experiment. All corrsponding files will be saved in the directory named with experiment title.
    -c, --config            The path to the config file. Refer to ./config/ for serveral example config file.
```

More information about configuration please refer to [configuration](./doc/configuration.md).

## Customize NAS For Your Tasks
To make customize more easily, we 

### Generate Templare
OSNASLib provides extremely flexible interfaces to make researchers can incorporate different components of one-shot NAS for various tasks easily.
For customizing for different components, you will need to generate some code that establishes the component template - a collection of interface for incorporating with other components.
```
python3 build_template.py -tt [TEMPLATE TYPE] --customize-name [CUSTOMIZE NAME] --customize-class [CUSTOMIZE CLASS]

optional arguments:
    -tt, --template-type    The type of the generated template (e.g., agent, criterion, and dataflow).
    --customize-name        The filename of the customizing template.
    --customize-class       The classname of the interface class in customizing template.
```

Please refer to the documents for more detail of customizing.
* [How to customize the criterion](./doc/customize/criterion.md)
* [How to customize the dataloader](./doc/customize/dataloader.md)
* [How to customize the search space](./doc/customize/search_space.md)
* [How to customize the search strategy](./doc/customize/search_strategy.md)
* [How to customize the training strategy](./doc/customize/training_strategy.md)
* [How to customize the agent](./doc/customize/agent.md)

In OSNASLib, we provide the example for serveral tasks. Please reference for following documents for more detail about the example:
* [Classification](./doc/example/classification.md)
* [Face Recognition](./doc/example/face_recognition.md)

## TODO
* [ ] Documents

