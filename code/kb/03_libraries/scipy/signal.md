# SciPy Signal Processing (scipy.signal)

Source: https://docs.scipy.org/doc/scipy/reference/signal.html

# Signal processing (scipy.signal) -- SciPy v1.17.0 Manual

Signal processing (`scipy.signal`)

## Convolution

`convolve(in1, in2[, mode, method])`
Convolve two N-dimensional arrays.

`correlate(in1, in2[, mode, method])`
Cross-correlate two N-dimensional arrays.

`fftconvolve(in1, in2[, mode, axes])`
Convolve two N-dimensional arrays using FFT.

`oaconvolve(in1, in2[, mode, axes])`
Convolve two N-dimensional arrays using the overlap-add method.

`convolve2d(in1, in2[, mode, boundary, fillvalue])`
Convolve two 2-dimensional arrays.

`correlate2d(in1, in2[, mode, boundary, ...])`
Cross-correlate two 2-dimensional arrays.

`sepfir2d(input, hrow, hcol)`
Convolve with a 2-D separable FIR filter.

`choose_conv_method(in1, in2[, mode, measure])`
Find the fastest convolution/correlation method.

`correlation_lags(in1_len, in2_len[, mode])`
Calculates the lag / displacement indices array for 1D cross-correlation.

## B-splines

`gauss_spline(x, n)`
Gaussian approximation to B-spline basis function of order n.

`cspline1d(signal[, lamb])`
Compute cubic spline coefficients for rank-1 array.

`qspline1d(signal[, lamb])`
Compute quadratic spline coefficients for rank-1 array.

`cspline2d(signal[, lamb, precision])`
Coefficients for 2-D cubic (3rd order) B-spline.

`qspline2d(signal[, lamb, precision])`
Coefficients for 2-D quadratic (2nd order) B-spline.

`cspline1d_eval(cj, newx[, dx, x0])`
Evaluate a cubic spline at the new set of points.

`qspline1d_eval(cj, newx[, dx, x0])`
Evaluate a quadratic spline at the new set of points.

`spline_filter(Iin[, lmbda])`
Smoothing spline (cubic) filtering of a rank-2 array.

## Filtering

`order_filter(a, domain, rank)`
Perform an order filter on an N-D array.

`medfilt(volume[, kernel_size])`
Perform a median filter on an N-dimensional array.

`medfilt2d(input[, kernel_size])`
Median filter a 2-dimensional array.

`wiener(im[, mysize, noise])`
Perform a Wiener filter on an N-dimensional array.

`symiirorder1(signal, c0, z1[, precision])`
Implement a smoothing IIR filter with mirror-symmetric boundary conditions using a cascade of first-order sections.

`symiirorder2(input, r, omega[, precision])`
Implement a smoothing IIR filter with mirror-symmetric boundary conditions using a cascade of second-order sections.

`lfilter(b, a, x[, axis, zi])`
Filter data along one-dimension with an IIR or FIR filter.

`lfiltic(b, a, y[, x])`
Construct initial conditions for lfilter given input and output vectors.

`lfilter_zi(b, a)`
Construct initial conditions for lfilter for step response steady-state.

`filtfilt(b, a, x[, axis, padtype, padlen, ...])`
Apply a digital filter forward and backward to a signal.

`savgol_filter(x, window_length, polyorder[, ...])`
Apply a Savitzky-Golay filter to an array.

`deconvolve(signal, divisor)`
Deconvolves `divisor` out of `signal` using inverse filtering.

`sosfilt(sos, x[, axis, zi])`
Filter data along one dimension using cascaded second-order sections.

`sosfilt_zi(sos)`
Construct initial conditions for sosfilt for step response steady-state.

`sosfiltfilt(sos, x[, axis, padtype, padlen])`
A forward-backward digital filter using cascaded second-order sections.

`hilbert(x[, N, axis])`
FFT-based computation of the analytic signal.

`hilbert2(x[, N, axes])`
Compute the '2-D' analytic signal of *x*.

`envelope(z[, bp_in, n_out, squared, ...])`
Compute the envelope of a real- or complex-valued signal.

`decimate(x, q[, n, ftype, axis, zero_phase])`
Downsample the signal after applying an anti-aliasing filter.

`detrend(data[, axis, type, bp, overwrite_data])`
Remove linear or constant trend along axis from data.

`resample(x, num[, t, axis, window, domain])`
Resample *x* to *num* samples using the Fourier method along the given *axis*.

`resample_poly(x, up, down[, axis, window, ...])`
Resample *x* along the given axis using polyphase filtering.

