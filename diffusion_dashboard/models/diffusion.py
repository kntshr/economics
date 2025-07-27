from __future__ import annotations
import numpy as np

def logistic(t, K, r, tau):
    return K / (1.0 + np.exp(-r * (t - tau)))

def fit_logistic_quick(t, y):
    import numpy as np
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    K0 = max(1.1 * np.nanmax(y), 1e-6)
    y_clip = np.clip(y, 1e-6, K0 - 1e-6)
    z = np.log(K0 / y_clip - 1.0)
    A = np.vstack([np.ones_like(t), t]).T
    a, b = np.linalg.lstsq(A, z, rcond=None)[0]
    r = -b
    tau = a / b if b != 0 else np.median(t)
    return {"K": float(K0), "r": float(r), "tau": float(tau)}
