from pathlib import Path
import uuid

import torch
from torchvision.utils import save_image

from models.generator import Generator


class GeneratorService:
    def __init__(self, model_path: Path, output_dir: Path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.model = Generator(nz=100, ngf=64, nc=3).to(self.device)
        try:
            state_dict = torch.load(model_path, map_location=self.device, weights_only=True)
        except TypeError:
            state_dict = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.eval()

    def generate(self) -> str:
        noise = torch.randn(1, 100, 1, 1, device=self.device)
        with torch.inference_mode():
            fake = self.model(noise).cpu()

        filename = f"generated_{uuid.uuid4().hex}.png"
        output_path = self.output_dir / filename
        # The notebook uses Tanh output in [-1, 1]; normalize=True maps it to a valid PNG.
        save_image(fake, str(output_path), normalize=True)
        return filename