`upfirdn(h, x[, up, down, axis, mode, cval])`
Upsample, FIR filter, and downsample.

## Filter design

`bilinear(b, a[, fs])`
Calculate a digital IIR filter from an analog transfer function by utilizing the bilinear transform.

`bilinear_zpk(z, p, k, fs)`
Return a digital IIR filter from an analog one using a bilinear transform.

`findfreqs(num, den, N[, kind])`
Find array of frequencies for computing the response of an analog filter.

`firls(numtaps, bands, desired, *[, weight, fs])`
FIR filter design using least-squares error minimization.

`firwin(numtaps, cutoff, *[, width, window, ...])`
FIR filter design using the window method.

`firwin2(numtaps, freq, gain, *[, nfreqs, ...])`
FIR filter design using the window method.

`firwin_2d(hsize, window, *[, fc, fs, ...])`
2D FIR filter design using the window method.

`freqs(b, a[, worN, plot])`
Compute frequency response of analog filter.

`freqs_zpk(z, p, k[, worN])`
Compute frequency response of analog filter.

`freqz(b[, a, worN, whole, plot, fs, ...])`
Compute the frequency response of a digital filter.

`sosfreqz(*args, **kwargs)`
Compute the frequency response of a digital filter in SOS format (legacy).

`freqz_sos(sos[, worN, whole, fs])`
Compute the frequency response of a digital filter in SOS format.

`freqz_zpk(z, p, k[, worN, whole, fs])`
Compute the frequency response of a digital filter in ZPK form.

`gammatone(freq, ftype[, order, numtaps, fs, ...])`
Gammatone filter design.

`group_delay(system[, w, whole, fs])`
Compute the group delay of a digital filter.

`iirdesign(wp, ws, gpass, gstop[, analog, ...])`
Complete IIR digital and analog filter design.

`iirfilter(N, Wn[, rp, rs, btype, analog, ...])`
IIR digital and analog filter design given order and critical points.

`kaiser_atten(numtaps, width)`
Compute the attenuation of a Kaiser FIR filter.

`kaiser_beta(a)`
Compute the Kaiser parameter *beta*, given the attenuation *a*.

`kaiserord(ripple, width)`
Determine the filter window parameters for the Kaiser window method.

`minimum_phase(h[, method, n_fft, half])`
Convert a linear-phase FIR filter to minimum phase

`savgol_coeffs(window_length, polyorder[, ...])`
Compute the coefficients for a 1-D Savitzky-Golay FIR filter.

`remez(numtaps, bands, desired, *[, weight, ...])`
Calculate the minimax optimal filter using the Remez exchange algorithm.

`unique_roots(p[, tol, rtype])`
Determine unique roots and their multiplicities from a list of roots.

`residue(b, a[, tol, rtype])`
Compute partial-fraction expansion of b(s) / a(s).

`residuez(b, a[, tol, rtype])`
Compute partial-fraction expansion of b(z) / a(z).

`invres(r, p, k[, tol, rtype])`
Compute b(s) and a(s) from partial fraction expansion.

`invresz(r, p, k[, tol, rtype])`
Compute b(z) and a(z) from partial fraction expansion.

`BadCoefficients`
Warning about badly conditioned filter coefficients

Lower-level filter design functions:

`abcd_normalize([A, B, C, D])`
Check state-space matrices compatibility and ensure they are 2d arrays.

`band_stop_obj(wp, ind, passb, stopb, gpass, ...)`
Band Stop Objective Function for order minimization.

`besselap(N[, norm, xp, device])`
Return (z,p,k) for analog prototype of an Nth-order Bessel filter.

`buttap(N, *[, xp, device])`
Return (z,p,k) for analog prototype of Nth-order Butterworth filter.

`cheb1ap(N, rp, *[, xp, device])`
Return (z,p,k) for Nth-order Chebyshev type I analog lowpass filter.

`cheb2ap(N, rs, *[, xp, device])`
Return (z,p,k) for Nth-order Chebyshev type II analog lowpass filter.

`ellipap(N, rp, rs, *[, xp, device])`
Return (z,p,k) of Nth-order elliptic analog lowpass filter.

`lp2bp(b, a[, wo, bw])`
Transform a lowpass filter prototype to a bandpass filter.

`lp2bp_zpk(z, p, k[, wo, bw])`
Transform a lowpass filter prototype to a bandpass filter.

`lp2bs(b, a[, wo, bw])`
Transform a lowpass filter prototype to a bandstop filter.

