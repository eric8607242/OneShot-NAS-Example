import numpy as np

import torch
import torch.nn as nn

from .base import BaseSearcher


class RandomSearcher(BaseSearcher):
    """ The searcher for the random search search strategy.
    """
    def __init__(self, config, supernet, val_loader, lookup_table, training_strategy, device, criterion, logger):
        super(RandomSearcher, self).__init__(config, supernet, val_loader, lookup_table, training_strategy, device, criterion, logger)

        self.random_iteration = self.config["search_utility"]["random_iteration"]

    def step(self):
        """ The searcher step before each iteration. 
        """
        pass

    def search(self):
        """ Searching the best architecture based on the hardware constraints and the supernet.

        Return:
            best_architecture (np.ndarray)
            best_architecture_hc (float)
            best_architecture_top1 (float)
        """
        self.supernet.module.set_forward_state("single") if isinstance(
            self.supernet, nn.DataParallel) else self.supernet.set_forward_state("single")
        
        random_architectures = []
        for i in range(self.random_iteration):
            self.logger.info("Architecture index : {}".format(i))

            architecture = self.training_strategy.generate_training_architecture()
            architecture_info = self.lookup_table.get_model_info(architecture)

            while architecture_info > self.target_hc:
                architecture = self.training_strategy.generate_training_architecture()
                architecture_info = self.lookup_table.get_model_info(architecture)
            random_architectures.append(architecture)

        architectures_top1_acc = self.evaluate_architectures(random_architectures)
        max_top1_acc_index = architectures_top1_acc.argmax()
        self.logger.info("Random search maximum top1 acc : {}".format(
            architectures_top1_acc[max_top1_acc_index]))

        best_architecture = random_architectures[max_top1_acc_index]
        best_architecture_top1 = architectures_top1_acc[max_top1_acc_index]
        best_architecture_hc = self.lookup_table.get_model_info(best_architecture)

        return best_architecture, best_architecture_hc, best_architecture_top1
