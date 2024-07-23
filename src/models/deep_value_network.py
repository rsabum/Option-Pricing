from torch import Tensor, save, load
from torch.nn import Module, MSELoss, Sequential, Conv2d, ReLU, Flatten, Linear
from torch.optim import Adam
from source.dataset import TransitionDataLoader
from numpy import ndarray, mean
from tqdm import trange

class DeepValueNetwork(Module):
    """
    Deep Value Network class for training a value function approximation model.

    Parameters
    ----------
    num_in_channels: int
        Number of input channels.
    
    num_out_channels: int
        Number of output channels.
    
    kernel_size: int
        Size of the convolutional kernel.
    
    padding: int
        Padding size for the convolutional layer.
    
    hidden_1_size: int
        Size of the first hidden layer.
    
    hidden_2_size: int
        Size of the second hidden layer.
    
    learning_rate: float
        Learning rate for the optimizer.
    
    device: str 
        Device to use for training (e.g., 'cpu', 'cuda').

    Returns
    -------
    None

    Attributes
    ----------
        net: Sequential
            The neural network model.
        
        loss: MSELoss 
            The loss function for training.
        
        optimizer: Adam 
            The optimizer for updating the model parameters.
        
        device: str 
            The device used for training.
    """

    def __init__(
        self,
        num_in_channels: int,
        num_out_channels: int,
        kernel_size: int,
        padding: int,
        hidden_1_size: int,
        hidden_2_size: int,
        learning_rate: float,
        device: str,
    ) -> None:
        super(DeepValueNetwork, self).__init__()

        layers = []

        layers.append(Conv2d(
            in_channels=num_in_channels,
            out_channels=num_out_channels,
            kernel_size=kernel_size,
            padding=padding
        ))

        layers.append(ReLU())
        layers.append(Flatten())
        layers.append(Linear(
            in_features=num_out_channels * 64,
            out_features=hidden_1_size
        ))

        layers.append(ReLU())
        layers.append(Linear(
            in_features=hidden_1_size,
            out_features=hidden_2_size
        ))

        layers.append(ReLU())
        layers.append(Linear(
            in_features=hidden_2_size,
            out_features=1
        ))

        self.net = Sequential(*layers)
        self.loss = MSELoss()
        self.optimizer = Adam(
            params=self.parameters(),
            lr=learning_rate
        )

        self.initialize_weights()

        self.device = device
        self.to(self.device)


    def initialize_weights(self) -> None:
        """
        Initialize the network weights.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        for layer in self.net:
            if hasattr(layer, 'weight'):
                layer.weight.data.normal_(0, 0.01)

    def forward(
        self,
        observation: ndarray
    ) -> Tensor:
        """
        Forward pass of the network.

        Parameters
        ----------
        observation: ndarray 
            The input observation(s) i.e., the chess board(s).

        Returns
        -------
        Tensor: 
            The value estimate(s) of the given observation(s).
        """

        observation = Tensor(observation).to(self.device)
        observation = observation.float()
        value_estimate = self.net(observation).squeeze()
        return value_estimate

    def fit(
        self,
        data_loader: TransitionDataLoader,
        discount_factor: float,
        num_batches: int,
        model_path: str,
        log_path: str,
    ) -> list[float]:
        """
        Train the network using train dataloader.

        Parameters
        ----------
        data_loader: TransitionDataLoader
            The data loader containing the transition data.

        discount_factor: float
            The discount factor for the Bellman equation.

        num_batches: int
            The number of batches to train on.

        model_path: str
            The path to save the trained model.

        log_path: str
            The path to save the training log.

        Returns
        -------
        list[float]: 
            A list of the TD errors for each batch.
        """

        td_error_history = []
        avg_error = lambda: mean(td_error_history[-100:])

        batches = iter(data_loader)
        batch_cntr = 1

        log_file = open(log_path, "w")

        print("Training started...")
        for _ in trange(num_batches, desc="Training", unit=" batches"):

            state_batch, reward_batch, next_state_batch, terminal_batch = next(batches)

            self.optimizer.zero_grad()

            values = self.forward(state_batch)
            next_values = self.forward(next_state_batch)
            next_values[terminal_batch] = 0.0

            target_values = reward_batch + discount_factor * next_values

            error = self.loss(values, target_values).to(self.device)
            error.backward()
            self.optimizer.step()

            td_error_history.append(error.item())

            log_file.write(f"Batch: {batch_cntr} \t|\t TD Error: {error:.5f} \t|\t Avg TD Error: {avg_error():.5f}\n")

            batch_cntr += 1

        print("Training finished")

        self.save_model(model_path)
        print(f"Model saved to {model_path}")

        log_file.close()
        print(f"Training Log saved to {log_path}")

        return td_error_history

    def save_model(
        self,
        model_path: str
    ) -> None:
        """
        Save the model to a file.

        Parameters
        ----------
        model_path: str 
            The path to save the model.
        """

        save(self.state_dict(), model_path)

    def load_model(
        self,
        model_path: str
    ) -> None:
        """
        Load a saved model from a file.

        Parameters
        ----------
        model_path: str
            The path to the saved model.
        """

        self.load_state_dict(load(model_path))