`lp2bs_zpk(z, p, k[, wo, bw])`
Transform a lowpass filter prototype to a bandstop filter.

`lp2hp(b, a[, wo])`
Transform a lowpass filter prototype to a highpass filter.

`lp2hp_zpk(z, p, k[, wo])`
Transform a lowpass filter prototype to a highpass filter.

`lp2lp(b, a[, wo])`
Transform a lowpass filter prototype to a different frequency.

`lp2lp_zpk(z, p, k[, wo])`
Transform a lowpass filter prototype to a different frequency.

`normalize(b, a)`
Normalize numerator/denominator of a continuous-time transfer function.

## Matlab-style IIR filter design

`butter(N, Wn[, btype, analog, output, fs])`
Butterworth digital and analog filter design.

`buttord(wp, ws, gpass, gstop[, analog, fs])`
Butterworth filter order selection.

`cheby1(N, rp, Wn[, btype, analog, output, fs])`
Chebyshev type I digital and analog filter design.

`cheb1ord(wp, ws, gpass, gstop[, analog, fs])`
Chebyshev type I filter order selection.

`cheby2(N, rs, Wn[, btype, analog, output, fs])`
Chebyshev type II digital and analog filter design.

`cheb2ord(wp, ws, gpass, gstop[, analog, fs])`
Chebyshev type II filter order selection.

`ellip(N, rp, rs, Wn[, btype, analog, output, fs])`
Elliptic (Cauer) digital and analog filter design.

`ellipord(wp, ws, gpass, gstop[, analog, fs])`
Elliptic (Cauer) filter order selection.

`bessel(N, Wn[, btype, analog, output, norm, fs])`
Bessel/Thomson digital and analog filter design.

`iirnotch(w0, Q[, fs, xp, device])`
Design second-order IIR notch digital filter.

`iirpeak(w0, Q[, fs, xp, device])`
Design second-order IIR peak (resonant) digital filter.

`iircomb(w0, Q[, ftype, fs, pass_zero, xp, ...])`
Design IIR notching or peaking digital comb filter.

## Continuous-time linear systems

`lti(*system)`
Continuous-time linear time invariant system base class.

`StateSpace(*system, **kwargs)`
Linear Time Invariant system in state-space form.

`TransferFunction(*system, **kwargs)`
Linear Time Invariant system class in transfer function form.

`ZerosPolesGain(*system, **kwargs)`
Linear Time Invariant system class in zeros, poles, gain form.

`lsim(system, U, T[, X0, interp])`
Simulate output of a continuous-time linear system.

`impulse(system[, X0, T, N])`
Impulse response of continuous-time system.

`step(system[, X0, T, N])`
Step response of continuous-time system.

`freqresp(system[, w, n])`
Calculate the frequency response of a continuous-time system.

`bode(system[, w, n])`
Calculate Bode magnitude and phase data of a continuous-time system.

## Discrete-time linear systems

`dlti(*system, **kwargs)`
Discrete-time linear time invariant system base class.

`StateSpace(*system, **kwargs)`
Linear Time Invariant system in state-space form.

`TransferFunction(*system, **kwargs)`
Linear Time Invariant system class in transfer function form.

`ZerosPolesGain(*system, **kwargs)`
Linear Time Invariant system class in zeros, poles, gain form.

`dlsim(system, u[, t, x0])`
Simulate output of a discrete-time linear system.

`dimpulse(system[, x0, t, n])`
Impulse response of discrete-time system.

`dstep(system[, x0, t, n])`
Step response of discrete-time system.

`dfreqresp(system[, w, n, whole])`
Calculate the frequency response of a discrete-time system.

`dbode(system[, w, n])`
Calculate Bode magnitude and phase data of a discrete-time system.

## LTI representations

`tf2zpk(b, a)`
Return zero, pole, gain (z, p, k) representation from a numerator, denominator representation of a linear filter.

`tf2sos(b, a[, pairing, analog])`
Return second-order sections from transfer function representation

`tf2ss(num, den)`
Transfer function to state-space representation.

`zpk2tf(z, p, k)`
Return polynomial transfer function representation from zeros and poles

`zpk2sos(z, p, k[, pairing, analog])`
Return second-order sections from zeros, poles, and gain of a system

`zpk2ss(z, p, k)`
Zero-pole-gain representation to state-space representation

`ss2tf(A, B, C, D[, input])`
State-space to transfer function.

`ss2zpk(A, B, C, D[, input])`
State-space representation to zero-pole-gain representation.

`sos2zpk(sos)`
Return zeros, poles, and gain of a series of second-order sections

