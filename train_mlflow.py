<<<<<<< HEAD
import argparse
import os
import time

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

import torchvision
import torchvision.transforms as transforms

import mlflow
import mlflow.pytorch


class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 128), nn.ReLU(),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        return self.net(x)


@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    correct = 0
    total = 0
    running_loss = 0.0
    criterion = nn.CrossEntropyLoss()

    for x, y in loader:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        loss = criterion(logits, y)
        running_loss += loss.item() * x.size(0)

        preds = torch.argmax(logits, dim=1)
        correct += (preds == y).sum().item()
        total += y.size(0)

    avg_loss = running_loss / max(total, 1)
    acc = correct / max(total, 1)
    return avg_loss, acc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--learning_rate", type=float, default=0.01)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--student_id", type=str, default="202200899")
    parser.add_argument("--experiment_name", type=str, default="Assignment3_Muhammad Kamal")
    args = parser.parse_args()

    # Reproducibility
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # MLflow pillars
    mlflow.set_experiment(args.experiment_name)
    mlflow.set_tag("student_id", args.student_id)
    mlflow.set_tag("framework", "pytorch")
    mlflow.set_tag("device", device)



    # Data
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    train_ds = torchvision.datasets.MNIST(root="./data", train=True, download=True, transform=transform)
    test_ds = torchvision.datasets.MNIST(root="./data", train=False, download=True, transform=transform)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=2)
    test_loader = DataLoader(test_ds, batch_size=args.batch_size, shuffle=False, num_workers=2)

    model = SimpleCNN(num_classes=10).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=args.learning_rate, momentum=0.9)

    try:
        mlflow.end_run()
    except Exception:
        pass

    with mlflow.start_run():
        mlflow.log_params({
        "learning_rate": args.learning_rate,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "seed": args.seed,
        "model": "SimpleCNN",
        "dataset": "MNIST",
    })
        mlflow.set_tag("run_name", f"lr={args.learning_rate}_bs={args.batch_size}_seed={args.seed}")

        for epoch in range(1, args.epochs + 1):
            model.train()
            epoch_loss = 0.0
            correct = 0
            total = 0
            t0 = time.time()

            for x, y in train_loader:
                x, y = x.to(device), y.to(device)
                optimizer.zero_grad()

                logits = model(x)
                loss = criterion(logits, y)
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item() * x.size(0)
                preds = torch.argmax(logits, dim=1)
                correct += (preds == y).sum().item()
                total += y.size(0)

            train_loss = epoch_loss / max(total, 1)
            train_acc = correct / max(total, 1)

            val_loss, val_acc = evaluate(model, test_loader, device)
            epoch_time = time.time() - t0

            # Live logging at end of every epoch (required)
            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("train_accuracy", train_acc, step=epoch)
            mlflow.log_metric("val_loss", val_loss, step=epoch)
            mlflow.log_metric("val_accuracy", val_acc, step=epoch)
            mlflow.log_metric("epoch_time_sec", epoch_time, step=epoch)

            print(
                f"Epoch {epoch}/{args.epochs} | "
                f"train_loss={train_loss:.4f}, train_acc={train_acc:.4f} | "
                f"val_loss={val_loss:.4f}, val_acc={val_acc:.4f}"
            )

        
        mlflow.pytorch.log_model(model, artifact_path="model")

        os.makedirs("artifacts", exist_ok=True)
        torch.save(model.state_dict(), "artifacts/model_state_dict.pt")
        mlflow.log_artifact("artifacts/model_state_dict.pt")


if __name__ == "__main__":
=======
import argparse
import os
import time

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

import torchvision
import torchvision.transforms as transforms

import mlflow
import mlflow.pytorch


class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 128), nn.ReLU(),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        return self.net(x)


@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    correct = 0
    total = 0
    running_loss = 0.0
    criterion = nn.CrossEntropyLoss()

    for x, y in loader:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        loss = criterion(logits, y)
        running_loss += loss.item() * x.size(0)

        preds = torch.argmax(logits, dim=1)
        correct += (preds == y).sum().item()
        total += y.size(0)

    avg_loss = running_loss / max(total, 1)
    acc = correct / max(total, 1)
    return avg_loss, acc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--learning_rate", type=float, default=0.01)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--student_id", type=str, default="202200899")
    parser.add_argument("--experiment_name", type=str, default="Assignment3_Muhammad Kamal")
    args = parser.parse_args()

    # Reproducibility
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # MLflow pillars
    mlflow.set_experiment(args.experiment_name)
    mlflow.set_tag("student_id", args.student_id)
    mlflow.set_tag("framework", "pytorch")
    mlflow.set_tag("device", device)



    # Data
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    train_ds = torchvision.datasets.MNIST(root="./data", train=True, download=True, transform=transform)
    test_ds = torchvision.datasets.MNIST(root="./data", train=False, download=True, transform=transform)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=2)
    test_loader = DataLoader(test_ds, batch_size=args.batch_size, shuffle=False, num_workers=2)

    model = SimpleCNN(num_classes=10).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=args.learning_rate, momentum=0.9)

    try:
        mlflow.end_run()
    except Exception:
        pass

    with mlflow.start_run():
        mlflow.log_params({
        "learning_rate": args.learning_rate,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "seed": args.seed,
        "model": "SimpleCNN",
        "dataset": "MNIST",
    })
        mlflow.set_tag("run_name", f"lr={args.learning_rate}_bs={args.batch_size}_seed={args.seed}")

        for epoch in range(1, args.epochs + 1):
            model.train()
            epoch_loss = 0.0
            correct = 0
            total = 0
            t0 = time.time()

            for x, y in train_loader:
                x, y = x.to(device), y.to(device)
                optimizer.zero_grad()

                logits = model(x)
                loss = criterion(logits, y)
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item() * x.size(0)
                preds = torch.argmax(logits, dim=1)
                correct += (preds == y).sum().item()
                total += y.size(0)

            train_loss = epoch_loss / max(total, 1)
            train_acc = correct / max(total, 1)

            val_loss, val_acc = evaluate(model, test_loader, device)
            epoch_time = time.time() - t0

            # Live logging at end of every epoch (required)
            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("train_accuracy", train_acc, step=epoch)
            mlflow.log_metric("val_loss", val_loss, step=epoch)
            mlflow.log_metric("val_accuracy", val_acc, step=epoch)
            mlflow.log_metric("epoch_time_sec", epoch_time, step=epoch)

            print(
                f"Epoch {epoch}/{args.epochs} | "
                f"train_loss={train_loss:.4f}, train_acc={train_acc:.4f} | "
                f"val_loss={val_loss:.4f}, val_acc={val_acc:.4f}"
            )

        
        mlflow.pytorch.log_model(model, artifact_path="model")

        os.makedirs("artifacts", exist_ok=True)
        torch.save(model.state_dict(), "artifacts/model_state_dict.pt")
        mlflow.log_artifact("artifacts/model_state_dict.pt")


if __name__ == "__main__":
>>>>>>> c6b3f959c497327714439fdbb3fca8254bf369c3
    main()