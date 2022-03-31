import os

import pickle

import math
import torch
from torch.autograd import Variable
from torch.nn import Module, Conv2d, MaxPool2d, ConvTranspose2d, BatchNorm2d, Parameter
from torch.nn.functional import leaky_relu, tanh

from settings import Settings
from hardware import load, gpu


class Discriminator1(Module):
    """
    A CNN that produces a density map and a count.
    """
    def __init__(self):
        super().__init__()
        self.conv1 = Conv2d(3, 32, kernel_size=7, padding=3)
        self.max_pool1 = MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = Conv2d(self.conv1.out_channels, 32, kernel_size=7, padding=3)
        self.max_pool2 = MaxPool2d(kernel_size=2, stride=2)
        self.conv3 = Conv2d(self.conv2.out_channels, 64, kernel_size=5, padding=2)
        self.conv4 = Conv2d(self.conv3.out_channels, 1000, kernel_size=18)
        self.conv5 = Conv2d(self.conv4.out_channels, 400, kernel_size=1)
        self.count_conv = Conv2d(self.conv5.out_channels, 1, kernel_size=1)
        self.density_conv = Conv2d(self.conv5.out_channels, 324, kernel_size=1)
        self.feature_layer = None

    def __call__(self, *args, **kwargs):
        """
        Defined in subclass just to allow for type hinting.

        :return: The predicted labels.
        :rtype: torch.autograd.Variable
        """
        return super().__call__(*args, **kwargs)

    def forward(self, x):
        """
        The forward pass of the network.

        :param x: The input images.
        :type x: torch.autograd.Variable
        :return: The predicted density labels.
        :rtype: torch.autograd.Variable
        """
        x = leaky_relu(self.conv1(x))
        x = self.max_pool1(x)
        x = leaky_relu(self.conv2(x))
        x = self.max_pool2(x)
        x = leaky_relu(self.conv3(x))
        x = leaky_relu(self.conv4(x))
        x = leaky_relu(self.conv5(x))
        self.feature_layer = x
        x_count = leaky_relu(self.count_conv(x)).view(-1)
        x_density = leaky_relu(self.density_conv(x)).view(-1, 18, 18)
        return x_density, x_count


class Generator(Module):
    """
    A generator for producing crowd images.
    """
    def __init__(self):
        super().__init__()
        self.conv_transpose1 = ConvTranspose2d(100, 64, kernel_size=18)
        self.conv_transpose2 = ConvTranspose2d(self.conv_transpose1.out_channels, 32, kernel_size=4, stride=2,
                                               padding=1)
        self.conv_transpose3 = ConvTranspose2d(self.conv_transpose2.out_channels, 3, kernel_size=4, stride=2,
                                               padding=1)

    def forward(self, z):
        """
        The forward pass of the generator.

        :param z: The input images.
        :type z: torch.autograd.Variable
        :return: Generated images.
        :rtype: torch.autograd.Variable
        """
        z = z.view(-1, 100, 1, 1)
        z = leaky_relu(self.conv_transpose1(z))
        z = leaky_relu(self.conv_transpose2(z))
        z = tanh(self.conv_transpose3(z))
        return z

    def __call__(self, *args, **kwargs):
        """
        Defined in subclass just to allow for type hinting.

        :return: The predicted labels.
        :rtype: torch.autograd.Variable
        """
        return super().__call__(*args, **kwargs)


class Predictor(Module):
    """
    The extra predictor layer.
    """
    def __init__(self):
        super().__init__()
        self.exponent = Parameter(torch.Tensor([0]))
        self.register_buffer('e', torch.Tensor([math.e]))

    def forward(self, y):
        """
        The forward pass of the predictor.

        :param y: Person counts.
        :type y: torch.autograd.Variable
        :return: Scaled person counts.
        :rtype: torch.autograd.Variable
        """
        y = y * Variable(self.e).pow(self.exponent)
        return yIntroduct

    def __call__(self, *args, **kwargs):
        """
        Defined in subclass just to allow for type hinting.

        :return: The predicted labels.
        :rtype: torch.autograd.Variable
        """
        return super().__call__(*args, **kwargs)


class GAN(Module):
    """
    The full GAN.
    """
    def __init__(self):
        super().__init__()
        self.D = JointCNN()
        self.G = Generator()
        self.P = Predictor()

    def forward(self, x):
        """Forward pass not implemented here."""
        raise NotImplementedError


def save_trainer(trialDirectory, model, optimizer, epoch, step, prefix=None):
    """
    Saves all the information needed to continue training.

    :param trialDirectory: The directory path to save the data to.
    :type trialDirectory: str
    :param model: The model to save.
    :type model: torch.nn.Module
    :param optimizer: The optimizer to save.
    :type optimizer: torch.optim.optimizer.Optimizer
    :param epoch: The number of epochs completed.
    :type epoch: int
    :param step: The number of steps completed.
    :type step: int
    :param prefix: A prefix to append to the model file names.
    :type prefix: str
    """
    model_path = 'model {}'.format(epoch)
    optimizer_path = 'optimizer {}'.format(epoch)
    meta_path = 'meta {}'.format(epoch)
    if prefix:
        model_path = prefix + ' ' + model_path
        optimizer_path = prefix + ' ' + optimizer_path
        meta_path = prefix + ' ' + meta_path
    torch.save(model.state_dict(), os.path.join(trialDirectory, model_path))
    torch.save(optimizer.state_dict(), os.path.join(trialDirectory, optimizer_path))
    with open(os.path.join(trialDirectory, meta_path), 'wb') as pickle_file:
        pickle.dump({'epoch': epoch, 'step': step}, pickle_file)


def load_trainer(prefix=None, settings=None):
    """
    Saves all the information needed to continue training.

    :param prefix: A prefix to append to the model file names.
    :type prefix: str
    :return: The model and optimizer state dict and the metadata for the training run.
    :rtype: dict[torch.Tensor], dict[torch.Tensor], int, int
    """
    if settings is None:
        settings = Settings()
    model_path = settings.load_model_path
    print('model_path =', model_path)
    optimizer_path = settings.load_model_path.replace('model', 'optimizer')
    print('optimizer_path = ',optimizer_path)
    meta_path = settings.load_model_path.replace('model', 'meta')
    print('meta_path =', meta_path)
    if prefix:
        model_path = os.path.join(os.path.split(model_path)[0], prefix + ' ' + os.path.split(model_path)[1])
        optimizer_path = os.path.join(os.path.split(optimizer_path)[0], prefix + ' ' + os.path.split(optimizer_path)[1])
        meta_path = os.path.join(os.path.split(meta_path)[0], prefix + ' ' + os.path.split(meta_path)[1])
    model_state_dict = load(model_path)
    optimizer_state_dict = torch.load(optimizer_path)
    with open(meta_path, 'rb') as pickle_file:
        metadata = pickle.load(pickle_file)
    if settings.restore_mode == 'continue':
        step = metadata['step']
        epoch = metadata['epoch']
    else:
        step = 0
        epoch = 0
    return model_state_dict, optimizer_state_dict, epoch, step
