import os
import time

import torch

from utils import AverageMeter, accuracy, save

from ..base_agent import MetaAgent

class CFMetaAgent(MetaAgent):
    """Classification meta agent
    """
    evaluate_metric = "top1-acc"
    def _training_step(
            self,
            model,
            train_loader,
            epoch,
            print_freq=100):
        top1 = AverageMeter()
        top5 = AverageMeter()
        losses = AverageMeter()

        model.train()
        start_time = time.time()

        for step, (X, y) in enumerate(train_loader):
            self._iteration_preprocess()

            X, y = X.to(
                self.device, non_blocking=True), y.to(
                self.device, non_blocking=True)
            N = X.shape[0]

            self.optimizer.zero_grad()
            outs = model(X)

            loss = self.criterion(outs, y)
            loss.backward()

            self.optimizer.step()
            self.lr_scheduler.step()

            prec1, prec5 = accuracy(outs, y, topk=(1, 5))

            losses.update(loss.item(), N)
            top1.update(prec1.item(), N)
            top5.update(prec5.item(), N)

            if (step > 1 and step % print_freq == 0) or (step == len(train_loader) - 1):
                self.logger.info(f"Train : [{(epoch+1):3d}/{self.epochs}]"
                                 f"Step {step:3d}/{len(train_loader)-1:3d} Loss {losses.get_avg():.3f}"
                                 f"Prec@(1, 5) ({top1.get_avg():.1%}, {top5.get_avg():.1%})")

        self.writer.add_scalar("Train/_loss/", losses.get_avg(), epoch)
        self.writer.add_scalar("Train/_top1/", top1.get_avg(), epoch)
        self.writer.add_scalar("Train/_top5/", top5.get_avg(), epoch)

        self.logger.info(
            f"Train: [{epoch+1:3d}/{self.epochs}] Final Loss {losses.get_avg():.3f}" 
            f"Final Prec@(1, 5) ({top1.get_avg():.1%}, {top5.get_avg():.1%})"
            f"Time {time.time() - start_time:.2f}")


    def _validate(self, model, val_loader, epoch):
        model.eval()
        start_time = time.time()

        top1_avg, top5_avg, losses_avg = self.searching_evaluate(model, val_loader, self.device, self.criterion)

        self.writer.add_scalar("Valid/_loss/", losses_avg, epoch)
        self.writer.add_scalar("Valid/_top1/", top1_avg, epoch)
        self.writer.add_scalar("Valid/_top5/", top5_avg, epoch)

        self.logger.info(
            f"Valid : [{epoch+1:3d}/{self.epochs}] Final Loss {losses_avg:.3f}" 
            f"Final Prec@(1, 5) ({top1_avg:.1%}, {top5_avg:.1%})"
            f"Time {time.time() - start_time:.2f}")

        return top1_avg

    @staticmethod
    def searching_evaluate(model, val_loader, device, criterion):
        top1 = AverageMeter()
        top5 = AverageMeter()
        losses = AverageMeter()

        with torch.no_grad():
            for step, (X, y) in enumerate(val_loader):
                X, y = X.to(device, non_blocking=True), \
                       y.to(device, non_blocking=True)
                N = X.shape[0]
                outs = model(X)

                loss = criterion(outs, y)
                prec1, prec5 = accuracy(outs, y, topk=(1, 5))

                losses.update(loss.item(), N)
                top1.update(prec1.item(), N)
                top5.update(prec5.item(), N)
        return top1.get_avg(), top5.get_avg(), losses.get_avg()

