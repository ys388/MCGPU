MC-GPU
==
MC-GPU [1] is an open-source software to calculate X-ray scattering signals. We here provide a detailed documentation and codes converting the measured signals to projections and CT images reconstruction.

Phantom
==
We used a real clinical dataset authorized for “the 2016 NIH-AAPM-Mayo Clinic Low Dose CT Grand Challenge" by Mayo Clinic for MC simulation.

Use
==
1. run prep.py to convert 'dicom file' to 'numpy array'
2. run npy2vox.py to obtain the phantom that can be performed simulations in MC-GPU.
3. run MC-GPU
4. run fan_beam_reconstruction.py to obtain scatter-free images and scatter-contaminated images.

