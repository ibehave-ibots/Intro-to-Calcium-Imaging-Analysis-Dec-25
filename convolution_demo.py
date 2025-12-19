"""
Interactive demonstration of convolution using matplotlib animations.
Shows how a kernel slides over a signal and produces the convolution output.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
import argparse


# Create sample signal and kernels
def create_demo_data():
    """Create a simple signal and different kernel types for demonstration"""
    # Signal: neural spikes with single spikes and bursts
    signal = np.zeros(100)

    # Single spikes
    single_spikes = [15, 35, 75]
    signal[single_spikes] = 1.0

    # Burst 1 (3 spikes close together)
    burst1 = [48, 50, 52]
    signal[burst1] = 1.0

    # Burst 2 (4 spikes)
    burst2 = [85, 87, 88, 90]
    signal[burst2] = 1.0

    kernel_size = 15

    # Boxcar kernel (uniform/rectangular) - shorter width
    boxcar_size = 9
    boxcar = np.zeros(kernel_size)
    boxcar[:boxcar_size] = 1.0
    boxcar = boxcar / boxcar.sum()  # Normalize

    # Gaussian kernel
    kernel_x = np.linspace(-2, 2, kernel_size)
    gaussian = np.exp(-(kernel_x**2))
    gaussian = gaussian / gaussian.sum()  # Normalize

    # Exponential kernel (calcium decay-like)
    exp_x = np.arange(kernel_size)
    exponential = np.exp(-exp_x / 3.0)
    # Leave as-is - will be flipped during convolution to create decay after spike
    exponential = exponential / exponential.sum()  # Normalize

    kernels = {
        "Boxcar (Uniform)": boxcar,
        "Gaussian": gaussian,
        "Exponential (Calcium-like)": exponential,
    }

    return signal, kernels


def convolution_animation(kernel_name, kernel):
    """Create an animated visualization of convolution"""

    # Setup data
    signal, _ = create_demo_data()
    kernel_size = len(kernel)

    # Compute full convolution
    convolution = np.convolve(signal, kernel, mode="same")

    # Setup figure
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    fig.suptitle(
        f"Convolution with {kernel_name} Kernel", fontsize=16, fontweight="bold"
    )

    # Plot 1: Original signal with sliding window
    ax1.set_title("Neural Spikes (Input Signal)")
    ax1.set_xlim(0, len(signal))
    ax1.set_ylim(-0.2, 1.5)
    ax1.set_ylabel("Spike Amplitude")
    ax1.grid(True, alpha=0.3)

    (signal_line,) = ax1.plot(
        signal, "b-", linewidth=1, marker="o", markersize=3, label="Spikes"
    )
    (kernel_line,) = ax1.plot([], [], "r-", linewidth=2, label="Kernel (positioned)")
    window_patch = Rectangle(
        (0, -0.2),
        kernel_size,
        1.7,
        alpha=0.2,
        facecolor="yellow",
        edgecolor="orange",
        linewidth=2,
    )
    ax1.add_patch(window_patch)
    ax1.legend(loc="upper right")

    # Plot 2: Kernel (zoomed view)
    ax2.set_title("Kernel (Original)")
    ax2.set_xlim(-2, kernel_size + 2)
    ax2.set_ylim(0, max(kernel) * 1.3)
    ax2.set_ylabel("Weight")
    ax2.grid(True, alpha=0.3)

    (kernel_display,) = ax2.plot(kernel, "r-", linewidth=2, marker="o", markersize=4)
    ax2.fill_between(range(kernel_size), kernel, alpha=0.3, color="red")

    # Plot 3: Convolution output
    ax3.set_title("Convolution Output (Building Up)")
    ax3.set_xlim(0, len(signal))
    ax3.set_ylim(min(convolution) - 0.1, max(convolution) + 0.1)
    ax3.set_xlabel("Sample Index")
    ax3.set_ylabel("Amplitude")
    ax3.grid(True, alpha=0.3)

    (conv_line,) = ax3.plot([], [], "g-", linewidth=2, label="Convolution Result")
    (current_point,) = ax3.plot([], [], "ro", markersize=10, label="Current Output")
    ax3.legend(loc="upper right")

    plt.tight_layout()

    # Animation function
    def animate(frame):
        # Calculate position (center of kernel)
        pos = frame

        # Update sliding window highlight
        window_start = max(0, pos - kernel_size // 2)
        window_patch.set_x(window_start)

        # Position kernel on signal
        kernel_start = max(0, pos - kernel_size // 2)
        kernel_end = min(len(signal), pos + kernel_size // 2 + 1)

        # Create positioned kernel for visualization
        positioned_kernel = np.zeros_like(signal)
        k_start = max(0, kernel_size // 2 - pos)
        k_end = k_start + (kernel_end - kernel_start)

        if k_end > k_start:
            positioned_kernel[kernel_start:kernel_end] = np.flip(kernel)[k_start:k_end]

        kernel_line.set_data(
            range(len(signal)), positioned_kernel * 1.2
        )  # Scale for visibility

        # Update convolution output (show progress)
        conv_line.set_data(range(pos + 1), convolution[: pos + 1])
        current_point.set_data([pos], [convolution[pos]])

        return kernel_line, window_patch, conv_line, current_point

    # Create animation
    anim = FuncAnimation(
        fig, animate, frames=len(signal), interval=100, blit=True, repeat=True
    )

    return fig, anim


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Demonstrate convolution with different kernel types"
    )
    parser.add_argument(
        "--kernel",
        "-k",
        choices=["boxcar", "gaussian", "exponential"],
        required=True,
        help="Kernel type to use (boxcar, gaussian, or exponential)",
    )

    args = parser.parse_args()

    signal, kernels = create_demo_data()

    # Map kernel names
    kernel_map = {
        "boxcar": "Boxcar (Uniform)",
        "gaussian": "Gaussian",
        "exponential": "Exponential (Calcium-like)",
    }

    # Run animation for selected kernel
    kernel_name = kernel_map[args.kernel]
    kernel = kernels[kernel_name]
    fig, anim = convolution_animation(kernel_name, kernel)

    plt.show()
