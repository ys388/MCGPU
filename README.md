MC-GPU
==
MC-GPU is an open-source software to calculate X-ray scattering signals. We here provide a detailed documentation and codes converting the measured signals to projections and CT images reconstruction. https://code.google.com/archive/p/mcgpu/downloads

Phantom
==
We used a real clinical dataset authorized for “the 2016 NIH-AAPM-Mayo Clinic Low Dose CT Grand Challenge" by Mayo Clinic for MC simulation.https://www.aapm.org/GrandChallenge/LowDoseCT/

Use
==
1. run prep.py to convert 'dicom file' to 'numpy array'.
2. run npy2vox.py to obtain the phantom that can be performed simulations in MC-GPU.
3. run MC-GPU.
4. run fan_beam_reconstruction.py to obtain scatter-free images and scatter-contaminated images.

More details can be seen in the documentation of MC-GPU.