`sos2tf(sos)`
Return a single transfer function from a series of second-order sections

`cont2discrete(system, dt[, method, alpha])`
Transform a continuous to a discrete state-space system.

`place_poles(A, B, poles[, method, rtol, maxiter])`
Compute K such that eigenvalues (A - dot(B, K))=poles.

## Waveforms

`chirp(t, f0, t1, f1[, method, phi, ...])`
Frequency-swept cosine generator.

`gausspulse(t[, fc, bw, bwr, tpr, retquad, ...])`
Return a Gaussian modulated sinusoid:

`max_len_seq(nbits[, state, length, taps])`
Maximum length sequence (MLS) generator.

`sawtooth(t[, width])`
Return a periodic sawtooth or triangle waveform.

`square(t[, duty])`
Return a periodic square-wave waveform.

`sweep_poly(t, poly[, phi])`
Frequency-swept cosine generator, with a time-dependent frequency.

`unit_impulse(shape[, idx, dtype])`
Unit impulse signal (discrete delta function) or unit basis vector.

## Window functions

For window functions, see the `scipy.signal.windows` namespace.

In the `scipy.signal` namespace, there is a convenience function to obtain these windows by name:

`get_window(window, Nx[, fftbins, xp, device])`
Convenience function for creating various windows.

## Peak finding

`argrelmin(data[, axis, order, mode])`
Calculate the relative minima of *data*.

`argrelmax(data[, axis, order, mode])`
Calculate the relative maxima of *data*.

`argrelextrema(data, comparator[, axis, ...])`
Calculate the relative extrema of *data*.

`find_peaks(x[, height, threshold, distance, ...])`
Find peaks inside a signal based on peak properties.

`find_peaks_cwt(vector, widths[, wavelet, ...])`
Find peaks in a 1-D array with wavelet transformation.

`peak_prominences(x, peaks[, wlen])`
Calculate the prominence of each peak in a signal.

`peak_widths(x, peaks[, rel_height, ...])`
Calculate the width of each peak in a signal.

## Spectral analysis

`periodogram(x[, fs, window, nfft, detrend, ...])`
Estimate power spectral density using a periodogram.

`welch(x[, fs, window, nperseg, noverlap, ...])`
Estimate power spectral density using Welch's method.

`csd(x, y[, fs, window, nperseg, noverlap, ...])`
Estimate the cross power spectral density, Pxy, using Welch's method.

`coherence(x, y[, fs, window, nperseg, ...])`
Estimate the magnitude squared coherence estimate, Cxy, of discrete-time signals X and Y using Welch's method.

`spectrogram(x[, fs, window, nperseg, ...])`
Compute a spectrogram with consecutive Fourier transforms (legacy function).

`lombscargle(x, y, freqs, *[, precenter, ...])`
Compute the generalized Lomb-Scargle periodogram.

`vectorstrength(events, period)`
Determine the vector strength of the events corresponding to the given period.

`ShortTimeFFT(win, hop, fs, *[, fft_mode, ...])`
Provide a parametrized discrete Short-time Fourier transform (stft) and its inverse (istft).

`closest_STFT_dual_window(win, hop[, ...])`
Calculate the STFT dual window of a given window closest to a desired dual window.

`stft(x[, fs, window, nperseg, noverlap, ...])`
Compute the Short Time Fourier Transform (legacy function).

`istft(Zxx[, fs, window, nperseg, noverlap, ...])`
Perform the inverse Short Time Fourier transform (legacy function).

`check_COLA(window, nperseg, noverlap[, tol])`
Check whether the Constant OverLap Add (COLA) constraint is met (legacy function).

`check_NOLA(window, nperseg, noverlap[, tol])`
Check whether the Nonzero Overlap Add (NOLA) constraint is met.

## Chirp Z-transform and Zoom FFT

`czt(x[, m, w, a, axis])`
Compute the frequency response around a spiral in the Z plane.

`zoom_fft(x, fn[, m, fs, endpoint, axis])`
Compute the DFT of *x* only for frequencies in range *fn*.

`CZT(n[, m, w, a])`
Create a callable chirp z-transform function.

`ZoomFFT(n, fn[, m, fs, endpoint])`
Create a callable zoom FFT transform function.

`czt_points(m[, w, a])`
Return the points at which the chirp z-transform is computed.

The functions are simpler to use than the classes, but are less efficient when using the same transform on many arrays of the same length, since they repeatedly generate the same chirp signal with every call. In these cases, use the classes to create a reusable function instead.
